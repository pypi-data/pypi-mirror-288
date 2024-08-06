import torch
import torch.nn as nn

class FusedLayer(nn.Module):
    def __init__(self, conv, bn, relu):
        if not isinstance(conv, nn.Conv2d):
            raise TypeError("Conv must be an instance of nn.Conv2d")
        if not isinstance(bn, nn.BatchNorm2d):
            raise TypeError("BN must be an instance of nn.BatchNorm2d")
        if not isinstance(relu, nn.ReLU):
            raise TypeError("ReLU must be an instance of nn.ReLU")
        super(FusedLayer, self).__init__()
        self.conv = conv
        self.bn = bn
        self.relu = relu

    def forward(self, x):
        if not isinstance(x, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")
        x = self.conv(x)
        x = self.bn(x)
        x = self.relu(x)
        return x

def fuse_layers(conv, bn, relu):
    return FusedLayer(conv, bn, relu)