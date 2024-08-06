import torch
import torch.nn as nn
import torch.distributed as dist
from torch.distributed.pipeline.sync import Pipe

class ModelParallelLayer(nn.Module):
    def __init__(self, layer, device_ids):
        if not isinstance(layer, torch.nn.Module):
            raise TypeError("Layer must be a torch.nn.Module")
        if not isinstance(device_ids, list):
            raise TypeError("Device IDs must be a list")
        super(ModelParallelLayer, self).__init__()
        self.layer = nn.DataParallel(layer, device_ids=device_ids)

    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        return self.layer(x)

class DataParallelLayer(nn.Module):
    def __init__(self, layer, device_ids):
        if not isinstance(layer, torch.nn.Module):
            raise TypeError("Layer must be a torch.nn.Module")
        if not isinstance(device_ids, list):
            raise TypeError("Device IDs must be a list")
        super(DataParallelLayer, self).__init__()
        self.layer = nn.DataParallel(layer, device_ids=device_ids)

    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        return self.layer(x)

class PipelineParallelLayer(nn.Module):
    def __init__(self, layers, chunks=2):
        if not isinstance(layers, list):
            raise TypeError("Layers must be a list")
        if not all(isinstance(layer, torch.nn.Module) for layer in layers):
            raise TypeError("All elements in layers must be torch.nn.Module")
        if not isinstance(chunks, int) or chunks <= 0:
            raise ValueError("Chunks must be a positive integer")
        super(PipelineParallelLayer, self).__init__()
        self.pipeline = Pipe(nn.Sequential(*layers), chunks=chunks)

    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        return self.pipeline(x)