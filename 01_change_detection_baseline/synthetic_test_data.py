import numpy as np
import csv

def generate_test_data():
    
    # 1. Create a base grid of 500 points with random X,Y,Z values
    # 2. Copy this to create ScanA and ScanB
    rng = np.random.default_rng(seed=42)

    points_a = rng.random((500, 3))
    points_b = points_a.copy()

    x_a = points_a[:, 0]
    y_a = points_a[:, 1]
    z_a = points_a[:, 2]

    x_b = points_b[:, 0]
    y_b = points_b[:, 1]
    z_b = points_b[:, 2]
    # 3. Modify the Z values of some points in ScanB, by adding 3.0metres (tree being removed, or something being added)
    points_b[0:5, 2] += 3.0
    # 4. return both arrays
    return points_a, points_b

def save_to_csv(points, filepath):
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(points)
        return
   

points1, points2 = generate_test_data()


save_to_csv(points1, "p1.csv")
save_to_csv(points2, "p2.csv")


    

    

