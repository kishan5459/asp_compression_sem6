import numpy as np
import cv2
from scipy.fftpack import dct, idct

def compress_channel(channel, block_size=8, keep_fraction=0.5):
    h, w = channel.shape
    compressed = np.zeros((h, w), dtype=np.float32)

    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            block = channel[i:i+block_size, j:j+block_size]
            if block.shape != (block_size, block_size):
                continue
            dct_block = dct(dct(block.T, norm='ortho').T, norm='ortho')
            dct_block[int(block_size * keep_fraction):, :] = 0
            dct_block[:, int(block_size * keep_fraction):] = 0
            idct_block = idct(idct(dct_block.T, norm='ortho').T, norm='ortho')
            compressed[i:i+block_size, j:j+block_size] = idct_block

    return np.clip(compressed, 0, 255).astype(np.uint8)

def compress_image_dct(image_path, block_size=8, keep_fraction=0.5):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR to RGB

    channels = cv2.split(img)
    compressed_channels = [compress_channel(c, block_size, keep_fraction) for c in channels]
    compressed_img = cv2.merge(compressed_channels)

    return cv2.cvtColor(compressed_img, cv2.COLOR_RGB2BGR)  # Back to BGR for saving

def save_image(image_array, output_path):
    cv2.imwrite(output_path, image_array)