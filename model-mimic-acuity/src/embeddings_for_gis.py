# do not call `module load miniconda3/23.3.1-py310` otherwise you get an error
# regarding: AttributeError: module 'collections' has no attribute 'MutableMapping' bc of python 3.10

'''This script is different from embeddings.py because it focuses on getting the embeddings across the 
train,val,and test images combined. It saves the full filepath of the corresponding image to the metadata.tsv associated with
the embeddings. This way we get access to both the specific image name and species label for GIS analysis.'''

import os
import cv2
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import argparse
import catalyst.dl as dl
from catalyst.contrib.nn import ArcFace
from tensorboardX import SummaryWriter
import albumentations as albu
from albumentations.pytorch.transforms import ToTensorV2

from dir_paths.dataset_paths import get_image_dataset_path
from dir_paths.train_val_test_paths import get_split_csvs
from dataloader import read_image, read_sized_image, get_transforms, get_loader
from utils import load_model
from dir_paths.model_log_paths import get_logdir
from model import ResNetEncoder, EncoderWithHead
from dir_paths.embedding_paths import get_embedding_paths
# from embeddings import save_embeddings, save_merged_embeddings

index2species = {0: 'Heliconius melpomene ssp. ecuadorensis',
 1: 'Heliconius melpomene ssp. nanna',
 2: 'Heliconius melpomene ssp. rosina',
 3: 'Heliconius erato ssp. phyllis',
 4: 'Heliconius erato ssp. dignus',
 5: 'Heliconius melpomene ssp. bellula',
 6: 'Heliconius erato ssp. lativitta',
 7: 'Heliconius melpomene ssp. vulcanus',
 8: 'Heliconius erato ssp. etylus',
 9: 'Heliconius melpomene ssp. plesseni',
 10: 'Heliconius melpomene ssp. malleti',
 11: 'Heliconius erato ssp. cyrbia',
 12: 'Heliconius erato ssp. amalfreda',
 13: 'Heliconius erato ssp. venus',
 14: 'Heliconius erato ssp. hydara',
 15: 'Heliconius melpomene ssp. meriana', 
 16: 'Heliconius erato ssp. petiverana',
 17: 'Heliconius melpomene ssp. cythera',
 18: 'Heliconius erato ssp. notabilis',
 19: 'Heliconius melpomene ssp. melpomene'}

index2species_erato = {
0: 'Heliconius erato ssp. phyllis',
1: 'Heliconius erato ssp. dignus',
2: 'Heliconius erato ssp. lativitta',
3: 'Heliconius erato ssp. etylus',
4: 'Heliconius erato ssp. cyrbia',
5: 'Heliconius erato ssp. amalfreda', #meriana is the melpomene mimic
6: 'Heliconius erato ssp. venus',
7: 'Heliconius erato ssp. hydara',
8: 'Heliconius erato ssp. petiverana',
9: 'Heliconius erato ssp. notabilis'}

index2species_melpomene = {
0: 'Heliconius melpomene ssp. nanna',
1: 'Heliconius melpomene ssp. bellula',
2: 'Heliconius melpomene ssp. malleti',
3: 'Heliconius melpomene ssp. ecuadorensis',
4: 'Heliconius melpomene ssp. cythera',
5: 'Heliconius melpomene ssp. meriana', #Missing from index2species in dorsal images
6: 'Heliconius melpomene ssp. vulcanus',
7: 'Heliconius melpomene ssp. melpomene',
8: 'Heliconius melpomene ssp. rosina',
9: 'Heliconius melpomene ssp. plesseni',
}

index2species_mimics = {
     0:'mimic_0',
     1:'mimic_1',
     2:'mimic_2',
     3:'mimic_3',
     4:'mimic_4',
     5:'mimic_5',
     6:'mimic_6',
     7:'mimic_7',
     8:'mimic_8',
     9:'mimic_9'

}
species2index = {v:k for k,v in index2species.items()}
species2index_erato = {v:k for k,v in index2species_erato.items()}
species2index_melpomene = {v:k for k,v in index2species_melpomene.items()}
species2index_mimics = species2index_erato
species2index_mimics.update(species2index_melpomene)

def predict_embeddings(df, encoder, device: str="cpu"):
    #move encoder to cuda device if available and use for eval only
    encoder = encoder.to(device)
    encoder = encoder.eval()

    #get embeddings on dataset from our model
    embeddings = []
    img_paths = []
    
    transforms = albu.Compose([
            albu.Resize(224, 224),
            albu.Normalize(),
            ToTensorV2()
        ])
    
    with torch.no_grad():
        for fp in df['path']:
            img = cv2.cvtColor(cv2.imread(fp), cv2.COLOR_BGR2RGB)#.to(device)
            img = transforms(image=img)["image"][None,:]
            img_paths.append(fp)

            #predict embeddings using encoder
            output = F.normalize(encoder(img))
            output = output.detach().cpu().numpy()
            output = np.reshape(output, (output.shape[1])) #reshape to dim: (128,)
            embeddings.append(output)
            
    #flatten out lists created per batch
    embeddings = np.array(embeddings)
    img_paths = np.array(img_paths) 

    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Img_paths shape: {img_paths.shape}")

    return embeddings, img_paths


def save_embeddings(embeddings, labels, directory):
    '''function to save embeddings alongside image paths for traceability '''
    all_embeddings = np.concatenate([e for e in embeddings], axis=0)
    all_labels = np.concatenate([l for l in labels], axis=0)

    if not os.path.isdir(directory):
        os.makedirs(directory)

    # store embeddings
    writer = SummaryWriter(logdir=os.path.join(directory, "embeddings"))

    writer.add_embedding(
        all_embeddings,
        metadata=all_labels
    )

    writer.close()
    return all_embeddings, all_labels

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--acuity", required=True, help="no_acuity, male_b, female_b, male_m, female_m, kingfisher")
    parser.add_argument("--model", required=True, help="regular, erato, melpomene, mimics")
    # parser.add_argument("--output_folder", required=True, help="Directory where we should save the cropped wings to.")
    
    return parser.parse_args()

def main():
    args = parse_args()

    #use CUDA device(s) if available
    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda:0" if use_cuda else "cpu")
    print("Device: ",device)

    if use_cuda:
        print('__CUDNN VERSION:', torch.backends.cudnn.version())
        print('__Number CUDA Devices:', torch.cuda.device_count())
        print('__CUDA Device Name:',torch.cuda.get_device_name(0))
        print('__CUDA Device Total Memory [GB]:',torch.cuda.get_device_properties(0).total_memory/1e9)

    #declare model type
    acuity_dict = {"no_acuity": "no_acuity", 
                   "male_b":'heliconius_male_behavioral_acuity',
                   "male_m":'heliconius_male_morphological_acuity',
                   "female_b":'heliconius_female_behavioral_acuity',
                   "female_m":'heliconius_female_morphological_acuity',
                   "kingfisher":"kingfisher_acuity"
                   }
    acuity = acuity_dict[args.acuity]

    model_name = None
    if args.model == "regular":
        model_name = 'RegularSpeciesClassification'
    elif args.model == "erato":
        model_name = 'EratoNet'
    elif args.model ==  "melpomene":
        model_name = 'MelpomeneNet'
    elif args.model ==  "mimics":
        model_name = 'MimicsNet'

    erato_net = True if model_name == 'EratoNet' else False
    melpomene_net = True if model_name == 'MelpomeneNet' else False
    mimic_net = True if model_name == 'MimicsNet' else False
    n_classes = 20 if model_name == 'RegularSpeciesClassification' else 10

    #load data in
    dataset_path = get_image_dataset_path(acuity) #path to images with the applied selected acuity
    main = get_split_csvs(acuity, model_name) #path to train/val/test split csvs 

    if mimic_net or model_name == 'RegularSpeciesClassification':
        train_df = pd.read_csv(main + 'train.csv')
        val_df = pd.read_csv(main + 'val.csv')
        test_df = pd.read_csv(main + 'test.csv')

    elif erato_net or melpomene_net:
        train_df = pd.read_csv(main + 'train.csv')
        val_df = pd.read_csv(main + 'val.csv')
        test_df_erato = pd.read_csv(main + 'test_erato.csv')
        test_df_melpomene = pd.read_csv(main + 'test_melpomene.csv')

    #load model in
    model_path = get_logdir(acuity, model_name) + '/checkpoints/classification_ckpt.pth'
    num_classes = n_classes #20 (0r 10 if mimicsnet, eratonet, melpomene net)
    encoder = ResNetEncoder("resnet50", 128)
    model   = EncoderWithHead(encoder,
                            ArcFace(128, n_classes, s=2**0.5*np.log(n_classes - 1), m=0.25))

    model = load_model(model, model_path, device)
    encoder = model.encoder
    device = 'cpu'

    print('Model Ckpt:', model_path)
    print('Num Classes: ', num_classes)

    #get embedding directories to store results in
    save_embeddings_dir = get_embedding_paths(acuity, model_name)
    save_embeddings_dir_all = save_embeddings_dir['all'] + '_GIS' #we're just going to get embeddings of train,val,test splits all in one go

    if erato_net or melpomene_net:
        save_embeddings_dir_test_erato = save_embeddings_dir['test_erato'] + '_GIS'
        save_embeddings_dir_test_melpomene = save_embeddings_dir['test_melpomene'] + '_GIS'
    else:
        save_embeddings_dir_test = save_embeddings_dir['test'] + '_GIS'
    
    print('Getting embeddings...')
    if erato_net or melpomene_net:
        df = pd.concat([train_df, val_df, test_df_erato, test_df_melpomene])
    else:
        df = pd.concat([train_df, val_df, test_df])
    all_embeddings, all_img_paths = predict_embeddings(df, model.encoder, device)
    save_embeddings([all_embeddings], [all_img_paths], save_embeddings_dir_all)

    return

if __name__ == "__main__":
    main()