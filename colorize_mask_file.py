

#a function to colorize masks with a custom colormap
import numpy as np
from matplotlib import pyplot as plt


def colorize_mask(mask):
    """turns mask images with low contrast values (0, 1, 2, ...) into color images"""
    # Define a dictionary of category colors
    category_colors = {
        "(0, 0, 0)": 0,  # Outlier
        "(255, 0, 0)": 1,  # Window
        "(255, 255, 0)": 2,  # Wall
        "(128, 0, 255)": 3,  # Balcony
        "(255, 128, 0)": 4,  # Door
        "(0, 0, 255)": 5,  # Roof
        "(128, 255, 255)": 6,  # Sky
        "(0, 255, 0)": 7,  # Shop
        "(128, 128, 128)": 8  # Chimney
    }
    # Create an array or list of colors for each pixel
    colors = np.empty((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
    # Loop through each category and color the pixels
    for category, label in category_colors.items():
        colors[mask == label] = eval(category)
    # Plot the image
    plt.imshow(colors)
    plt.axis('off')
    plt.draw()
    return colors