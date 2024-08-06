import os
from PIL import Image

def load_image(name):
    # Define the path to the images
    data_dir = os.path.join(os.path.dirname(__file__), 'images')
    image_path = os.path.join(data_dir, f'{name}.png')  
    
    # Check if the image exists
    if not os.path.isfile(image_path):
        raise ValueError(f"Image {name} does not exist.")
    
    # Load and return the image
    return Image.open(image_path)
