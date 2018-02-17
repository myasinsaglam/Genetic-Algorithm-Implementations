from  Population import  Population
from  PIL import Image, ImageDraw
import  os
from  matplotlib import  pyplot as plt


original_image=Image.open("cocacola.jpg")
image_width=50
image_height=50
original_image.thumbnail((image_height,image_width),Image.ADAPTIVE)


chromosome_length= 50
population_size=2
mutation_rate=0.2
iteration=5000
shape_type="rectangle"




def main():



        p = Population(chromosome_length, population_size, mutation_rate, shape_type, original_image, image_height,
                       image_width)
        k=1
        while(k<=iteration):

            distances=[]
            for i in range(population_size):
                chromosome_image=p.draw(p.population[i])
                distances.append(p.fitness(chromosome_image))

            sorted_population_indexes=p.sortPopulation(distances)

            if k%(iteration)==0:

                #chromosome_image.save('resimler/ '+file_name+".png", 'PNG')
                 plt.imshow(chromosome_image)
                 plt.show()

            new_population_indexes=p.selection(sorted_population_indexes)

            new_population=[]
            for i in range(0,population_size,2):
                c1,c2=p.crossingOver(p.population[new_population_indexes[i]],p.population[new_population_indexes[i+1]])
                new_population.append(c1)
                new_population.append(c2)


            p.population = new_population

            for i in range(population_size):
                p.mutation(p.population[i])

            k+=1




main()





