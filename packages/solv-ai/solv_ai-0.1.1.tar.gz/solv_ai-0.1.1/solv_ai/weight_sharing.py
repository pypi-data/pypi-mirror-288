import torch
import torch.nn as nn

class SharedWeightsLayer(nn.Module):
    def __init__(self, shared_weights):
        if not isinstance(shared_weights, torch.Tensor):
            raise TypeError("Shared weights must be a torch.Tensor")
        super(SharedWeightsLayer, self).__init__()
        self.shared_weights = shared_weights

    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        return nn.functional.linear(x, self.shared_weights)