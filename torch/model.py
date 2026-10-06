import torch
import torch.nn as nn

class ChangeClassifier(nn.Module):
    def __init__(self, input_features=3, num_classes=3):
        super(ChangeClassifier, self).__init__()

        #1. first linear layer:
        # maps 3 input features to 16 hidden neurons
        self.fc1 = nn.Linear(in_features=input_features, out_features=16)

        #2. Activation function:
        # Adds non-linearity
        self.relu = nn.ReLU()

        #3. second linear layer: 
        # maps 16 hidden neurons to 3 output classes
        self.fc2 = nn.Linear(in_features=16, out_features=num_classes)

    def forward(self, x):
        # Pass the input 'x' through the first linear layer
        x = self.relu(self.fc1(x))

        # Apply the ReLU activation function
        x = self.relu(x)

        # pass through second linear layer to get final class scores(logits)
        x = self.fc2(x)

        return x
    
# Test model
if __name__ == "__main__":
    # 1. import data generator
    from data_generator import generated_labeled_training_data
    # 2. get small batch of dummy data
    X, y = generated_labeled_training_data(num_samples=999)
    X_batch = X[:5]
    # 3. Intantiate the model
    model = ChangeClassifier()
    print("Model Architecture")
    print(model)

    # 4. dummy forward pass
    output = model(X_batch)

    print(f"\nInput shape: {X_batch.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Raw output scores (logits) for first sample: {output[0]}")



