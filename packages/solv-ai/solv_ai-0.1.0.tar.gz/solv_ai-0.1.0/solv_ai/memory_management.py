import torch
from torch.utils.checkpoint import checkpoint

class MemoryManager:
    def __init__(self):
        self.memory_pool = {}

    def allocate(self, size):
        if not isinstance(size, tuple):
            raise TypeError("Size must be a tuple")
        if size not in self.memory_pool:
            self.memory_pool[size] = torch.empty(size, dtype=torch.float32)
        return self.memory_pool[size]

    def deallocate(self, size):
        if not isinstance(size, tuple):
            raise TypeError("Size must be a tuple")
        if size in self.memory_pool:
            del self.memory_pool[size]

    def checkpoint(self, function, *args):
        if not callable(function):
            raise TypeError("Function must be callable")
        return checkpoint(function, *args)