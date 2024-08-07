import torch
import torch.nn as nn
import torch.distributed as dist

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

class CustomPipelineParallelLayer(nn.Module):
    def __init__(self, layers, devices):
        if not isinstance(layers, list):
            raise TypeError("Layers must be a list")
        if not all(isinstance(layer, torch.nn.Module) for layer in layers):
            raise TypeError("All elements in layers must be torch.nn.Module")
        if not isinstance(devices, list):
            raise TypeError("Devices must be a list")
        if not all(isinstance(device, torch.device) for device in devices):
            raise TypeError("All elements in devices must be torch.device")
        super(CustomPipelineParallelLayer, self).__init__()
        self.layers = nn.ModuleList(layers)
        self.devices = devices

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            x = x.to(self.devices[i])
            x = layer(x)
        return x