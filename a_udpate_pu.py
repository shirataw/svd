import copy
import numpy


class a_pu:

    # The PU memory model;
    class pu_mem:
        def __init__ (self, mem_size, index_init):
            # The PU memory model parameters, has memory content, 
            # index of the current column stored,
            # and the status of the memory: private(0) or shared(1) or invalid(2); 
            self.mem = numpy.zeros((mem_size,), dtype = float)
            self.index_old = 0
            self.index_new = index_init
            self.status = 'initial'

    def __init__ (self, mem_size, num_col, index):
        # Inializa parameters;
        self.mem0 = pu_mem(mem_size, index[0])
        self.mem1 = pu_mem(mem_size, index[1])
        self.np = 0
        self.nq = 0
        self.cov = 0
        self.num_col = num_col
        self.cnt_itr_pu = 1
    # Method for reading current index and determing the status;
    def mem_stat_config (self, index):
        # Read in the new indices; 
        self.mem0.index_old = copy.deepcopy(self.mem0.index_new)
        self.mem1.index_old = copy.deepcopy(self.mem1.index_new)
        # Based on the old and new indices, determines the memory status bits; 
        # At sequence head, all mems set to 'head' state, increase iteration counter;
        if (self.cnt_itr_pu == 1):
            self.mem0.status = 'head'
            self.mem1.status = 'head'
            self.cnt_itr_pu = self.cnt_itr_pu + 1
        # At sequence tail, all mems set to 'tail' state, reset the iteration counter;
        elif (self.cnt_itr_pu == self.num_col - 1): 
            self.mem0.status = 'tail'
            self.mem1.status = 'tail'
            self.cnt_itr_pu = 1
        # In the middle of the sequence, determine each mem is private or shared; 
        else: 
            # Mem0 is the private memory;
            if (self.mem0.index_old == index[0]):
                self.mem0.status = 'private'
                self.mem1.status = 'shared'
                self.mem0.index_new = index[0]
                self.mem1.index_new = index[1]
            elif (self.mem0.index_old == index[1]):
                self.mem0.status = 'private'
                self.mem1.status = 'shared'
                self.mem0.index_new = index[1]
                self.mem1.index_new = index[0]
            # Mem1 is the private memory;
            elif (self.mem1.index_old == index[0]):
                self.mem0.status = 'shared'
                self.mem1.status = 'private'
                self.mem0.index_new = index[1]
                self.mem1.index_new = index[0]
            elif (self.mem1.index_old == index[1]):
                self.mem0.status = 'shared'
                self.mem1.status = 'private'
                self.mem0.index_new = index[0]
                self.mem1.index_new = index[1]
        # Meeting boundary, 

    # Methods for data transfering;
    # Method for reading data from DRAM;
    def rd_dram (self, dram):
        self.mem0.mem = dram[:, self.mem0.index_new]
        self.mem1.mem = dram[:, self.mem1.index_new]
    # Method for writing data to DRAM;
    def wr_dram (self, dram):
        dram[:, self.mem0.index_old] = self.mem0.mem
        dram[:, self.mem1.index_old] = self.mem1.mem
    # Method for writing shared data; 
    def data_sync (self):
        if (self.mem0.status == 'shared'):
            return self.mem0.mem
        else:
            return self.mem1.mem

    # Methods for computation and updating;
    # Covariance and Euclidean norm calculation;
    def cov_cal (self):
        # Compare the indices in different mems;
        if (self.mem0.index_new)
    
