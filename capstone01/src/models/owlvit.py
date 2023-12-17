from typing import Tuple

import numpy as np
import torch
from PIL import Image
from transformers import OwlViTForObjectDetection, OwlViTProcessor

OFFSET = 20  # Set the offset value for the mask

# Initialize OwlViT processor and model
processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
owlvit_model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")


def detect_classes(image: Image, target: str, threshold: float) -> Tuple[np.ndarray, np.ndarray]:
    inputs = processor(text=target, images=image, return_tensors="pt")
    outputs = owlvit_model(**inputs)

    # Process OwlViT outputs to create a mask
    target_sizes = torch.Tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs=outputs, target_sizes=target_sizes, threshold=threshold)
    boxes = results[0]["boxes"]

    mask = np.zeros(image.size[::-1], dtype=np.uint8)
    for box in boxes:
        box = [int(round(b)) for b in box.tolist()]
        x_min, y_min, x_max, y_max = np.clip([box[0] - OFFSET, box[1] - OFFSET, box[2] + OFFSET, box[3] + OFFSET], 0, [image.size[0], image.size[1], image.size[0], image.size[1]])
        mask[y_min:y_max, x_min:x_max] = 1

    # Convert the mask to a PIL Image for processing
    mask_image = Image.fromarray(mask * 255)

    # Convert PIL Images to NumPy arrays for LaMa model processing
    # np_image = np.array(image.convert("RGB"))
    # np_mask = np.array(mask_image.convert("L"))
    
    return np.array(image), np.array(mask_image)
