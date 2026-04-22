import numpy as np
import random
import time

# ─── City Coordinates (from cities.csv / cities.pdf) ───
cities = np.array([
    [0.046, 4.006], [-0.454, -0.706], [0.181, 5.769], [0.739, 4.741],
    [-0.11, 5.179], [-0.235, 0.271], [-0.265, 5.257], [0.148, 5.131],
    [0.458, 5.164], [5.104, 4.02], [-0.117, -0.117], [0.034, -0.712],
    [-0.351, 4.836], [5.515, 5.466], [-0.301, 0.926], [5.411, 4.39],
    [-0.196, 4.268], [5.166, 5.488], [0.181, 4.677], [4.58, 4.845],
    [0.121, -0.957], [-0.272, 0.055], [0.79, 0.384], [-0.506, 0.157],
    [0.049, 5.484], [0.003, 4.883], [-0.232, -0.233], [-0.3, -0.146],
    [-0.862, -0.281], [4.76, 4.907], [5.406, 5.678], [4.964, 5.502],
    [5.172, 4.118], [-0.018, 5.782], [-1.31, 5.411], [4.942, 4.849],
    [-0.007, -0.529], [5.369, 5.086], [4.261, 4.64], [-0.404, 4.749],
    [4.447, 4.402], [0.733, -0.113], [4.336, 5.098], [5.162, 4.807],
    [4.662, 5.306], [0.044, 4.85], [4.77, 5.529], [-0.575, 0.188],
    [0.248, -0.069], [0.324, 0.762]
])

K = 3  # number of airports/clusters
N = len(cities)


def assign_clusters(data, centers):
    """Assign each city to its nearest cluster center."""
    labels = np.zeros(len(data), dtype=int)
    for i, point in enumerate(data):
        dists = np.sum((centers - point) ** 2, axis=1)
        labels[i] = np.argmin(dists)
    return labels


def compute_ssd(data, centers, labels):
    """Compute sum of squared distances for each cluster and total."""
    cluster_ssd = np.zeros(len(centers))
    for i, point in enumerate(data):
        cluster_ssd[labels[i]] += np.sum((point - centers[labels[i]]) ** 2)
    return cluster_ssd, np.sum(cluster_ssd)


def initialize_centers(data, k, seed=42):
    """K-means++ initialization for better starting centers."""
    rng = np.random.RandomState(seed)
    centers = [data[rng.randint(len(data))]]
    for _ in range(1, k):
        dists = np.array([min(np.sum((x - c) ** 2) for c in centers) for x in data])
        probs = dists / dists.sum()
        idx = rng.choice(len(data), p=probs)
        centers.append(data[idx])
    return np.array(centers, dtype=float)


# ═══════════════════════════════════════════════════════════════
# Method (a): Gradient Descent (First Order Derivatives)
# ═══════════════════════════════════════════════════════════════

def gradient_descent_kmeans(data, k, lr=0.01, max_iter=500, tol=1e-8, seed=42):
    """
    K-Means optimization using Gradient Descent.

    The objective function is:
        J = Σᵢ ||xᵢ - μ_c(i)||²
    where c(i) is the cluster assignment of point i.

    Gradient w.r.t. center μⱼ:
        ∂J/∂μⱼ = -2 Σ_{i: c(i)=j} (xᵢ - μⱼ)

    Update rule:
        μⱼ ← μⱼ - lr × ∂J/∂μⱼ
    """
    centers = initialize_centers(data, k, seed)

    prev_ssd = float('inf')

    for iteration in range(1, max_iter + 1):
        # step 1: assign clusters
        labels = assign_clusters(data, centers)

        # step 2: compute gradients
        gradients = np.zeros_like(centers)
        for j in range(k):
            mask = labels == j
            if np.any(mask):
                cluster_points = data[mask]
                # gradient = -2 * sum(x_i - mu_j) = 2 * (n_j * mu_j - sum(x_i))
                gradients[j] = -2 * np.sum(cluster_points - centers[j], axis=0)

        # step 3: update centers
        centers = centers - lr * gradients

        # step 4: check convergence
        _, total_ssd = compute_ssd(data, centers, labels)
        if abs(prev_ssd - total_ssd) < tol:
            break
        prev_ssd = total_ssd

    labels = assign_clusters(data, centers)
    return centers, labels, iteration


# ═══════════════════════════════════════════════════════════════
# Method (b): Newton Raphson (Second Order Derivatives / Hessian)
# ═══════════════════════════════════════════════════════════════

def newton_raphson_kmeans(data, k, max_iter=500, tol=1e-8, seed=42):
    """
    K-Means optimization using Newton-Raphson Method.

    The objective function is the same:
        J = Σᵢ ||xᵢ - μ_c(i)||²

    Gradient w.r.t. center μⱼ:
        ∂J/∂μⱼ = -2 Σ_{i: c(i)=j} (xᵢ - μⱼ)

    Hessian w.r.t. center μⱼ:
        ∂²J/∂μⱼ² = 2 × nⱼ × I  (where nⱼ = number of points in cluster j)

    Newton-Raphson update:
        μⱼ ← μⱼ - H⁻¹ × ∇J
        μⱼ ← μⱼ - (2nⱼI)⁻¹ × (-2 Σ(xᵢ - μⱼ))
        μⱼ ← μⱼ + (1/nⱼ) × Σ(xᵢ - μⱼ)
        μⱼ ← (1/nⱼ) × Σ xᵢ   (simplifies to the mean — one-step convergence!)
    """
    centers = initialize_centers(data, k, seed)

    prev_ssd = float('inf')

    for iteration in range(1, max_iter + 1):
        # step 1: assign clusters
        labels = assign_clusters(data, centers)

        # step 2: compute gradient and Hessian, then update
        new_centers = np.copy(centers)
        for j in range(k):
            mask = labels == j
            n_j = np.sum(mask)
            if n_j == 0:
                continue

            cluster_points = data[mask]

            # gradient: -2 * sum(x_i - mu_j)
            gradient = -2 * np.sum(cluster_points - centers[j], axis=0)

            # Hessian: 2 * n_j * I (2x2 identity scaled)
            # H_inv = (1 / (2 * n_j)) * I
            hessian_inv = (1.0 / (2.0 * n_j)) * np.eye(2)

            # Newton update: mu_j = mu_j - H_inv @ gradient
            new_centers[j] = centers[j] - hessian_inv @ gradient

        centers = new_centers

        # step 3: check convergence
        _, total_ssd = compute_ssd(data, centers, labels)
        if abs(prev_ssd - total_ssd) < tol:
            break
        prev_ssd = total_ssd

    labels = assign_clusters(data, centers)
    return centers, labels, iteration


# ═══════════════════════════════════════════════════════════════
# Main: Run both methods and compare
# ═══════════════════════════════════════════════════════════════

def print_results(name, centers, labels, iters, data):
    cluster_ssd, total_ssd = compute_ssd(data, centers, labels)
    print(f"\n--- {name} (Converged in {iters} iterations) ---")
    for j in range(K):
        n_j = np.sum(labels == j)
        print(f"  Airport {j+1}: ({centers[j][0]:.3f}, {centers[j][1]:.3f})  |  Cities: {n_j}  |  SSD: {cluster_ssd[j]:.3f}")
    print(f"  Total SSD: {total_ssd:.3f}")
    return total_ssd


if __name__ == "__main__":
    # (a) Gradient Descent
    t1 = time.time()
    gd_centers, gd_labels, gd_iters = gradient_descent_kmeans(cities, K)
    gd_time = time.time() - t1
    gd_ssd = print_results("Gradient Descent (First Order)", gd_centers, gd_labels, gd_iters, cities)

    # (b) Newton Raphson
    t2 = time.time()
    nr_centers, nr_labels, nr_iters = newton_raphson_kmeans(cities, K)
    nr_time = time.time() - t2
    nr_ssd = print_results("Newton Raphson (Second Order / Hessian)", nr_centers, nr_labels, nr_iters, cities)

    # Comparison
    print(f"\n--- Comparison ---")
    print(f"  {'Method':<35} {'Iterations':>10} {'Total SSD':>12} {'Time (s)':>10}")
    print(f"  {'Gradient Descent':<35} {gd_iters:>10} {gd_ssd:>12.3f} {gd_time:>10.3f}")
    print(f"  {'Newton Raphson':<35} {nr_iters:>10} {nr_ssd:>12.3f} {nr_time:>10.3f}")