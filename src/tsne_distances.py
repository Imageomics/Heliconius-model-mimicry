from sklearn.manifold import TSNE
import pandas as pd
import numpy as np
import argparse
import os

from dir_paths.embedding_paths import get_embedding_paths
from utils import load_tsv 
from dir_paths.tsne_distances_paths import get_tsne_distance_path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--acuity", required=True, help="no_acuity, male_b, female_b, male_m, female_m, kingfisher")
    parser.add_argument("--model", required=True, help="regular, erato, melpomene, mimics")
    parser.add_argument("--tsne_perplexity", required=False, default=5, help="perplexity parameter for tSNE. Default val is 5")

    return parser.parse_args()

def main():
    args = parse_args()
    
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

    #load embeddings and their labels
    save_embeddings_dir = get_embedding_paths(acuity, model_name)
    save_embeddings_dir_all = save_embeddings_dir['all'] + '_GIS'
    tensors_all = save_embeddings_dir_all + '/embeddings/00000/default/tensors.tsv'
    metadata_all = save_embeddings_dir_all + '/embeddings/00000/default/metadata.tsv'

    print('Loading embeddings...')
    all_embeddings = load_tsv(tensors_all).astype('float32')
    all_labels = load_tsv(metadata_all)
    all_labels = np.concatenate(all_labels)
    print(all_embeddings.shape)

    #generate tsne
    species_labels = [p.split('/')[7] for p in all_labels]
    img_names = [p.split('/')[-1] for p in all_labels]

    #get tsne embeddings - reduce from 128dim to 2dim
    print(f'Getting tSNE with p={args.tsne_perplexity} for embeddings...')
    tsne = TSNE(n_components=2, perplexity=args.tsne_perplexity).fit_transform(all_embeddings)

    #create a dataframe out of tsne 2d embeddings with their labels
    x = tsne[:, 0]
    y = tsne[:, 1]
    tsne_embeddings_df = pd.DataFrame({"x": x, "y":y, "path": all_labels})

    #create a df enumerating all possible pairs of points 
    #final product should have a total of 3822*3822 = 14607684 columns
    tsne_embeddings_df['key'] = 1
    point_pairs = pd.merge(tsne_embeddings_df, tsne_embeddings_df, on='key', suffixes=('_1', '_2'))
    point_pairs.drop('key', axis=1, inplace=True)

    # calculate euclidean distance b/w all points in the tsne space using matrix ops for efficiency
    # do distances have to be normalized?
    df = tsne_embeddings_df[['x', 'y']]
    points = df.to_numpy()
    
    print('calculating euclidean distances b/w all tsne point pairs...')
    diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    dist_sq = np.sum(diff**2, axis=-1)
    euclidean_distances = np.sqrt(dist_sq)  #(3822, 3822)
    euclidean_distances_flat = np.concatenate(euclidean_distances, axis=0) #(14607684,)
    
    #add euclidean distances into dataframe and remove same point pairings
    point_pairs['distance'] = euclidean_distances_flat
    tsne_distances = point_pairs[(point_pairs.x_1 != point_pairs.x_2) & (point_pairs.y_1 != point_pairs.y_2)] #should be 14603862 (3882*3822-3822)
    print('TSNE Distances Shape: ', tsne_distances.shape)

    #save as a csv (img_1, img_2, distance)
    output = get_tsne_distance_path(acuity, model_name)
    os.makedirs(output, exist_ok=True)
    tsne_embeddings_df.to_csv(output+'/tsne_embeddings.csv', index=False)
    tsne_distances.to_csv(output+'/tsne_point_pairs_dist.csv', index=False)

    return


if __name__ == "__main__":
    main()