import copy

class seq_gen:
    def __init__ (self, num_col, num_pu): 
        self.num_col = num_col
        self.num_pu = num_pu
        # Initializing parameters;
        self.seq = []
        for i in range (num_pu):
            self.seq.append([i + 1, num_col - i])
        self.seq_init = copy.deepcopy(self.seq)
        self.cnt_itr_pu = 1
        self.cnt_itr_glb = num_pu
        self.itr_max = num_col * (num_col - 1)//2
        self.flag = [0 for _ in range (num_pu)]
    # Generating next index for all PUs;
    def next (self):
        # If boundary is reached, set the new begining sequence; 
        if (self.cnt_itr_pu == self.num_col - 1):
            # Reset cnt_itr_pu, increase cnt_itr_glb, reset flag;
            self.cnt_itr_pu = 1
            self.flag = [0 for _ in range (self.num_pu)]
            # If cnt_itr_glb is not at maximum, simply increase;
            if (self.cnt_itr_glb < self.itr_max - self.num_pu):
                self.cnt_itr_glb = self.cnt_itr_glb + self.num_pu
                for i in range (self.num_pu): 
                    self.seq[i][0] = self.seq_init[i][0] + self.num_pu
                    self.seq[i][1] = self.seq_init[i][1] - self.num_pu
                    self.seq_init[i][0] = self.seq[i][0]
                    self.seq_init[i][1] = self.seq[i][1]
            # Else, set the initial sequence to the most initial state, reset cnt_itr_glb
            elif (self.cnt_itr_glb == self.itr_max): 
                self.cnt_itr_glb = self.num_pu
                self.seq = []
                for i in range (self.num_pu):
                    self.seq.append([i + 1, self.num_col - i])
                self.seq_init = copy.deepcopy(self.seq)
        # Else, based on the actual curretn index, generate next index for each PU;
        else: 
            # Increase cnt_itr_pu and cnt_itr_glb;
            self.cnt_itr_pu = self.cnt_itr_pu + 1
            self.cnt_itr_glb = self.cnt_itr_glb + self.num_pu
            for i in range (self.num_pu):
                # First two cases; 
                if (self.flag[i - 1] == 0):
                    if (self.seq[i][0] == self.seq[i][1] - 1):
                        self.flag[i - 1] = 1
                        self.seq[i][1] = self.num_col
                    else: 
                        self.seq[i][1] = self.seq[i][1] - 1
                # Second case;
                elif (self.flag[i - 1] == 1):
                    self.flag[i - 1] = 2
                    self.seq[i][0] = self.seq[i][0] + self.num_col//2 - 1
                # Third case;
                elif (self.flag[i - 1] == 2):
                    self.flag[i - 1] = 3
                    self.seq[i][1] = self.seq[i][0]
                    self.seq[i][0] = self.seq[i][1] - 1
                # Last case;
                elif (self.flag[i - 1] == 3):
                    self.seq[i][0] = self.seq[i][0] - 1
    # Print function, for debug;
    def display (self):
        print('The current sequence is: ', self.seq)
        #print('The current sequence_init is: ', self.seq_init)
        #print('The current cnt_itr_glb is: ', self.cnt_itr_pu)
        #print('The current cnt_itr_glb is: ', self.cnt_itr_glb)


seq_inst = seq_gen(16,2)
print(seq_inst.itr_max)

for _ in range (30):
    seq_inst.display()
    seq_inst.next()
    
