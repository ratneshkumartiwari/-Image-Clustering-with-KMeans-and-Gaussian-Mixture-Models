# -*- coding: utf-8 -*-
"""M23MAC011_task1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wRKRi3rr-iLAE9nM3T5OtM5AtLHku1W1
"""

import numpy as np
import pandas as pd
from numpy.linalg import norm
file = pd.read_csv("mnist_train.csv")

def cosine_distance(vector1, vector2):
    # Compute the dot product of the two vectors
    dot_product = np.dot(vector1, vector2)

    # Calculate the Euclidean norm (L2 norm) of each vector
    norm_vector1 = norm(vector1)
    norm_vector2 = norm(vector2)

    # Calculate the cosine similarity
    cosine_similarity = dot_product / (norm_vector1 * norm_vector2)

    # Calculate the cosine distance (1 - cosine_similarity)
    cosine_distance = 1 - cosine_similarity

    return cosine_distance

def k_means_clustering(X, K, max_iterations=1000):
    # Initialize centroids randomly
    # here we have chose any random point from dataset itself as the initial point.
    #This is done because if initial point will be in same locality, it will converge faster.
    centroids = X[np.random.choice(X.shape[0], K, replace=False)]


    for _ in range(max_iterations):
        # Assign each data point to the nearest centroid using cosine distance
        distances = np.array([[cosine_distance(x, c) for c in centroids] for x in X])
        labels = np.argmin(distances, axis=1)

        # Update centroids based on the mean of data points in each cluster
        new_centroids = np.array([X[labels == k].mean(axis=0) for k in range(K)])

        # Check for convergence
        if np.all(centroids == new_centroids):
            break

        centroids = new_centroids

    return centroids, labels



# Separate features and targets
X = file.drop('label', axis=1)
y = file['label']
X = np.array(X)

# scalling the data
X = X/255.0

#performing k means using the value of k as 10, 7, 4
centroids1, labels1 = k_means_clustering(X, 10)
centroids2, labels2 = k_means_clustering(X, 7)
centroids3, labels3 = k_means_clustering(X, 4)

#writing the function to visualize
import matplotlib.pyplot as plt
def show_image(num, labels):
    # Create a dictionary to store images for each cluster
    cluster_images = {}
    for cluster in range(num):
        cluster_images[cluster] = []

    # Collect images for each cluster
    for i in range(len(X)):
        cluster = labels[i]
        cluster_images[cluster].append(X[i].reshape(28, 28))

    # Visualize a sample image from each cluster
    # plt.figure(figsize=(15, 8))
    plt.suptitle("Sample Images from K-means Clusters (Cosine Similarity)")
    for cluster in range(num):
        plt.suptitle(f'Samples of Cluster {cluster+1}')
        for i in range(10):
            plt.subplot(3, 5, i + 1)
            sample_image = cluster_images[cluster][i]
            plt.imshow(sample_image, cmap='gray')

            plt.axis('off')

        plt.show()

#When total number of cluster is 10
show_image(10, labels1)

#When total number of cluster is 7
show_image(7, labels2)

#When total number of cluster is 4
show_image(4, labels3)

#Try to write a python function which finds optimal number of clusters for this dataset.

#This can be achieved by using elbow method. We will check the inertia for each value of k and plot it.

# Function to calculate the Euclidean distance between two points
def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

# Function to calculate the inertia for a given set of centroids
def inertia(data, centroids, labels):
    inertia = 0
    for i, centroid in enumerate(centroids):
        cluster_points = data[labels == i]
        cluster_inertia = np.sum([euclidean_distance(centroid, point) ** 2 for point in cluster_points])
        inertia += cluster_inertia
    return inertia


distortions = []
for k in range(1, 20):
    centroids, labels = k_means_clustering(X, k)

    distortions.append(inertia(X, centroids, labels))

# Plot the Elbow Method graph
plt.figure(figsize=(8, 6))
plt.plot(range(1, 20), distortions, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Distortion (Inertia)')
plt.show()


#IN the plot, the value of k, for which the curve started to flatten
 #(ie, doen not decrease further significantly) will be the elbow point and it will be the optimal value of k