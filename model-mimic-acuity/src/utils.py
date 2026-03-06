import csv
import torch
import numpy as np

def load_model(model, model_path, device):
    model_dict = model.state_dict()
    #load the pretrained dict with the specified map_location
    pretrained_dict = torch.load(model_path, map_location=device)
    #filter out unnecessary keys
    pretrained_dict = {k: v for k, v in pretrained_dict.items() if k in model_dict}
    #overwrite entries in the existing state dict
    model_dict.update(pretrained_dict)
    #load the new state dict
    model.load_state_dict(model_dict)
    return model

def load_tsv(path):
    content = []
    with open(path) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        for line in tsv_file:
            content.append(line)
    content = np.array(content)
    return content