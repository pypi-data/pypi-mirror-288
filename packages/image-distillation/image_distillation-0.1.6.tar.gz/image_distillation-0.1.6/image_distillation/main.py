import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


class ImageClusterSampler:
    """
    Base class for image clustering and sampling
    
    args:
        X: numpy array of shape (n_samples, height, width, channels)
        y: numpy array of shape (n_samples,)
        n_clusters: number of clusters to form
        n_samples: number of samples to select from each cluster
        
    methods:
        cluster_images: Cluster the images using KMeans and reduce the dimensionality using PCA
        plot_clusters: Plot the clusters in the 2D PCA space
        plot_selected_samples_on_clusters: Plot the selected samples on the clusters in the 2D PCA space
    """

    def __init__(self, X, y, n_clusters, n_samples):
        """
        X: numpy array of shape (n_samples, height, width, channels)
        y: numpy array of shape (n_samples,)
        n_clusters: number of clusters to form
        n_samples: number of samples to select from each cluster
        """

        self.X = X
        self.y = y
        self.n_clusters = n_clusters
        self.n_samples = n_samples
        self.cluster_labels = None
        self.X_pca = None
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.pca = PCA(n_components=2, random_state=42)
    
    def cluster_images(self):
        """
        Cluster the images using KMeans and reduce the dimensionality using PCA
        """
        self.kmeans.fit(self.X.reshape(self.X.shape[0], -1))
        self.cluster_labels = self.kmeans.labels_
        self.X_pca = self.pca.fit_transform(self.X.reshape(self.X.shape[0], -1))

    def plot_clusters(self):
        """
        Plot the clusters in the 2D PCA space
        """

        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f"Cluster {i}")
        plt.title("Clustering of the Dataset")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend()
        plt.show()
    
    def plot_selected_samples_on_clusters(self, selected_samples):
        """
        Plot the selected samples on the clusters in the 2D PCA space

        args:
            selected_samples: list of indices of selected samples
        """

        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f"Cluster {i}", alpha=0.5)
        
        selected_data = self.X_pca[selected_samples]
        plt.scatter(selected_data[:, 0], selected_data[:, 1], color="red", label="Selected Samples", edgecolor="k")
        
        plt.title("Clustering Selected Samples")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend()
        plt.show()


class GridSampler(ImageClusterSampler):
    """
    Class for grid-based sampling of the clusters
    
    methods:
        plot_clusters_with_grids: Plot the clusters with grid lines in the 2D PCA space
        get_grid_sampled_indices: Get the sampled indices from each cluster using grid sampling
        get_selected_samples: Get the selected samples from each cluster using grid sampling
    """
    
    def plot_clusters_with_grids(self):
        """
        Plot the clusters with grid lines in the 2D PCA space
        """

        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f"Cluster {i}", alpha=0.5)
        
        grid_size = int(np.ceil(np.sqrt(self.n_samples)))
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_grid = np.linspace(x_min, x_max, grid_size + 1)
        y_grid = np.linspace(y_min, y_max, grid_size + 1)
        
        for x in x_grid:
            plt.axvline(x=x, color="k", linestyle="--", alpha=0.5)
        for y in y_grid:
            plt.axhline(y=y, color="k", linestyle="--", alpha=0.5)
        
        plt.title("Clustering with Grids")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend()
        plt.show()
    
    def get_grid_sampled_indices(self, cluster_indices, n_samples):
        """
        Get the sampled indices from each cluster using grid sampling

        args:
            cluster_indices: list of indices of samples in the cluster
            n_samples: number of samples to select from each cluster

        returns:
            sampled_indices: list of indices of selected samples
        """

        if len(cluster_indices) <= n_samples:
            return cluster_indices
        
        grid_size = int(np.ceil(np.sqrt(n_samples)))
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_grid = np.linspace(x_min, x_max, grid_size + 1)
        y_grid = np.linspace(y_min, y_max, grid_size + 1)
        
        sampled_indices = []
        for i in range(grid_size):
            for j in range(grid_size):
                x_start, x_end = x_grid[i], x_grid[i + 1]
                y_start, y_end = y_grid[j], y_grid[j + 1]
                
                grid_indices = [
                    idx for idx in cluster_indices 
                    if x_start <= self.X_pca[idx, 0] < x_end and y_start <= self.X_pca[idx, 1] < y_end
                ]
                
                if grid_indices:
                    sampled_indices.append(np.random.choice(grid_indices))

        while len(sampled_indices) < n_samples:
            sampled_indices.append(np.random.choice(cluster_indices))
        
        return sampled_indices[:n_samples]

    def get_selected_samples(self):
        """
        Get the selected samples from each cluster using grid sampling

        returns:
            selected_samples: list of indices of selected samples
        """

        selected_samples = []
        unique_labels = np.unique(self.y)
        for label in unique_labels:
            label_indices = np.where(self.y == label)[0]
            label_cluster_labels = self.cluster_labels[label_indices]
            unique_clusters = np.unique(label_cluster_labels)
            
            for cluster_id in unique_clusters:
                cluster_indices = label_indices[label_cluster_labels == cluster_id]
                selected_indices = self.get_grid_sampled_indices(cluster_indices, self.n_samples)
                selected_samples.extend(selected_indices)
        return selected_samples


class ParallelogramSampler(ImageClusterSampler):
    """
    Class for parallelogram-based sampling of the clusters

    methods:
        get_angle: Get the angle of the optimum parallelogram grid
        get_grid_size: Get the grid size of the optimum parallelogram grid
        plot_clusters_with_parallelograms: Plot the clusters with parallelogram grids in the 2D PCA space
        get_parallelogram_sampled_indices: Get the sampled indices from each cluster using parallelogram sampling
        get_selected_samples: Get the selected samples from each cluster using parallelogram sampling
    """

    def get_angle(self):
        """
        Get the angle of the optimum parallelogram grid
        
        returns:
            angle: angle of the parallelogram grid
        """

        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        x_length = x_max - x_min
        y_length = y_max - y_min
        angle = np.degrees(np.arctan(y_length / x_length))
        return angle
    
    def get_grid_size(self):
        """
        Get the grid size of the optimum parallelogram grid

        returns:
            grid_size: size of the grid
        """

        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        x_length = x_max - x_min
        y_length = y_max - y_min
        grid_size = int(np.ceil(np.sqrt(x_length * y_length)))
        return grid_size

    def plot_clusters_with_parallelograms(self, angle=30, grid_size=10):
        """
        Plot the clusters with parallelogram grids in the 2D PCA space

        args:
            angle: angle of the parallelogram grid
            grid_size: size of the grid
        """

        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f"Cluster {i}", alpha=0.5)
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_length = (x_max - x_min) / grid_size
        dx = x_length * np.cos(np.radians(angle))
        dy = x_length * np.sin(np.radians(angle))
        y_length = dy

        for i in range(grid_size):
            for j in range(grid_size):
                x_start = x_min + i * x_length
                y_start = y_min + j * y_length

                parallelogram = [
                    (x_start, y_start),
                    (x_start + x_length, y_start),
                    (x_start + x_length + dx, y_start + dy),
                    (x_start + dx, y_start + dy)
                ]
                
                parallelogram_x, parallelogram_y = zip(*parallelogram)
                plt.plot(parallelogram_x + (parallelogram_x[0],), parallelogram_y + (parallelogram_y[0],), "k--", alpha=0.5)
        
        plt.title("Clustering with Parallelogram Grids")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend()
        plt.show()
    
    def get_parallelogram_sampled_indices(self, cluster_indices, n_samples, angle=30, grid_size=10):
        """
        Get the sampled indices from each cluster using parallelogram sampling

        args:
            cluster_indices: list of indices of samples in the cluster
            n_samples: number of samples to select from each cluster
            angle: angle of the parallelogram grid
            grid_size: size of the grid

        returns:
            sampled_indices: list of indices of selected samples
        """
        
        if len(cluster_indices) <= n_samples:
            return cluster_indices
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_length = (x_max - x_min) / grid_size
        dx = x_length * np.cos(np.radians(angle))
        dy = x_length * np.sin(np.radians(angle))
        y_length = dy
        
        sampled_indices = []
        
        for i in range(grid_size):
            for j in range(grid_size):
                x_start = x_min + i * x_length
                y_start = y_min + j * y_length

                parallelogram_indices = [
                    idx for idx in cluster_indices 
                    if (self.X_pca[idx, 0] >= x_start and self.X_pca[idx, 0] < x_start + x_length + dx and
                        self.X_pca[idx, 1] >= y_start and self.X_pca[idx, 1] < y_start + y_length and
                        (self.X_pca[idx, 1] - y_start) < dy / dx * (self.X_pca[idx, 0] - x_start + x_length))
                ]
                
                if parallelogram_indices:
                    sampled_indices.append(np.random.choice(parallelogram_indices))

        while len(sampled_indices) < n_samples:
            sampled_indices.append(np.random.choice(cluster_indices))
        
        return sampled_indices[:n_samples]

    def get_selected_samples(self):
        """
        Get the selected samples from each cluster using parallelogram sampling

        returns:
            selected_samples: list of indices of selected samples
        """

        selected_samples = []
        unique_labels = np.unique(self.y)
        for label in unique_labels:
            label_indices = np.where(self.y == label)[0]
            label_cluster_labels = self.cluster_labels[label_indices]
            unique_clusters = np.unique(label_cluster_labels)
            
            for cluster_id in unique_clusters:
                cluster_indices = label_indices[label_cluster_labels == cluster_id]
                selected_indices = self.get_parallelogram_sampled_indices(cluster_indices, self.n_samples)
                selected_samples.extend(selected_indices)
        return selected_samples


class TriangularSampler(ImageClusterSampler):
    """
    Class for triangular-based sampling of the clusters

    methods:
        plot_clusters_with_triangles: Plot the clusters with triangular grids in the 2D PCA space
        get_triangle_sampled_indices: Get the sampled indices from each cluster using triangular sampling
        get_selected_samples: Get the selected samples from each cluster using triangular sampling
        plot_selected_samples_on_clusters: Plot the selected samples on the clusters in the 2D PCA space
    """
    
    def plot_clusters_with_triangles(self, grid_size=10):
        """
        Plot the clusters with triangular grids in the 2D PCA space
        
        args:
            grid_size: size of the grid
        """

        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f"Cluster {i}", alpha=0.5)
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        side_length = (x_max - x_min) / grid_size
        height = np.sqrt(3) / 2 * side_length
        
        for i in range(-1, grid_size + 1):
            for j in range(-1, grid_size + 1):
                x_start = x_min + i * side_length
                y_start = y_min + j * height

                if (i + j) % 2 == 0:
                    triangle = [
                        (x_start, y_start),
                        (x_start + side_length / 2, y_start + height),
                        (x_start - side_length / 2, y_start + height)
                    ]
                else:
                    triangle = [
                        (x_start, y_start),
                        (x_start + side_length, y_start),
                        (x_start + side_length / 2, y_start + height)
                    ]

                triangle_x, triangle_y = zip(*triangle)
                plt.plot(triangle_x + (triangle_x[0],), triangle_y + (triangle_y[0],), "k--", alpha=0.5)
        
        plt.title("Clustering with Triangular Grids")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend()
        plt.show()
    
    def get_triangle_sampled_indices(self, cluster_indices, grid_size=10):
        """
        Get the sampled indices from each cluster using triangular sampling

        args:
            cluster_indices: list of indices of samples in the cluster
            grid_size: size of the grid

        returns:
            sampled_indices: list of indices of selected samples
        """

        if len(cluster_indices) <= self.n_samples:
            return cluster_indices
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        side_length = (x_max - x_min) / grid_size
        height = np.sqrt(3) / 2 * side_length
        
        sampled_indices = []
        
        for i in range(-1, grid_size + 1):
            for j in range(-1, grid_size + 1):
                x_start = x_min + i * side_length
                y_start = y_min + j * height

                if (i + j) % 2 == 0:
                    triangle_indices = [
                        idx for idx in cluster_indices 
                        if self.point_in_triangle(self.X_pca[idx], 
                                                  (x_start, y_start), 
                                                  (x_start + side_length / 2, y_start + height), 
                                                  (x_start - side_length / 2, y_start + height))
                    ]
                else:
                    triangle_indices = [
                        idx for idx in cluster_indices 
                        if self.point_in_triangle(self.X_pca[idx], 
                                                  (x_start, y_start), 
                                                  (x_start + side_length, y_start), 
                                                  (x_start + side_length / 2, y_start + height))
                    ]

                if triangle_indices:
                    sampled_indices.append(np.random.choice(triangle_indices))

        while len(sampled_indices) < self.n_samples:
            sampled_indices.append(np.random.choice(cluster_indices))
        
        return sampled_indices[:self.n_samples]
    
    def point_in_triangle(self, point, v1, v2, v3):
        """
        Check if a point is inside a triangle

        args:
            point: tuple of (x, y) coordinates of the point
            v1: tuple of (x, y) coordinates of the first vertex of the triangle
            v2: tuple of (x, y) coordinates of the second vertex of the triangle
            v3: tuple of (x, y) coordinates of the third vertex of the triangle

        returns:
            bool: True if the point is inside the triangle, False otherwise
        """

        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        b1 = sign(point, v1, v2) < 0.0
        b2 = sign(point, v2, v3) < 0.0
        b3 = sign(point, v3, v1) < 0.0
        
        return ((b1 == b2) & (b2 == b3))

    def get_selected_samples(self):
        """
        Get the selected samples from each cluster using triangular sampling

        returns:
            selected_samples: list of indices of selected samples
        """

        selected_samples = []
        unique_labels = np.unique(self.y)
        for label in unique_labels:
            label_indices = np.where(self.y == label)[0]
            label_cluster_labels = self.cluster_labels[label_indices]
            unique_clusters = np.unique(label_cluster_labels)
            
            for cluster_id in unique_clusters:
                cluster_indices = label_indices[label_cluster_labels == cluster_id]
                selected_indices = self.get_triangle_sampled_indices(cluster_indices, self.n_samples)
                selected_samples.extend(selected_indices)
        return selected_samples

    def plot_selected_samples_on_clusters(self, selected_samples):
        """
        Plot the selected samples on the clusters in the 2D PCA space

        args:
            selected_samples: list of indices of selected samples
        """

        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f"Cluster {i}", alpha=0.5)
        
        selected_data = self.X_pca[selected_samples]
        plt.scatter(selected_data[:, 0], selected_data[:, 1], color="red", label="Selected Samples", edgecolor="k")
        
        plt.title("Clustering with Selected Samples")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend()
        plt.show()


class BrickSampler(ImageClusterSampler):
    """
    Class for brick-based sampling of the clusters

    methods:
        plot_clusters_with_bricks: Plot the clusters with brick grids in the 2D PCA space
        get_brick_sampled_indices: Get the sampled indices from each cluster using brick sampling
        get_selected_samples: Get the selected samples from each cluster using brick sampling
    """
    
    def plot_clusters_with_bricks(self, grid_size=10):
        """
        Plot the clusters with brick grids in the 2D PCA space

        args:
            grid_size: size of the grid
        """

        plt.figure(figsize=(10, 6))
        for i in range(self.n_clusters):
            cluster_data = self.X_pca[self.cluster_labels == i]
            plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f"Cluster {i}", alpha=0.5)
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_grid = np.linspace(x_min, x_max, grid_size + 1)
        y_grid = np.linspace(y_min, y_max, grid_size + 1)
        
        skew_factor = (x_max - x_min) / (grid_size * 2)
        
        for i in range(grid_size):
            for j in range(grid_size):
                x_start, x_end = x_grid[i] + j * skew_factor, x_grid[i + 1] + j * skew_factor
                y_start, y_end = y_grid[j], y_grid[j + 1]
                
                plt.plot([x_start, x_end], [y_start, y_start], "k--", alpha=0.5)
                plt.plot([x_start, x_end], [y_end, y_end], "k--", alpha=0.5)
                plt.plot([x_start, x_start], [y_start, y_end], "k--", alpha=0.5)
                plt.plot([x_end, x_end], [y_start, y_end], "k--", alpha=0.5)
        
        plt.title("Clustering with Brick Grids")
        plt.xlabel("PCA Component 1")
        plt.ylabel("PCA Component 2")
        plt.legend()
        plt.show()
    
    def get_brick_sampled_indices(self, cluster_indices, n_samples, grid_size=10):
        """
        Get the sampled indices from each cluster using brick sampling

        args:
            cluster_indices: list of indices of samples in the cluster
            n_samples: number of samples to select from each cluster
            grid_size: size of the grid

        returns:
            sampled_indices: list of indices of selected samples
        """

        if len(cluster_indices) <= n_samples:
            return cluster_indices
        
        x_min, x_max = np.min(self.X_pca[:, 0]), np.max(self.X_pca[:, 0])
        y_min, y_max = np.min(self.X_pca[:, 1]), np.max(self.X_pca[:, 1])
        
        x_grid = np.linspace(x_min, x_max, grid_size + 1)
        y_grid = np.linspace(y_min, y_max, grid_size + 1)
        
        sampled_indices = []
        skew_factor = (x_max - x_min) / (grid_size * 2)
        
        for i in range(grid_size):
            for j in range(grid_size):
                x_start, x_end = x_grid[i] + j * skew_factor, x_grid[i + 1] + j * skew_factor
                y_start, y_end = y_grid[j], y_grid[j + 1]
                
                grid_indices = [
                    idx for idx in cluster_indices 
                    if x_start <= self.X_pca[idx, 0] < x_end and y_start <= self.X_pca[idx, 1] < y_end
                ]
                
                if grid_indices:
                    sampled_indices.append(np.random.choice(grid_indices))

        while len(sampled_indices) < n_samples:
            sampled_indices.append(np.random.choice(cluster_indices))
        
        return sampled_indices[:n_samples]

    def get_selected_samples(self):
        """
        Get the selected samples from each cluster using brick sampling

        returns:
            selected_samples: list of indices of selected samples
        """
        
        selected_samples = []
        unique_labels = np.unique(self.y)
        for label in unique_labels:
            label_indices = np.where(self.y == label)[0]
            label_cluster_labels = self.cluster_labels[label_indices]
            unique_clusters = np.unique(label_cluster_labels)
            
            for cluster_id in unique_clusters:
                cluster_indices = label_indices[label_cluster_labels == cluster_id]
                selected_indices = self.get_brick_sampled_indices(cluster_indices, self.n_samples)
                selected_samples.extend(selected_indices)
        return selected_samples
