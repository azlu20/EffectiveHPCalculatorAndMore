#import pytorch as torch
import numpy as np
import pandas as pd
from GetItems import *
from PullChampionStats import *
from pprint import pprint

# class RNNModel(nn.module):
#     def __init__(self, input_size=6, output_size=1, hidden_dims=0):
#         super(Net, self).__init__()
#         self.hidden_dim = hidden_dims
#         self.rnn = torch.RNN()
#

class DataEncoder(object):
    def __init__(self):
        self.items_file_location = item_create_file()
        self.champions_file_location = create_file()
        self.items_dataset = pd.read_csv(self.items_file_location, sep=',', header=0)
        self.champions_dataset = pd.read_csv(self.champions_file_location, sep=',', header=0)
        self.item_dict = {}
    def encodeData(self):
        i = 0
        while i < self.items_dataset.count()[0]:
            #print(self.items_dataset.iloc[i])
            pprint(dir(self.items_dataset.iloc[i]))
            break
            i+=1


test = DataEncoder()
test.encodeData()