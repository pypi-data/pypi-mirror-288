import torch
import asyncio

class LayerManager:
    def __init__(self, model):
        if not isinstance(model, torch.nn.Module):
            raise TypeError("Model must be a torch.nn.Module")
        self.model = model
        self.layer_cache = {}

    async def load_layer(self, layer_name):
        if not isinstance(layer_name, str):
            raise TypeError("Layer name must be a string")
        if layer_name not in self.layer_cache:
            try:
                self.layer_cache[layer_name] = getattr(self.model, layer_name)
            except AttributeError:
                raise ValueError(f"Layer {layer_name} not found in the model")
        return self.layer_cache[layer_name]

    async def offload_layer(self, layer_name):
        if not isinstance(layer_name, str):
            raise TypeError("Layer name must be a string")
        if layer_name in self.layer_cache:
            del self.layer_cache[layer_name]