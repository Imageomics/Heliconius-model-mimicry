import torch
import torch.nn as nn

def get_accuracy(model, test_dataloader, split, device):
    # Switch model to evaluation mode
    model = model.eval()

    correct = 0
    total = 0

    all_predicted = []
    all_labels = []

    # No gradient is needed for evaluation, which saves memory and computations
    with torch.no_grad():
        for data in test_dataloader:
            inputs, labels = data  # Adjust these based on your dataset structure
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs, labels)  # Get model predictions
            
            print(outputs.shape)

            #just using total to print shapes once
            # if total == 0:
            #     print(f"Input shape: {inputs.shape}")
            #     print(f"Labels shape: {labels.shape}")
            #     print(f"Outputs shape: {outputs.shape}")

            # The class with the highest energy is what we choose as prediction
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            all_predicted += [p.item() for p in predicted]
            all_labels += [l.item() for l in labels]

    accuracy = correct / total
    print(f'Accuracy of the model on the test ({split}) images: {accuracy}')

    return accuracy, all_predicted, all_labels