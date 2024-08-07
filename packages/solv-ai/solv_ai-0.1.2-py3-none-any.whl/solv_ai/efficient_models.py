import torch
import torch.nn as nn
import torchvision.models as models

class EfficientNet(nn.Module):
    def __init__(self):
        super(EfficientNet, self).__init__()
        try:
            self.model = models.efficientnet_b0(pretrained=True)
        except Exception as e:
            raise RuntimeError(f"Failed to load EfficientNet model: {e}")

    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        return self.model(x)