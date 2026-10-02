import numpy as np
import csv

def generate_test_data():
    """
    Create realistic synthetic LiDAR data:
    - Structured grid of points (not random)
    - Corresponding points at same X,Y
    - Only 5 points with large Z changes
    - Small Z noise on all other points
    """
    # 1. Create a 224x224 grid of points (50,176 total)
    x = np.linspace(0, 1, 224)
    y = np.linspace(0, 1, 224)
    xx, yy = np.meshgrid(x, y)
    
    # 2. Create base Z values (flat terrain at Z=0)
    zz = np.zeros_like(xx)
    
    # 3. Flatten into Nx3 array
    points_a = np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()])
    
    # 4. Copy to create Scan B
    points_b = points_a.copy()
    
    # 5. Add small noise to all Z values (simulating sensor noise)
    rng = np.random.default_rng(seed=42)
    points_b[:, 2] += rng.normal(0, 0.05, size=len(points_b))
    
    # 6. Modify 5 specific points by adding 3.0m
    points_b[0, 2] += 3.0
    points_b[1000, 2] += 3.0
    points_b[5000, 2] += 3.0
    points_b[10000, 2] += 3.0
    points_b[25000, 2] += 3.0
    
    return points_a, points_b

def save_to_csv(points, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(points)
        return

# main
points1, points2 = generate_test_data()

save_to_csv(points1, "p1.csv")
save_to_csv(points2, "p2.csv")



    

    

