
from random import  randint
from  random import  random
import random
import numpy as np
class Cell:
    '''
    properties of each gen inside chromosome
    '''
    def __init__(self, cell_id,group_id):

        self.cell_id=cell_id
        self.group_id=group_id
        self.is_opened=False;
        self.is_bomb=False
        self.color = np.array((255, 255, 255), np.float32)




