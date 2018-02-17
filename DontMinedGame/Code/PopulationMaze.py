import  operator
import cv2
import numpy as np
import random
from random import  randint
from copy import deepcopy
class Population:
    def __init__(self, maze, chromosome_length, population_size, mutation_rate, maze_width, maze_height):
        self.chromosome_length = chromosome_length
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.maze = maze
        self.temp_maze = deepcopy(maze)
        self.total_space = self.maze_width * self.maze_height - self.maze.mine_rate
        self.population = []
        for i in range(population_size):
            chromosome = []
            for j in range(chromosome_length):
                chr = [randint(0, maze_height - 1), randint(0, maze_width - 1)]
                chromosome.append(chr)
            self.population.append(chromosome)

    def openCell(self, cell):
        '''
        open given cell, first check is bomb or not ,
        then check for opened before, if it is not
        open that cell

        '''
        maze = self.temp_maze

        if cell.is_bomb == False:
            if cell.is_opened == False:
                c = maze.groups_index[cell.group_id]
                for row in c:
                    for clm in row:
                        if clm.is_bomb == False:
                            maze.cells[clm.cell_id[0]][clm.cell_id[1]].color = (0.7, 0.7, 0.7)
                            maze.cells[clm.cell_id[0]][clm.cell_id[1]].is_opened = True

                maze.cells[cell.cell_id[0]][cell.cell_id[1]].color=(0,0,0)
                self.draw(350)
                maze.cells[cell.cell_id[0]][cell.cell_id[1]].color = (0.7, 0.7, 0.7)
            return 1
        else:
            for bomb in maze.mine_index:
                maze.cells[bomb[0]][bomb[1]].color = (0, 0, 1)

            maze.cells[cell.cell_id[0]][cell.cell_id[1]].color = (0, 0, 0)
            self.draw(350)
            return 0

    def draw(self,mnt):
        '''
        draw maze with cv2 librariy, show it
        till given mnt paramter miliseconds

        '''
        maze = self.temp_maze
        maze_image = []

        for i in range(self.maze_width):
            temp = []
            for j in range(self.maze_height):
                temp.append(maze.cells[i][j].color)
            maze_image.append(temp)

        resized = cv2.resize(np.array(maze_image), (self.maze_width, self.maze_height))
        header="Generation: "+str(self.pop_count_print)
        cv2.namedWindow(header, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(header,500,500)
        cv2.moveWindow(header,500,200)
        cv2.imshow(header, resized)
        cv2.waitKey(mnt)


    def calculateFitness(self,pop_count_print):
        '''
        calculate fitness of chromosome
        first cell opens for any chromosome then
        calculate area of that chormosome opened
        if area is equal to (maze area- area covered by bomb)
        this chromosome solve the maze. Other way chromosome hit the bomb
        and take this area whic is opened by that choromosome
        as fintessy

        '''

        self.pop_count_print=pop_count_print
        opened_area = []
        for i in range(self.population_size):
            count=0
            for j in range(self.chromosome_length):
                row, column = self.population[i][j][0], self.population[i][j][1]
                cell = self.temp_maze.cells[row][column]
                return_value=self.openCell(cell)
                if(return_value==0):
                    self.temp_maze = deepcopy(self.maze)
                    break

            for k in range(self.maze_height):
                for l in range(self.maze_width):
                    if self.temp_maze.cells[k][l].is_opened == True:
                        count += 1

            if count == self.total_space:
                for bomb in self.temp_maze.mine_index:
                    self.temp_maze.cells[bomb[0]][bomb[1]].color = (1, 1, 1)
                self.draw(0)
                return 1
            else:
                opened_area.append(count / self.total_space)

        return opened_area

    def mutation(self):
        '''
        go through all chromosome ,
        pick cells(gene) randomly to change location
        '''
        for i in range(self.population_size):

            for j in range(int(self.mutation_rate*self.chromosome_length)):
                x= randint(0,2)
                index=randint(0,self.chromosome_length-1)
                if x == 0:
                    self.population[i][index][0]=randint(0,self.maze_height-1)
                if x==1:
                    self.population[i][index][1] = randint(0, self.maze_width - 1)
                if x==2:
                    self.population[i][index][0] = randint(0, self.maze_height - 1)
                    self.population[i][index][1] = randint(0, self.maze_width - 1)


    def sortPopulation(self,opened_area):
        '''
        sort fintess of chromosemes,
        return index of  that chromosomes
        '''
        dif_dict = {}
        sorted_indexes = []
        for i in range(self.population_size):
            dif_dict[i] = opened_area[i]
        temp = sorted(dif_dict.items(), key=operator.itemgetter(1),reverse=True)
        for i in range(self.population_size):
            sorted_indexes.append(temp[i][0])
        return sorted_indexes

    def crossingOver(self,chromosome1,chromosome2):

        '''
        crossing over with order based algorithm
        '''
        template = [randint(0, 1) for _ in range(self.chromosome_length)]

        child1 = deepcopy(chromosome1)
        child2 = deepcopy(chromosome2)

        for i in range(self.chromosome_length):

            if template[i] == 0:
                temp = child1[i]
                child1[i] = child2[i]
                child2[i] = temp

        return (child1, child2)


    def selection(self, sorted_indexes):
        '''
        Select chromosome according to fitness function,
        if chromosome has high fitness rate then that
        chromosome will appear high rate in selection array
        '''

        selection = []
        new_select = []
        size = self.population_size * (self.population_size + 1) / 2
        for i in range(self.population_size):
            for j in range(self.population_size - i):
                selection.append(sorted_indexes[i])

        random.shuffle(selection)
        random_index = random.randint(0, size - 1)
        new_select.append(selection[random_index])
        for i in range(self.population_size - 1):
            random_index = random.randint(0, size - 1)
            while (new_select[-1] == selection[random_index]):
                random_index = random.randint(0, size - 1)
            new_select.append(selection[random_index])
        return new_select
