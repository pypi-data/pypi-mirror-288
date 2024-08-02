import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
from collections import deque
import random

def cluster_colors(image_matrix, n_clusters=8):
    rows, cols, _ = image_matrix.shape
    flat_image_matrix = image_matrix.reshape(-1, 3)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(flat_image_matrix)
    cluster_centers = kmeans.cluster_centers_
    labels = kmeans.labels_
    
    label_to_center = {label: center for label, center in enumerate(cluster_centers)}
    clustered_flat_image_matrix = np.array([label_to_center[label] for label in labels])
    clustered_image_matrix = clustered_flat_image_matrix.reshape((rows, cols, 3))
    
    clustered_image_matrix = np.clip(clustered_image_matrix, 0, 255).astype(np.uint8)
    
    return clustered_image_matrix, labels.reshape(rows, cols), cluster_centers

def within_color_range(color1, color2, threshold=0.02):
    color1 = np.array(color1, dtype=float)
    color2 = np.array(color2, dtype=float)
    return all(abs(c1 - c2) <= threshold * 255 for c1, c2 in zip(color1, color2))

def flood_fill(image_matrix, start_pos, threshold=0.02):
    rows, cols, _ = image_matrix.shape
    checked = np.zeros((rows, cols), dtype=bool)
    flood_area = []
    edge_pixels = []

    queue = deque([start_pos])
    start_color = image_matrix[start_pos]

    while queue:
        x, y = queue.popleft()
        if not checked[x, y]:
            checked[x, y] = True
            current_color = image_matrix[x, y]

            if within_color_range(start_color, current_color, threshold):
                flood_area.append((x, y))

                is_edge = False
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and not within_color_range(start_color, image_matrix[nx, ny], threshold):
                        is_edge = True
                        break

                if is_edge:
                    edge_pixels.append((x, y))

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and not checked[nx, ny]:
                        queue.append((nx, ny))

    return flood_area, edge_pixels

def explore_all_zones(image_matrix, threshold=0.02):
    rows, cols, _ = image_matrix.shape
    unexplored_pixels = {(x, y) for x in range(rows) for y in range(cols)}
    zones = []
    all_edge_pixels = []

    while unexplored_pixels:
        start_pos = random.choice(list(unexplored_pixels))
        zone, edge_pixels = flood_fill(image_matrix, start_pos, threshold)
        if zone:
            zones.append(zone)
            all_edge_pixels.extend(edge_pixels)
            unexplored_pixels.difference_update(zone)

    return zones, all_edge_pixels

def merge_small_zones(zones, image_matrix, min_pixels):
    large_zones = [zone for zone in zones if len(zone) >= min_pixels]
    small_zones = [zone for zone in zones if len(zone) < min_pixels]

    large_zone_colors = [
        np.mean([image_matrix[x, y] for x, y in zone], axis=0)
        for zone in large_zones
    ]

    for small_zone in small_zones:
        small_zone_color = np.mean([image_matrix[x, y] for x, y in small_zone], axis=0)
        distances = [
            euclidean(small_zone_color, large_zone_color)
            for large_zone_color in large_zone_colors
        ]
        closest_large_zone_index = np.argmin(distances)
        large_zones[closest_large_zone_index].extend(small_zone)

    return large_zones

def process_image(image_path, threshold=0.02, min_pixels=100, n_clusters=8, return_format="outlined_image"):
    # Security checks
    if threshold < 0.01:
        threshold = 0.01
    elif threshold > 0.999:
        threshold = 0.999

    if n_clusters < 2:
        n_clusters = 2
    elif n_clusters > 99:
        n_clusters = 99

    image = Image.open(image_path)
    image_rgb = image.convert('RGB')
    image_matrix = np.array(image_rgb)

    if min_pixels < 1:
        min_pixels = 1
    elif min_pixels > image_matrix.shape[0] * image_matrix.shape[1]:
        min_pixels = image_matrix.shape[0] * image_matrix.shape[1]

    clustered_image_matrix, labels, cluster_centers = cluster_colors(image_matrix, n_clusters=n_clusters)

    zones, all_edge_pixels = explore_all_zones(clustered_image_matrix, threshold)

    merged_zones = merge_small_zones(zones, clustered_image_matrix, min_pixels)

    outlined_image = image_matrix.copy()
    for x, y in all_edge_pixels:
        outlined_image[x, y] = [0, 0, 0]

    if return_format == "outlined_image":
        output_image = outlined_image
    elif return_format == "mask":
        mask = np.ones_like(image_matrix) * 255
        for x, y in all_edge_pixels:
            mask[x, y] = [0, 0, 0]
        output_image = mask
    elif return_format == "weighted_colored_zones":
        weighted_colored_image = np.zeros_like(clustered_image_matrix)
        for zone in merged_zones:
            if zone:
                zone_color = cluster_centers[labels[zone[0][0], zone[0][1]]]
                for x, y in zone:
                    weighted_colored_image[x, y] = zone_color
        output_image = weighted_colored_image
    elif return_format == "local_colored_zones":
        local_colored_image = np.zeros_like(clustered_image_matrix)
        for zone in merged_zones:
            if zone:
                local_zone_color = np.mean([image_matrix[x, y] for x, y in zone], axis=0)
                for x, y in zone:
                    local_colored_image[x, y] = local_zone_color
        output_image = local_colored_image
    elif return_format == "rgbm":
        rgbm_image = np.zeros((image_matrix.shape[0], image_matrix.shape[1], 4), dtype=np.uint8)
        rgbm_image[:, :, :3] = image_matrix
        mask = np.zeros((image_matrix.shape[0], image_matrix.shape[1]), dtype=np.uint8)
        for x, y in all_edge_pixels:
            mask[x, y] = 1
        rgbm_image[:, :, 3] = mask
        output_image = rgbm_image
    else:
        raise ValueError("Invalid return format specified")

    if return_format != "rgbm" and output_image.shape[2] != 3:
        raise ValueError("Output image must have 3 channels for the selected return format")

    return output_image
