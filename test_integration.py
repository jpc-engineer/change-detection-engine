import change_detection as cd

# load data
points_a = cd.load_points_from_csv("Data/p1.csv")
points_b = cd.load_points_from_csv("Data/p2.csv")

print(f"Loaded {len(points_a)} points from A")
print(f"Loaded {len(points_b)} points from B")

changes = cd.detect_changes(points_a, points_b, 0.002, 2.0, 0.1)

print(f"\nFound {len(changes)} significant changes")
for i, pt in enumerate(changes):
    print(f"Change {i+1}: X={pt.x}, Y={pt.y}, Z={pt.z}")
