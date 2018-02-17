
from Cell import Cell
import random
import  sys
import  numpy as np

class Maze:
    '''
    creating main maze for game
    '''
    def __init__(self,maze_h,maze_w,group_h,group_w):

        self.maze_height=maze_h
        self.maze_width=maze_w
        self.mine_rate=maze_h*maze_w*0.1
        self.createCell(maze_w,maze_h,group_h,group_w)



    def createCell(self,maze_w,maze_h,group_h,group_w):
        '''
         define cell, gather them  for bigger areas
        '''
        group_count=int(maze_w/group_w)
        group_length=group_w



        self.groups_index= []
        self.cells=[]

        group_id_i=-group_count

        for i in range(maze_w):
            temp=[]

            if((i%group_length)==0):
                group_id_i+=group_count

            group_id_j = -1
            group_id_j+=group_id_i
            for j in range(maze_h):
                if((j%group_length)==0):
                    group_id_j+=1

                temp.append(Cell((i,j),group_id_j))


            self.cells.append(temp)

        self.assignMine()


        aa=np.array(self.cells)
        for i in range(0, group_count):
            for j in range(0, group_count):
                self.groups_index.append(aa[i*group_length:((i*group_length)+group_length),j*group_length:((j*group_length)+group_length)] )


    def assignMine(self):
        '''
        assigning mine to randomly selected some cells
        '''
        count=0
        self.mine_index=[]
        while count<self.mine_rate:
            random_num1=random.randint(0,(self.maze_width-1))
            random_num2 = random.randint(0, (self.maze_height-1))
            if self.cells[random_num1][random_num2].is_bomb==False:
                self.cells[random_num1][random_num2].is_bomb = True
                # self.cells[random_num1][random_num2].color=(0,0,255)
                self.mine_index.append((random_num1,random_num2))
                count+=1