import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

comimic_dict = {"Heliconius melpomene ssp. malleti": "Heliconius erato ssp. lativitta",
                "Heliconius melpomene ssp. melpomene": "Heliconius erato ssp. hydara", 
                "Heliconius melpomene ssp. plesseni": "Heliconius erato ssp. notabilis",
                "Heliconius melpomene ssp. vulcanus": "Heliconius erato ssp. venus",
                "Heliconius melpomene ssp. rosina": "Heliconius erato ssp. petiverana",
                "Heliconius melpomene ssp. cythera": "Heliconius erato ssp. cyrbia", 
                "Heliconius melpomene ssp. nanna": "Heliconius erato ssp. phyllis",
                "Heliconius melpomene ssp. bellula": "Heliconius erato ssp. dignus",
                "Heliconius melpomene ssp. ecuadorensis": "Heliconius erato ssp. etylus", 
                "Heliconius melpomene ssp. meriana": "Heliconius erato ssp. amalfreda"}

#add erato --> melpomene mimic mappings
inv_comimic_dict = {v:k for k,v in comimic_dict.items()}
comimic_dict.update(inv_comimic_dict)

melpomene_list = list(comimic_dict.keys())  
erato_list = list(comimic_dict.values())

# def get_euclidean_distance(A, B):
#     '''Use matrix operations to compute euclidean distance between two matrices.
#        source: https://medium.com/swlh/euclidean-distance-matrix-4c3e1378d87f
#     '''
#     p1 = np.sum(A**2, axis=1)[:, np.newaxis]
#     p2 = np.sum(B**2, axis=1)
#     p3 = -2 * np.dot(A, B.T)
#     distances = np.round(np.sqrt(p1+p2+p3), 5)
#     return distances

def get_euclidean_distance(A, B):
    # Compute distances between A and B
    dot_products = np.dot(A, B.T)  # Shape (m, n)
    norms1_squared = np.sum(A**2, axis=1, keepdims=True)  # Shape (m, 1)
    norms2_squared = np.sum(B**2, axis=1, keepdims=True)  # Shape (n, 1)
    distances_squared = np.maximum(norms1_squared - 2 * dot_products + norms2_squared.T, 0.0)  # Shape (m, n)
    distances = np.sqrt(distances_squared)  # Shape (m, n)
    return distances


#get pairwise embedding distances for embeddings belonging to the same species class (intra-species)
# def get_identity_old(species_embeddings, species_list=None):
#     distances = []
#     if not species_list:
#         species_list = species_embeddings.keys()
#     for ss in species_list:
#         try:
#             if ss in species_embeddings:
#                 embeddings = species_embeddings[ss] #a list of embeddings
#                 for i in range(len(embeddings)):
#                     for j in range(i+1, len(embeddings)):
#                         dist = np.linalg.norm(embeddings[i].astype("float") - embeddings[j].astype("float"))
#                         distances.append(dist)
#         except KeyError:
#             continue
#     return distances

#get pairwise embedding distances for embeddings belonging to the same species class (intra-species)
def get_identity(species_embeddings, species_list=None):
    distances = []
    if not species_list:
        species_list = species_embeddings.keys()
    for ss in species_list:
        try:
            if ss in species_embeddings:
                embeddings = species_embeddings[ss] #a list of embeddings
                embeddings = np.asarray(embeddings).astype("float") #convert to numpy float array
                ss_distances = get_euclidean_distance(embeddings, embeddings) #use matrix operations to get euclidean distance (0 when distance is from itself to itself)
                ss_distances = ss_distances[np.triu_indices(ss_distances.shape[0], k=1)] #only keep upper triangle to remove repetitive entries
                distances += list(ss_distances)
        except KeyError:
            print(f'{ss} does not have embeddings.')
            continue
    return distances
    

#get pairwise embeddings distances for embeddings belonging to mimic species classes
def get_comimic(species_embeddings): 
    distances = []
    for ss in species_embeddings:
        try:
            embeddings = np.asarray(species_embeddings[ss]).astype("float")
            comimic_embeddings = np.asarray(species_embeddings[comimic_dict[ss]]).astype("float")
            ss_distances = get_euclidean_distance(embeddings, comimic_embeddings) #use matrix operations to get euclidean distance (0 when distance is from itself to itself)
            ss_distances = ss_distances.flatten() #flatten distances into a 1D array
            distances += list(ss_distances)
            # for i in range(len(embeddings)):
            #     for j in range(len(comimic_embeddings)):
            #         dist = np.linalg.norm(embeddings[i].astype("float") - comimic_embeddings[j].astype("float"))
            #         distances.append(dist)
        except KeyError:
            print(f'{ss} or {comimic_dict[ss]} does not have embeddings.')
            continue
    return distances


# compute pairwise embedding distances between subspecies1 and subspecies2 where
# subspecies1 != subspecies2 AND subspecies1 != mimic of subspecies2
def get_other(species_embeddings, species_list=None):
    distances = []
    for ss in species_list: 
        try:
            embeddings = species_embeddings[ss]
            other_embeddings = []

            # store all embeddings belonging to "other" class (not itself and not comimic)
            for mm in species_list:
                if mm != ss and mm != comimic_dict[ss] and mm in species_embeddings:
                    other_embeddings += species_embeddings[mm] 

            # compute pairwise euclidean distance between embeddings
            embeddings = np.asarray(embeddings).astype("float")
            other_embeddings = np.asarray(other_embeddings).astype("float")
            other_distances = get_euclidean_distance(embeddings, other_embeddings) 
            other_distances = other_distances.flatten() 
            distances += list(other_distances)
            # for i in range(len(embeddings)):
            #     for j in range(len(other_embeddings)): 
            #         dist = np.linalg.norm(embeddings[i].astype("float") - other_embeddings[j].astype("float"))
            #         distances.append(dist)
        except KeyError:
            print(f'{ss} or {mm} does not have embeddings.')
            continue
    return distances


# def get_boxplot_separate(net, data, labels, subspecies, ax=None, negative=False, correct_only=False) : 
def get_boxplot_separate(species_embeddings, erato_list, melpomene_list, acuity, ax=None, negative=False, correct_only=False):
    #get intra-species embedding distance boxplots for erato and melpomene
    identity_distances_erato = get_identity(species_embeddings, erato_list)
    identity_distances_melpomene = get_identity(species_embeddings, melpomene_list)

    #get embedding distance boxplot for comimic species
    comimic_distances = get_comimic(species_embeddings)

    #get inter-species embedding distance boxplots for erato and melpomene
    other_distances_erato = get_other(species_embeddings, erato_list) #distance from erato_ssp_x to all other erato ssp
    other_distances_melpomene = get_other(species_embeddings, melpomene_list) #distance from melpomene_ssp_x to all other melpomene ssp

    if not ax:
        fig, ax = plt.subplots(figsize=(8, 6))

    boxplot_dict = ax.boxplot([identity_distances_erato, identity_distances_melpomene, comimic_distances, other_distances_erato, other_distances_melpomene], sym='')
    ax.set_xticklabels(['identity\nerato', 'identity\nmelpomene', 'mimic', 'other\nerato', 'other\nmelpomene'], fontsize=20)
    ax.set_ylim([0, 2.0])

    df = get_box_plot_data(['identity erato', 'identity melpomene', 'mimic', 'other erato', 'other melpomene'], boxplot_dict)
    df['acuity'] = [acuity] * 5
    return df #, identity_distances_erato, identity_distances_melpomene, comimic_distances, other_distances_erato, other_distances_melpomene

def get_box_plot_data(labels, bp):
    rows_list = []

    for i in range(len(labels)):
        dict1 = {}
        dict1['label'] = labels[i]
        dict1['lower_whisker'] = bp['whiskers'][i*2].get_ydata()[1]
        dict1['lower_quartile'] = bp['boxes'][i].get_ydata()[1]
        dict1['median'] = bp['medians'][i].get_ydata()[1]
        dict1['upper_quartile'] = bp['boxes'][i].get_ydata()[2]
        dict1['upper_whisker'] = bp['whiskers'][(i*2)+1].get_ydata()[1]
        rows_list.append(dict1)

    return pd.DataFrame(rows_list)