import numpy as np

class QuantizedLayer:
    def __init__(self, weights, bits=8, scheme='symmetric', per_channel=False):
        if not isinstance(weights, np.ndarray):
            raise TypeError("Weights must be a numpy array")
        if bits not in [8, 16, 32]:
            raise ValueError("Bits must be one of [8, 16, 32]")
        if scheme not in ['symmetric', 'asymmetric']:
            raise ValueError("Scheme must be 'symmetric' or 'asymmetric'")
        self.weights = weights
        self.bits = bits
        self.scheme = scheme
        self.per_channel = per_channel
        self.scale, self.zero_point = self.calculate_quantization_params()

    def calculate_quantization_params(self):
        if self.per_channel:
            min_val = np.min(self.weights, axis=1, keepdims=True)
            max_val = np.max(self.weights, axis=1, keepdims=True)
        else:
            min_val = np.min(self.weights)
            max_val = np.max(self.weights)
        
        if np.any(min_val == max_val):
            raise ValueError("Min and max values of weights are the same, cannot quantize")
        
        qmin = 0
        qmax = 2**self.bits - 1
        if self.scheme == 'symmetric':
            scale = np.maximum(np.abs(min_val), np.abs(max_val)) / (qmax / 2)
            zero_point = np.zeros_like(scale)
        else:  # asymmetric
            scale = (max_val - min_val) / (qmax - qmin)
            zero_point = qmin - min_val / scale
        return scale, zero_point

    def quantize(self, x):
        if not isinstance(x, np.ndarray):
            raise TypeError("Input must be a numpy array")
        return np.round(x / self.scale + self.zero_point).astype(np.int32)

    def dequantize(self, x):
        if not isinstance(x, np.ndarray):
            raise TypeError("Input must be a numpy array")
        return (x.astype(np.float32) - self.zero_point) * self.scale

    def forward(self, x):
        qx = self.quantize(x)
        return self.dequantize(qx)