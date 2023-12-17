import time

import cv2
import numpy as np
from loguru import logger
from PIL import Image

from .models.model_manager import ModelManager
from .models.owlvit import detect_classes
from .schema import Config, HDStrategy

lama_model = ModelManager(name="lama", device="cpu")


class_texts = {
    # "class_name": "prompt",
    "class_1": "photo of an advertising sign on a building",
    "class_2": "photo of an Signboard on a building",
    "class_3": "photo of a Pavement sign",
    "class_4": "photo of an advertising lightbox sign on building",
    "class_5": "Split-type AC units",
}


def inpaint(image: Image, class_name: str, threshold: float) -> Image:
    prompt = class_texts.get(class_name, "Unknown class name")
    np_image, np_mask = detect_classes(image, prompt, threshold)
          
    # Check if the mask is empty (all black)
    if not np.any(np_mask):
        logger.info(f"No objects detected for '{class_name}', skipping inpainting.")
        return Image.fromarray(np_image.astype(np.uint8))

    #
    config = Config(
        hd_strategy=HDStrategy.CROP,
        hd_strategy_crop_margin=10,
        hd_strategy_crop_trigger_size=1000,
        hd_strategy_resize_limit=2048,
    )

    # Perform inpainting with LaMa model
    start = time.time()
    res_np_img = lama_model(np_image, np_mask, config=config)
    logger.info(f"Processing time for '{class_name}': {(time.time() - start) * 1000}ms")

    # Update the image with the result for the next iteration
    return Image.fromarray(cv2.cvtColor(res_np_img.astype(np.uint8), cv2.COLOR_BGR2RGB))