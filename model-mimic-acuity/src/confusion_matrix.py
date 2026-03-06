import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import seaborn as sns

import os
import numpy as np

def create_confusion_matrix(all_predicted, all_labels, xlist, ylist, save_path, test_set):

    #plot confusion matrix
    fig, ax = plt.subplots(figsize=(25,25)) #24,24

    #create confusion matrix
    cm = confusion_matrix(all_labels, all_predicted)
    cm_sum = cm.sum(axis=1)[:, np.newaxis]
    cm_normalized = cm.astype('float') / np.maximum(cm_sum, 1e-10)
    # cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] #normalize

    sns.heatmap(cm_normalized, 
                annot=True, 
                xticklabels=xlist, #predicted
                yticklabels=ylist #actual
                )

    #label axes
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    ax.set_title(f"{test_set} Test Set - Confusion Matrix for {save_path}", pad=30)

    #save the figure
    os.makedirs(save_path, exist_ok=True)
    plt.savefig(f'{save_path}/confusion_matrix_{test_set}.png', dpi = fig.dpi, bbox_inches='tight')

    plt.show(block=False)
    return


# def get_confusion_matrix(loader, model, save_path, device="cpu", image_size=(24, 24)):
#     model = model.to(device)
#     model = model.eval()
    
#     true_labels = []
#     pred_labels = []
#     accuracy_list = []
    
#     with torch.no_grad():
#         for x, y in loader:
#             x = x.to(device)
#             y = y.to(device)
            
#             #get embeddings
#             # output = F.normalize(model.encoder(x))
#             # output = output.detach().cpu().numpy()
#             # embeddings.append(output)
            
#             #predict labels
#             logits = model(x, y)
#             pred_labels += list(logits.argmax(1).numpy())
            
#             #calculate accuracy
#             accuracy = (logits.argmax(1) == y).float().mean().detach().cpu()
#             accuracy_list.append(accuracy.item())
            
#             #store ground truth labels (labels are integers rep. classes)
#             true_labels += list(y.numpy())
    
#     # convert int categorical labels to species name labels
#     true_labels = [index2species[l] for l in true_labels]
#     pred_labels = [index2species[p] for p in pred_labels]

#     #plot confusion matrix
#     fig, ax = plt.subplots(figsize=image_size) 
    
#     #create confusion matrix
#     cm = confusion_matrix(true_labels, pred_labels)
#     cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] #normalize
#     # sns.heatmap(cm_normalized, 
#     #             annot=True, 
#     #             xticklabels=class_names, 
#     #             yticklabels=class_names)
    
#     sns.heatmap(cm_normalized, 
#                 annot=True, 
#                 xticklabels=melpomene_list+erato_list, 
#                 yticklabels=melpomene_list+erato_list)
    
    
#     #label axes
#     plt.ylabel('Actual')
#     plt.xlabel('Predicted')
#     # plt.savefig(f'{save_path}/confusion_matrix.png', dpi = fig.dpi)
#     plt.show(block=False)
    
#     return accuracy_list, true_labels, pred_labels