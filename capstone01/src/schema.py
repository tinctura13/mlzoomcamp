from enum import Enum

from pydantic import BaseModel


class HDStrategy(str, Enum):
    # Use original image size
    ORIGINAL = "Original"
    # Resize the longer side of the image to a specific size(hd_strategy_resize_limit),
    # then do inpainting on the resized image. Finally, resize the inpainting result to the original size.
    # The area outside the mask will not lose quality.
    RESIZE = "Resize"
    # Crop masking area(with a margin controlled by hd_strategy_crop_margin) from the original image to do inpainting
    CROP = "Crop"

class Config(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # Configs for High Resolution Strategy(different way to preprocess image)
    hd_strategy: str  # See HDStrategy Enum
    hd_strategy_crop_margin: int
    # If the longer side of the image is larger than this value, use crop strategy
    hd_strategy_crop_trigger_size: int
    hd_strategy_resize_limit: int
