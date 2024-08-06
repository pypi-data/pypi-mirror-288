import torch
from torch.cuda.amp import autocast, GradScaler

class MixedPrecisionLayer:
    def __init__(self, layer, optimizer):
        if not isinstance(layer, torch.nn.Module):
            raise TypeError("Layer must be a torch.nn.Module")
        if not isinstance(optimizer, torch.optim.Optimizer):
            raise TypeError("Optimizer must be a torch.optim.Optimizer")
        self.layer = layer
        self.optimizer = optimizer
        self.scaler = GradScaler()

    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        with autocast():
            output = self.layer(x)
        return output

    def backward(self, loss):
        if not isinstance(loss, torch.Tensor):
            raise TypeError("Loss must be a torch.Tensor")
        self.scaler.scale(loss).backward()
        self.scaler.step(self.optimizer)
        self.scaler.update()