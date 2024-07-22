import cv2
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader, SubsetRandomSampler
import albumentations as albu
from albumentations.pytorch.transforms import ToTensorV2

class ImagesDataset(Dataset):
    def __init__(self, files, targets=None, transforms=None):
        self.files = files
        self.targets = targets
        self.transforms = transforms
    
    def __filenames__(self):
        return self.files

    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, index):
        file = self.files[index]
        img = read_image(str(file))
        
        if self.transforms is not None:
            img = self.transforms(image=img)["image"]

        if self.targets is None:
            return img
        
        target = self.targets[index]
        
        return img, target

def read_image(file):
    img = cv2.imread(str(file))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def read_sized_image(path, size=(16, 16)):
    img = read_image(path)
    img = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)
    return img

def get_transforms(dataset: str):
    """Get transforms depends from dataset.

    Args:
        dataset (str): dataset type (train or valid)

    Returns:
        dataset transforms
    """

    if dataset.lower() == "train":
        return albu.Compose([
            albu.Resize(256, 256),
            albu.RandomCrop(224, 224),
            albu.HorizontalFlip(),
            albu.Normalize(),
            ToTensorV2()
        ])
    else:
        return albu.Compose([
            albu.Resize(224, 224),
            albu.Normalize(),
            ToTensorV2()
        ])

def get_loader(stage: str, images, targets, batch_size: int = 32, num_workers: int = 1):
    """Builds data loaders for a stage (train/test/val).

    Args:
        stage: stage name (one of: 'train', 'test', or 'valid')
        batch_size: number of samples to load at a given time

    Returns:
        DataLoader for given stage
    """
    stage_dataset = ImagesDataset(images, targets, get_transforms(stage))

    # drop_last_decision = True if stage == 'train' else False
    #drop_last parameter is only useful in multiprocessing to avoid duplicating data on diff workers
    stage_dataloader = DataLoader(
        stage_dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle = False if stage=='test' else True,
        drop_last=False
        # sampler=SubsetRandomSampler(train_idx)
        # drop_last=drop_last_decision, #included this to fix the test loader (was not loading the last batch), but ran fine with True on train and val
    )

    return stage_dataset, stage_dataloader