import torch

class DynamicQuantizedLayer:
    def __init__(self, layer):
        if not isinstance(layer, torch.nn.Module):
            raise TypeError("Layer must be a torch.nn.Module")
        self.layer = layer

    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        x = torch.quantize_per_tensor(x, scale=0.1, zero_point=0, dtype=torch.qint8)
        output = self.layer(x.dequantize())
        return torch.quantize_per_tensor(output, scale=0.1, zero_point=0, dtype=torch.qint8).dequantize()