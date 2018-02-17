from  Maze import Maze
from PopulationMaze import Population
import  random
import  cv2
import  numpy as np
import random as rand
maze_width=10
maze_height=10
population_size=12
group_w=2
group_h=2
chromosome_length=int((maze_height/group_h)*(maze_height/group_h)*2)
mutation_rate=0.1

pop_count_print = 0
finished=0

#create mazee and first population
maze=Maze(maze_height,maze_width,group_h,group_w)
pop=Population(maze,chromosome_length,population_size,mutation_rate,maze_width,maze_height)


#check for maze solved
while(finished !=1):

    opened_area=pop.calculateFitness(pop_count_print)

    if(opened_area==1):
        finished=1
        break

    #sort chromose according to fitness value then seleck some of them
    sorted_chromosome_indexes=pop.sortPopulation(opened_area)
    new_selected_chromosome=pop.selection(sorted_chromosome_indexes)

    #cross over selected chromosome
    new_population=[]
    for i in range (0,int(population_size/2),1):
        new_chr1, new_chr2=pop.crossingOver(pop.population[ new_selected_chromosome [i*2] ], pop.population[ new_selected_chromosome[(i*2)+1] ])
        new_population.append(new_chr1)
        new_population.append(new_chr2)

    #assing as new population and mutate som of them
    pop.population=new_population
    pop.mutation()

    pop_count_print+=1
    cv2.destroyAllWindows()


print("finished")

