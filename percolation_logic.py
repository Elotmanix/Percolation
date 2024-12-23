import numpy as np
import cv2
import os
from datetime import datetime
import random

class DisjointSet:
    def __init__(self, n):
        self.disjoint_set = [-1] * n

    def find(self, item):
        if self.disjoint_set[item] < 0:
            return item
        else:
            root = self.find(self.disjoint_set[item])
            self.disjoint_set[item] = root
            return root

    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)
        if root1 == root2:
            return False

        height1 = -self.disjoint_set[root1]
        height2 = -self.disjoint_set[root2]

        if height1 > height2:
            self.disjoint_set[root2] = root1
        elif height1 < height2:
            self.disjoint_set[root1] = root2
        else:
            self.disjoint_set[root1] = root2
            self.disjoint_set[root2] -= 1

        return True

def generate_percolation_clusters(size_x, size_y, p):
    disjoint_set = DisjointSet(size_x * size_y)
    for y in range(size_y):
        for x in range(size_x):
            # Check the left neighbor and connect with probability p
            if x > 0 and random.random() <= p:
                disjoint_set.union(y * size_x + (x - 1), y * size_x + x)
            # Check the upper neighbor and connect with probability p
            if y > 0 and random.random() <= p:
                disjoint_set.union((y - 1) * size_x + x, y * size_x + x)
    return disjoint_set

def generate_rgb():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (int(r), int(g), int(b))

def visualize_clusters(size_x, size_y, disjoint_set):
    grid = np.zeros((size_y, size_x, 3), dtype=np.uint8)
    cluster_colors = {}

    def get_cluster_color(cell_index):
        root = disjoint_set.find(cell_index)
        if root not in cluster_colors:
            cluster_colors[root] = generate_rgb()
        return cluster_colors[root]

    for y in range(size_y):
        for x in range(size_x):
            if random.random() <= 0.5: # Simulate site occupancy for visualization
                grid[y, x] = get_cluster_color(y * size_x + x)
            else:
                grid[y, x] = [255, 255, 255] # Empty sites are white
    return grid

def save_network_image(image, filename="percolation_network.png"):
    filepath = os.path.join("static", "images", filename)
    cv2.imwrite(filepath, image)
    return filepath