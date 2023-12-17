import gc

import torch

from src.models.lama import LaMa
from src.schema import Config

models = {
    "lama": LaMa,
}


class ModelManager:
    def __init__(self, name: str, device: torch.device, **kwargs):
        if name != "lama":
            raise NotImplementedError("This version only supports the LaMa model.")
        self.name = name
        self.device = device
        self.kwargs = kwargs
        self.model = self.init_model(name, device, **kwargs)

    def init_model(self, name: str, device, **kwargs):
        if name == "lama":
            model = models[name](device, **kwargs)
        else:
            raise NotImplementedError(f"Not supported model: {name}")
        return model

    def is_downloaded(self, name: str) -> bool:
        if name == "lama":
            return models[name].is_downloaded()
        else:
            raise NotImplementedError(f"Not supported model: {name}")

    def __call__(self, image, mask, config: Config):
        return self.model(image, mask, config)

    def switch(self, new_name: str, **kwargs):
        if new_name != "lama":
            raise NotImplementedError("This version only supports the LaMa model.")
        # No need to switch if the new model is the same as the current one
        if new_name == self.name:
            return
        try:
            if torch.cuda.memory_allocated() > 0:
                # Clear current loaded model from memory
                torch.cuda.empty_cache()
                del self.model
                gc.collect()

            self.model = self.init_model(new_name, self.device, **self.kwargs)
            self.name = new_name
        except NotImplementedError as e:
            raise e
