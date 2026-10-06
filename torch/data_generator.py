import numpy as np
import torch

def generated_labeled_training_data(num_samples=1000):
    # Generate synthetic features for change classification
    """
    returns: X: Pytorch tensor of shape (num_samples, 3) containing [z_diff, local_density, z_variance]
             Y: Pytorch tensor of shape (num_samples) containing integer labels (0, 1 or 2)
    """
    rng = np.random.default_rng(seed=42)

    samples_per_class = num_samples // 3

    # Sensor Noise
    # small Z difference, random density, low variance
    noise_z_diff = rng.uniform(2.0, 15.0, samples_per_class)
    noise_density = rng.uniform(5, 20, samples_per_class)
    noise_variance = rng.uniform(0.01, 0.1, samples_per_class)
    labels_0 = np.zeros(samples_per_class, dtype=np.int64)

    # Tree Fall
    # Large negative Z difference (tree is gone), HIGH density (scattered branches), High variance
    tree_z_diff = rng.uniform(2.0, 15.0, samples_per_class)
    tree_density = rng.uniform(50, 200, samples_per_class)
    tree_variance = rng.uniform(1.0, 5.0, samples_per_class)
    labels_1 = np.ones(samples_per_class, dtype=np.int64)

    # New Structure (e.g, building, tower)
    # large positive Z difference, LOW/MEDIUM density (flat roof/walls), Low variance
    struct_z_diff = rng.uniform(2.0, 10.0, samples_per_class)
    struct_density = rng.uniform(10, 40, samples_per_class)
    struct_variance = rng.uniform(0.1, 0.5, samples_per_class)
    labels_2 = np.full(samples_per_class, 2, dtype=np.int64)

    # 1. Concatenate all features into a single NumPy array
    # combine z_diff, density, and variance arrays vertically
    # combine the label arrays vertically
    noise_features = np.column_stack([noise_z_diff, noise_density, noise_variance])
    tree_features = np.column_stack([tree_z_diff, tree_density, tree_variance])
    structure_features = np.column_stack([struct_z_diff, struct_density, struct_variance])

    all_labels = np.concatenate([labels_0, labels_1, labels_2])

    all_features = np.vstack([noise_features, tree_features, structure_features])

    # 2. Shuffle the data so the model doesnt learn the order (all 0s then all 1s etc)
    # Use rng.permutation to shuffle the rows of your combined features and labels together
    shuffle_idx = rng.permutation(len(all_labels))
    all_features = all_features[shuffle_idx]
    all_labels = all_labels[shuffle_idx]
    # 3. Convert to pytorch sensors
    X_tensor = torch.tensor(all_features, dtype=torch.float32)
    y_tensor = torch.tensor(all_labels, dtype=torch.long)

    return X_tensor, y_tensor
    

if __name__ == "__main__":
    X, y = generated_labeled_training_data(1000)
    print(f"Features shape: {X.shape}") # Should be torch.Size([1000, 3])
    print(f"Labels shape: {y.shape}")   # Should be torch.Size([1000])
    print(f"First 5 labels: {y[:5]}")
    print(f"Label dtype: {y.dtype}")
