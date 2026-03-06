import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from tensorboardX import SummaryWriter

from sklearn.model_selection import train_test_split

import albumentations as albu
from albumentations.pytorch.transforms import ToTensorV2

from torchvision.models import resnet, ResNet50_Weights

from tqdm import tqdm 
import torchvision
import torchvision.transforms as T

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from matplotlib import cm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import PIL

import catalyst.dl as dl
from catalyst.contrib.nn import (
    ArcFace,
    CosFace,
    AdaCos,
    SubCenterArcFace,
    CurricularFace,
    ArcMarginProduct,
) 

from src.dataloader import read_sized_image

def predict_embeddings(encoder, dataloader, device: str="cpu"):
    #move encoder to cuda device if available and use for eval only
    encoder = encoder.to(device)
    encoder = encoder.eval()

    #get embeddings on dataset from our model
    embeddings = []
    true_labels = []
    
    with torch.no_grad():
        for x, y in dataloader:
            x = x.to(device)
            
            #predict embeddings using encoder
            output = F.normalize(encoder(x))
            output = output.detach().cpu().numpy()
            embeddings.append(output)
            
            #store the ground truth labels associated with each embedding
            # print(y)
            # print(x)
            true_labels.append(y)
    
    #flatten out lists created per batch
    embeddings = np.concatenate(embeddings)
    true_labels = np.concatenate(true_labels) 

    return embeddings, true_labels

## embeddings preperation logic
def save_embeddings(label_mapper, dataset, dataloader, encoder, directory, device="cpu", image_size=(64, 64)):
    """
    Args:
        label_mapper (dict): dictionary mapping numerical labels to string labels,
        dataset (torch.utils.data.Dataset): images dataset,
        encoder (torch.nn.Module): encoder network
        directory (str): directory where will be stored predictions
        device (str or torch.device): inference device
        image_size (Tuple[int, int]): image size to use
            for plotting in embedding
    """
    if not os.path.isdir(directory):
        os.makedirs(directory)
    
    #predict embeddings
    embeddings, labels = predict_embeddings(encoder, dataloader, device)

    # store embeddings
    writer = SummaryWriter(
        logdir=os.path.join(directory, "embeddings"),
        comment="embeddings"
    )
    small_images = np.stack(
        [read_sized_image(name, image_size) for name in dataset.files],
        axis=0
    )
    small_images = small_images.transpose((0, 3, 1, 2)) / 255.0
    small_images = small_images.astype(np.float32)
    metadata = [label_mapper[l] for l in labels] #convert numerical labels to subspecies string labels formerly (index2species)

    writer.add_embedding(
        embeddings,
        label_img=small_images,
        metadata=metadata
    )
    writer.close()
    
    return embeddings, metadata

# def save_merged_embeddings(train_embeddings, test_embeddings, train_labels, test_labels, directory):
def save_merged_embeddings(embeddings, labels, directory):
    '''function to save train and test embeddings as one cohesive file '''
    # all_embeddings = np.concatenate([train_embeddings, test_embeddings], axis=0)
    # all_labels = np.concatenate([train_labels, test_labels], axis=0)
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