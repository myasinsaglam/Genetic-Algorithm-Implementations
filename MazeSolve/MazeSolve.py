import numpy as np
import cv2
import  random
import math
import operator
import copy
import matplotlib.pyplot as plt
import pylab as pl
matrix_size=61
shift_value=0.1
mid_value=0.5
obstacle_rate=0
chromosome_length=matrix_size*3#abs(int(matrix_size*shift_value)- int(matrix_size*mid_value))*5
population_size=600
mutation_rate=0
vardi=False

population_counts=[500,750,1000]
mutation_rates=[0.1,0.2,0.3]


xfinish=int(matrix_size*shift_value)
yfinish=int(matrix_size*shift_value)
xstart=int(matrix_size*mid_value)
ystart=int(matrix_size*mid_value)

def createMaze(size, shift_value=0.2, mid_value=0.5,obstacle_rate=0.1):
    maze=np.array(np.zeros(shape=(size,size)))
    maze[int(size*shift_value),int(size*shift_value)]=4 #renk atamasi
    maze[int(mid_value*size),int(mid_value*size)]=3

    for i in range(size):
        maze[i,0]=1
        maze[0,i]=1
        maze[size-1,i]=1
        maze[i,size-1]=1

    for i in range(int(size*obstacle_rate)):
        x=random.randint(1,(size-1))
        y = random.randint(1, (size - 1))

        while((x ==int(size*shift_value) and y==int(size*shift_value)) or (x ==int(size*mid_value) and y==int(size*mid_value))):
            x = random.randint(1, (size - 1))
            y = random.randint(1, (size - 1))

        maze[x,y]=1

    return maze

def showMaze(maze_array):
    length=np.shape(maze_array)[0]
    maze_image=np.array(np.zeros(shape=(length,length,3)))
    for i in range(length):
        for j in range(length):
            #background color assigment cv2=BGR
            if(maze_array[i,j]==0):
                maze_image[i,j,0]=255
                maze_image[i, j, 1] = 255
                maze_image[i, j, 2] = 255
            #obstacle color assignment
            elif maze_array[i,j]==1:
                maze_image[i, j, 0] = 0
                maze_image[i, j, 1] = 0
                maze_image[i, j, 2] = 0
            #path color assignment
            elif maze_array[i,j]==2:
                maze_image[i, j, 0] = 255
                maze_image[i, j, 1] = 0
                maze_image[i, j, 2] = 0
            #start color assignment
            elif maze_array[i,j]==3:
                maze_image[i, j, 0] = 204
                maze_image[i, j, 1] = 204
                maze_image[i, j, 2] = 0

            #finish color assignment
            elif maze_array[i, j] == 4:
                maze_image[i, j, 0] = 0
                maze_image[i, j, 1] = 255
                maze_image[i, j, 2] = 0

            # start color assignment
            else :
                maze_image[i, j, 0] = 0
                maze_image[i, j, 1] = 0
                maze_image[i, j, 2] = 255



    cv2.namedWindow("maze", flags=cv2.WINDOW_NORMAL)
    cv2.imshow("maze",maze_image)
    cv2.waitKey(10)

#create random initial chromosomes
def createPopulation(chromosome_length,population_size=10):
    population=np.array(np.zeros(shape=(population_size,chromosome_length)))

    for i in  range(population_size):
        for j in range (chromosome_length):
            population[i,j]=random.randint(1,4)


    return  population

#it moves chromosome
def move(chromosome,maze,length):
    global  vardi
    k=0
    i,j=int(matrix_size*mid_value),int(matrix_size*mid_value)
    temp,cost=3,0


    while k<length and temp!=4 and temp!=1:

        if chromosome[k] == 1:
            temp=maze[i,j-1]
            maze[i, j - 1] = 2
            j-=1
            cost-=int(matrix_size*0.1)

        elif chromosome[k] == 2:
            temp = maze[i-1, j ]
            maze[i-1, j ] = 2
            i-= 1
            cost-=int(matrix_size*0.1)

        elif chromosome[k] == 3:
            temp = maze[i, j +1]
            maze[i, j + 1] = 2
            j += 1
            cost+=int(matrix_size*0.1)

        elif chromosome[k] == 4:
            temp = maze[i + 1, j]
            maze[i +1, j] = 2
            i += 1
            cost+=int(matrix_size*0.1)

        elif temp==2:
            cost += int(matrix_size * 0.1)
        k+=1


    if temp == 1:
        cost += man_dist(xfinish,yfinish,i,j) * 2
        maze[i,j]=1



    if temp == 4:
        maze[i,j]=4
        #print("vardıııııı")
        vardi=True
        cost = 0
        showMaze(maze)
        cv2.waitKey(0)


    if(k==length):
        cost+=man_dist(xfinish,yfinish,i,j)
        maze[i,j]=5



    maze[int(matrix_size*mid_value),int(matrix_size*mid_value)]=3

    return  cost

def man_dist(a1,a2,b1,b2):
    return abs(a1-b1)+abs(a2-b2)


def crossingOver(population, selection_array,mutation_rate=0.3):

    new_population=[]
    #print("---------------------------------")

    for i in range(population_size):
        new_population.append(population[selection_array[i]])

#önceki crossover
    # # print("pop1", new_population[1])
    for i in range(0,population_size,2):
        rate=random.randint(1,9)
        comma=int((population_size*rate)/10)
        k=comma
        #print(comma)

        while(k<chromosome_length):
            new_population[i][k],new_population[i+1][k]=new_population[i+1][k],new_population[i][k]
            k+=1
    #
    #     # print("new Pop", new_population[1])

    for i in range(population_size):
        for j in range(int(population_size*mutation_rate)):
            new_population[i][random.randint(0,chromosome_length-1)]=random.randint(1,4)




    return new_population






maze = createMaze(matrix_size, shift_value, mid_value, obstacle_rate)

showMaze(maze)
results = []

for p in  range(len(population_counts)):
    population_size=population_counts[p]

    for m in range (len(mutation_rates)):
        mutation_rate=mutation_rates[m]

        cost = {}
        l = 0
        generation=0
        population = createPopulation(chromosome_length=chromosome_length, population_size=population_size)
        while(l<1):



            for i in range(population_size):
                temp_maze = copy.deepcopy(maze)
                cost[i]=move(population[i], temp_maze,chromosome_length)
            sorted_x = sorted(cost.items(), key=operator.itemgetter(1))
          # print(sorted_x)
            temp_maze1=copy.deepcopy(maze)
            bestcost=move(population[sorted_x[0][0]],temp_maze1,chromosome_length)
            showMaze(temp_maze1)
            new_select=[]
            for i in range(population_size):
                new_select.append(sorted_x[i][0])

            population=crossingOver(population=population,selection_array=new_select,mutation_rate=mutation_rate)

            if(vardi):

                results.append(generation)
                generation=0
                l+=1
                population = createPopulation(chromosome_length=chromosome_length, population_size=population_size)
                vardi=False

            generation+=1


np.save("results.npy",np.array(results))


data=np.load("results.npy")
#print(data)