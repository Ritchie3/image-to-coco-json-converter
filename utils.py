from PIL import Image
import os

def get_unique_colors(file_path) -> list:
    with Image.open(file_path) as im:
        # Get a list of all pixels in the image
        pixels = im.convert('RGB').getdata()
        # Use a set to get unique RGB values
        unique_colors = set(pixels)
        # Return the unique colors as a list
        return list(unique_colors)


def get_unique_colors_from_folder(folder_path) -> dict:
    """get_unique_colors from gif files in a folder and return a dictionary"""
    unique_colors = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".gif"):
            print(filename)
            unique_colors.extend(get_unique_colors(os.path.join(folder_path, filename)))
        else:
            continue

    unique_values = set(colors)
    unique_values = sorted(unique_values)
    # Use dictionary comprehension to create a dictionary with integer labels
    output_dict = {f"{x}": i for i, x in enumerate(unique_values)}
    return output_dict

if __name__ == "__main__":

    if 0:
        pass


    if 1: #get_unique_colors from giffiles in a folder and return a dictionary
        folder_path = r"C:\dataset_inspect40\picanol_sabrina_pro\full_size\masks"
        colors = get_unique_colors_from_folder(folder_path)
        print(colors)
