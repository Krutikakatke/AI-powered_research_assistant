from sklearn.cluster import KMeans
import numpy as np


def cluster_papers(tfidf_matrix, num_clusters=3):
    """
    Cluster research papers into topics using KMeans

    tfidf_matrix: TF-IDF feature matrix
    num_clusters: number of topics
    """

    kmeans = KMeans(
        n_clusters=num_clusters,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(tfidf_matrix)

    return labels, kmeans