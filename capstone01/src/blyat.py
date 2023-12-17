import requests
from PIL import Image
import torch
import numpy as np
from transformers import OwlViTProcessor, OwlViTForObjectDetection
from models.model_manager import ModelManager
from schema import Config, HDStrategy
from helper import resize_max_size
import cv2
import time


OFFSET = 20  # Set the offset value for the mask

# Initialize OwlViT processor and model
processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
owlvit_model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")

# Take image URL as input
url = input("Enter image URL: ")

# Initialize the LaMa model
lama_model = ModelManager(name="lama", device="cpu")

# Load initial image from URL
image = Image.open(requests.get(url, stream=True).raw)

# List of texts to iterate over
texts = [
    (["photo of an advertising sign on a building"], 0.09),
    (["photo of a freestanding A-frame sidewalk signs"], 0.08),
    (["photo of a vertical signs on building sides with text"], 0.08),
    (["photo of an advertising lightbox pharmacy sign on building"], 0.06),
    (["photo of an advertising lightbox pharmacy sign on building"], 0.06),
    (["Split-type AC units"], 0.04),
]

for text_item in texts:
    # Prepare inputs for OwlViT
    inputs = processor(text=text_item[0], images=image, return_tensors="pt")
    outputs = owlvit_model(**inputs)

    # Process OwlViT outputs to create a mask
    target_sizes = torch.Tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=text_item[1])
    boxes = results[0]["boxes"]

    mask = np.zeros(image.size[::-1], dtype=np.uint8)
    for box in boxes:
        box = [int(round(b)) for b in box.tolist()]
        x_min, y_min, x_max, y_max = np.clip([box[0] - OFFSET, box[1] - OFFSET, box[2] + OFFSET, box[3] + OFFSET], 0, [image.size[0], image.size[1], image.size[0], image.size[1]])
        mask[y_min:y_max, x_min:x_max] = 1

    # Check if the mask is empty (all black)
    if not np.any(mask):
        print(f"No objects detected for '{text_item[0]}', skipping inpainting.")
        continue  # Skip to the next iteration

    # Convert the mask to a PIL Image for processing
    mask_image = Image.fromarray(mask * 255)

    # Convert PIL Images to NumPy arrays for LaMa model processing
    np_image = np.array(image.convert("RGB"))
    np_mask = np.array(mask_image.convert("L"))

    # Resize the image and mask if necessary
    # size_limit = max(np_image.shape)
    # interpolation = cv2.INTER_CUBIC
    # np_image = resize_max_size(np_image, size_limit=size_limit, interpolation=interpolation)
    # np_mask = resize_max_size(np_mask, size_limit=size_limit, interpolation=interpolation)

    # Configuration for LaMa model
    config = Config(
        hd_strategy=HDStrategy.CROP,
        hd_strategy_crop_margin=10,
        hd_strategy_crop_trigger_size=1000,
        hd_strategy_resize_limit=2048,
    )

    # Perform inpainting with LaMa model
    start = time.time()
    res_np_img = lama_model(np_image, np_mask, config=config)
    print(f"Processing time for '{text_item[0]}': {(time.time() - start) * 1000}ms")

    # Update the image with the result for the next iteration
    image = Image.fromarray(cv2.cvtColor(res_np_img.astype(np.uint8), cv2.COLOR_BGR2RGB))

# Display the final result using PIL
image.show()