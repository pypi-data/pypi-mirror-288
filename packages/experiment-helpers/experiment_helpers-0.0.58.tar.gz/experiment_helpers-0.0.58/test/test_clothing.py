import os
import sys
sys.path.append('/home/jlb638/Desktop/package')
from src.experiment_helpers.clothing import get_segmentation_model,clothes_segmentation
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from torchvision.transforms import PILToTensor,Normalize
import torch

# Load an image from a URL
image_url = 'https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/assets/characters/akshan/skins/skin10/images/akshan_splash_uncentered_10.jpg'  # Replace with your image URL
response = requests.get(image_url)
image = Image.open(BytesIO(response.content)).convert('RGB')

model=get_segmentation_model("cpu",torch.float32)
segmented=clothes_segmentation(image,model,5)

segmented.save("segment.jpg")