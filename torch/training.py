import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Import data generator and Model
from data_generator import generated_labeled_training_data
from model import ChangeClassifier

def train_model():
    # 1. Generate synthetic dataset
    X, y = generated_labeled_training_data(num_samples=999)

    # 2. split into train(80%) and test(20%)
    train_size = int(0.8 * len(X))
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

    # 3. Create DataLoaders (batches data for efficient training)
    train_dataset = TensorDataset(X_train, y_train)
    test_dataset = TensorDataset(X_test, y_test)

    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # 4. Instantiate the model, loss function and optimizer
    model = ChangeClassifier()

    # Define the loss function
    criterion = nn.CrossEntropyLoss() 

    # Define the optimizer
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # 5. training loop
    num_epochs = 200
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0

        for batch_X, batch_y in train_loader:
            # Zero the gradients (Pytorch accumulates gradients by default)
            optimizer.zero_grad()
            # forward pass: get predictions
            outputs = model(batch_X)
            # calculate loss
            loss = criterion(outputs, batch_y)
            #backward pass: compute gradients
            loss.backward()
            # update weights
            optimizer.step()

            running_loss += loss.item()

        if (epoch + 1) % 10 == 0:
            avg_loss = running_loss / len(train_loader)
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")

    # 6. Evaluate on test set
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for batch_X, batch_y in test_loader:
            outputs = model(batch_X)
            _, predicted = torch.max(outputs.data, 1)
            total += batch_y.size(0)
            correct += (predicted == batch_y).sum().item()
    
    accuracy = 100 * correct / total
    print(f"\nTest Accuracy: {accuracy:.2f}%")

    torch.save(model.state_dict(), 'change_classifier.pth')
    print("Model weight saved to 'change_classifier.pth'")
    return model

if __name__ == "__main__":
    train_model = train_model()

