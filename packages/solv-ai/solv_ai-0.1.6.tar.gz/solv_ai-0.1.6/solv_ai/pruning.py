import numpy as np

class PrunedLayer:
    def __init__(self, weights, pruning_rate=0.5, structured=False, method='l1'):
        if not isinstance(weights, np.ndarray):
            raise TypeError("Weights must be a numpy array")
        if not (0 <= pruning_rate <= 1):
            raise ValueError("Pruning rate must be between 0 and 1")
        if method not in ['l1', 'l2']:
            raise ValueError("Method must be 'l1' or 'l2'")
        self.weights = weights
        self.pruning_rate = pruning_rate
        self.structured = structured
        self.method = method
        self.mask = self.create_pruning_mask()

    def create_pruning_mask(self):
        if self.structured:
            if self.method == 'l1':
                norm = np.sum(np.abs(self.weights), axis=(1, 2, 3))
            else:  # default to L2 norm
                norm = np.linalg.norm(self.weights, axis=(1, 2, 3))
            threshold = np.percentile(norm, self.pruning_rate * 100)
            mask = norm >= threshold
        else:
            if self.method == 'l1':
                threshold = np.percentile(np.abs(self.weights), self.pruning_rate * 100)
            else:  # default to L2 norm
                threshold = np.percentile(np.square(self.weights), self.pruning_rate * 100)
            mask = np.abs(self.weights) >= threshold
        return mask

    def forward(self, x):
        if not isinstance(x, np.ndarray):
            raise TypeError("Input must be a numpy array")
        pruned_weights = self.weights * self.mask
        return np.dot(x, pruned_weights)