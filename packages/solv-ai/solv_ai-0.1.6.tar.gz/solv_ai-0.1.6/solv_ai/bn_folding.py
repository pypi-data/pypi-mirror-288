import torch
import torch.nn as nn

def fold_batch_norm(conv, bn):
    if not isinstance(conv, nn.Conv2d):
        raise TypeError("Conv must be an instance of nn.Conv2d")
    if not isinstance(bn, nn.BatchNorm2d):
        raise TypeError("BN must be an instance of nn.BatchNorm2d")
    with torch.no_grad():
        # Fold batch norm parameters into convolutional layer
        conv.weight.data = conv.weight.data * bn.weight.data.view(-1, 1, 1, 1) / torch.sqrt(bn.running_var + bn.eps).view(-1, 1, 1, 1)
        conv.bias.data = (conv.bias.data - bn.running_mean) * bn.weight.data / torch.sqrt(bn.running_var + bn.eps) + bn.bias.data
    return conv