import pandas as pd
import os
import shutil
import cv2
import argparse

from dir_paths.dataset_paths import get_image_dataset_path
from dir_paths.train_val_test_paths import get_split_csvs

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

def copy_images(df, dir, label2index):
    for p in df['path']:
        species = label2index[p.split('/')[7]]
        img_name = p.split('/')[-1]
        #copy image into new intr dataset path
        os.makedirs(f'{dir}/{species}', exist_ok=True)
        shutil.copy(p, f'{dir}/{species}/{img_name}')

    return
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--acuity", required=True, help="no_acuity, male_b, female_b, male_m, female_m, kingfisher")
    parser.add_argument("--model", required=True, help="regular, erato, melpomene, mimics, binary") #binary refers to malleti_lativitta
    parser.add_argument("--high_res", default=False, action="store_true", help="Used to load original high resolution images")
    return parser.parse_args()

def main():
    #select acuity dataset
    args=parse_args()

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
    elif args.model == "binary":
        model_name = "MalletiLativitta"

    erato_net = True if model_name == 'EratoNet' else False
    melpomene_net = True if model_name == 'MelpomeneNet' else False
    mimic_net = True if model_name == 'MimicsNet' else False

    if model_name == 'RegularSpeciesClassification':
        n_classes = 20
    elif model_name == "MalletiLativitta":
        n_classes = 2
    else:
        n_classes = 10

    #load in train, val, and test csvs
    dataset_path = get_image_dataset_path(acuity, args.high_res) #path to images with the applied selected acuity
    main = get_split_csvs(acuity, model_name, args.high_res) #path to train/val/test split csvs 

    print('Dataset path: ', dataset_path)
    print('main: ', main)

    if mimic_net or model_name == 'RegularSpeciesClassification' or model_name == 'MalletiLativitta':
        train_df = pd.read_csv(main + 'train.csv')
        val_df = pd.read_csv(main + 'val.csv')
        test_df = pd.read_csv(main + 'test.csv')

    elif erato_net or melpomene_net:
        train_df = pd.read_csv(main + 'train.csv')
        val_df = pd.read_csv(main + 'val.csv')
        test_df_erato = pd.read_csv(main + 'test_erato.csv')
        test_df_melpomene = pd.read_csv(main + 'test_melpomene.csv')

    #create train, val, and test subfolders
    if args.model == 'binary':
        intr_dataset = '/fs/ess/PAS2136/Butterfly/Model_Mimic/INTR_Datasets_Binary_Classification' + '/' + dataset_path.split('/')[-2]
    else:
        intr_dataset = '/fs/ess/PAS2136/Butterfly/Model_Mimic/INTR_Datasets' + '/' + dataset_path.split('/')[-2]
    train_dir = intr_dataset+'/train'
    val_dir = intr_dataset+'/val'
    test_dir = intr_dataset+'/test'

    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    #copy images into respective split folder
    print("creating dataset in INTR format...")
    copy_images(train_df, train_dir, species2index)
    copy_images(val_df, val_dir, species2index)
    copy_images(test_df, test_dir, species2index)

    labels = pd.DataFrame({'species': list(species2index.keys()),
                           'index': list(species2index.values())})

    labels.to_csv(f'{intr_dataset}/labels_to_index.csv', index=False)
    return

if __name__ == "__main__":
    main()