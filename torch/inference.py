import torch
import torch.nn as nn
from model import ChangeClassifier

def predict_change(z_diff, local_density, z_variance, model):
    """
    Takes 3 features of a detected change and predicts its class.
    """
    # 1. Convert the single sample into a PyTorch tensor with shape (1,3)
    # The model expects a batch dimension, so we wrap it in an extra list: [[...]]
    features = torch.tensor([[z_diff, local_density, z_variance]], dtype=torch.float32)

    # 2. Set model to evaluation mode (disables dropout, etc.)
    model.eval()

    # 3. Predict (no gradients needed for inference)
    with torch.no_grad():
        # get raw logits
        logits = model(features)

        #convert logits to probabilities using Softmax
        probabilities = torch.softmax(logits, dim=1)

        # Get the index of the highest probability
        predicted_class = torch.argmax(logits, dim=1).item()
        confidence = probabilities[0][predicted_class].item() * 100

    # 4. Map the integer to a human-readable label
    class_names = ["Sensor Noise", "Tree Fall", "New Structure"]

    return class_names[predicted_class], confidence

if __name__ == "__main__":
    # 1. Load the trained model architecture
    model = ChangeClassifier()

    # load the saved weights here:
    model.load_state_dict(torch.load('change_classifier.pth', weights_only=True))

    # 2. Simulate 3 different changes detected by our c++ engine

    #Scenario A: a tiny Z difference, low density, low variance (eg wind moving a branch)
    print("---Scenario A---")
    pred, conf = predict_change(z_diff=0.3, local_density=12.0, z_variance=0.05, model=model)
    print(f"Prediction: {pred} (Confidence: {conf:.2f}%)")

    #Scenario B: A massive Z difference, high density, high variance (e.g, a fallen tree crown)
    print(f"\n--- Scenario B---")
    pred, conf = predict_change(z_diff=8.5, local_density=150.0, z_variance=3.2, model=model)
    print(f"Prediction: {pred} (Confidence: {conf:.2f}%)")

    #Scenario C: A large Z difference, low density, low variance (eg new flat roofed shed)
    print(f"\n--- Scenario C ---")
    pred, conf = predict_change(z_diff=4.0, local_density=25.0, z_variance=0.2, model=model)
    print(f"Prediction: {pred} (Confidence: {conf:.2f}%)")


