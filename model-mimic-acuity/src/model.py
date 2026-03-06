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

class ResNetEncoder(nn.Module):
    def __init__(self, base, ouf_features, bias=True):
        """
        Args:
            base (str): name of resnet to use
            ouf_features (int): number of features to profuce
            bias (bool): use bias term in final linear layer.
                Default is ``True``.
        """
        super().__init__()

        # self.base = vars(resnet)[base](pretrained=True)
        self.base = vars(resnet)[base](weights=ResNet50_Weights.IMAGENET1K_V2)
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.output_filter = self.base.fc.in_features
        self.classifier = nn.Linear(self.output_filter, ouf_features, bias=bias)

    def extract_conv_features(self, x):
        x = self.base.conv1(x)
        x = self.base.bn1(x)
        x = self.base.relu(x)
        x = self.base.maxpool(x)

        x = self.base.layer1(x)
        x = self.base.layer2(x)
        x = self.base.layer3(x)
        x = self.base.layer4(x)

        x = self.avg_pool(x)
        return x

    def forward(self, batch):
        x = self.extract_conv_features(batch)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


class EncoderWithHead(nn.Module):
    def __init__(self, encoder, head):
        """
        Args:
            encoder (nn.Module): encoder network
            head (nn.Module): head layer
        """
        super().__init__()
        self.encoder = encoder
        self.head = head

    def forward(self, images, targets=None) -> torch.tensor:
        features = self.encoder(images) #resnet acts as the feature extractor from our images
        if targets is None:
            return features
        outputs = self.head(features, targets) #ArcFace is the last layer; computes final outputs, which are logits for classification
        return outputs