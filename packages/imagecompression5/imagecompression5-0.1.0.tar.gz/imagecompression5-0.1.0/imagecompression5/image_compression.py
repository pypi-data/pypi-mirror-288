from PIL import Image
import numpy as np
from .reis_algorithm import reis_algorithm

def image_to_matrix(image_path):
    image = Image.open(image_path).convert('L')
    matrix = np.array(image)
    return matrix

def matrix_to_image(matrix, output_path):
    image = Image.fromarray(matrix)
    image.save(output_path)

def split_image_to_blocks(matrix, block_size):
    blocks = []
    h, w = matrix.shape
    h_blocks = h // block_size
    w_blocks = w // block_size
    for i in range(h_blocks):
        for j in range(w_blocks):
            block = matrix[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size]
            blocks.append(block)
    return blocks, (h_blocks, w_blocks)

def merge_blocks_to_image(blocks, h_blocks, w_blocks, block_size):
    h = h_blocks * block_size
    w = w_blocks * block_size
    new_image = np.zeros((h, w), dtype=np.uint8)
    block_idx = 0
    for i in range(h_blocks):
        for j in range(w_blocks):
            new_image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size] = blocks[block_idx]
            block_idx += 1
    return new_image

def compress_image(matrix, block_size, epsilon=1e-6):
    blocks, (h_blocks, w_blocks) = split_image_to_blocks(matrix, block_size)
    compressed_blocks = []
    P = np.eye(block_size)

    for block in blocks:
        R = reis_algorithm(block, P, epsilon)
        compressed_blocks.append(R)

    return compressed_blocks, h_blocks, w_blocks

def normalize(matrix):
    matrix = matrix - np.min(matrix)
    matrix = matrix / np.max(matrix) * 255
    return matrix.astype(np.uint8)

def main(image_path, compressed_image_path, block_size=8, epsilon=1e-6):
    matrix = image_to_matrix(image_path)
    compressed_blocks, h_blocks, w_blocks = compress_image(matrix, block_size, epsilon)
    compressed_matrix = merge_blocks_to_image(compressed_blocks, h_blocks, w_blocks, block_size)
    normalized_matrix = normalize(compressed_matrix)
    matrix_to_image(normalized_matrix, compressed_image_path)
