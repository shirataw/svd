import copy


class a_pu:

    # The PU memory model;
    class pu_mem:
        def __init__ (self, mem_size):
            # The PU memory model parameters, has memory content, 
            # index of the current column stored,
            # and the status of the memory: private(0) or shared(1) or invalid(2); 
            self.mem = [0 for _ in range (mem_size)]
            self.index_old = 0
            self.index_new = 0
            self.status = 0

    def __init__ (self, mem_size):
        # Inializa parameters;
        self.mem0 = pu_mem(mem_size)
        self.mem0 = pu_mem(mem_size)
    # Method for reading current index;
    def index_rd (self, index):
        self.index_old = copy.deepcopy(self.index_new)
        self.index_new = index
    # Method for data reading;