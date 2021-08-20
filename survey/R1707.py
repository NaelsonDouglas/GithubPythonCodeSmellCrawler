def alocate_memory(self, memory=1024):
    swap = 64
    if memory < 512:
        swap = 256,
    diff = memory-swap
    self.memory = memory
    self.swap = swap
    self.diff = diff