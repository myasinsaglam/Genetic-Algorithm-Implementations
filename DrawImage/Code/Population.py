from  Shape import  Shape
import  cv2
import  numpy as np
from  random import  randint
import  random
import  operator
import  math
from  PIL import Image, ImageDraw
from  matplotlib import  pyplot as plt




class Population:
    #algoritma parametreleri kullanicidan alinarak populasyon olusturuluyor
    def __init__(self,Chromosome_Length,Population_Size,mutation_rate,shapeType,image,picture_h,picture_w):
        self.chromosome_length=Chromosome_Length
        self.population_size=Population_Size
        self.shapeType=shapeType
        self.picture_h=picture_h
        self.picture_w=picture_w
        self.original_image=image
        self.mutation_rate=mutation_rate

        self.population=[]
        for i in range(Population_Size):
            chromosome = []
            for j in range(Chromosome_Length):
                chromosome.append(Shape(shapeType,picture_h,picture_w))
            self.population.append(chromosome)

    def draw(self,chromosome):
    #Verilen kromozomun resmini cizen ve cizimi disari donduren fonksiyon
        # frame = np.zeros((self.picture_w, self.picture_h, 3), np.uint8)
        # output = np.zeros((self.picture_w, self.picture_h, 3), np.uint8)
        image = Image.new('RGB', (self.picture_w, self.picture_h), color="white")
        draw = ImageDraw.Draw(image, "RGBA")

        for i in range(self.chromosome_length):
            if chromosome[i].type == "circle":
                    c=chromosome[i]
                    draw.ellipse((c.x, c.y, (c.x+2*c.r), (c.y+2*c.r)), fill=(c.R, c.G, c.B, c.A),outline=(c.R, c.G, c.B, c.A))

                    # cv2.circle(frame, (c.x, c.y), c.r, (c.B, c.G, c.R), -1)
                    # cv2.addWeighted(frame, 0.1, output, 1 - 0.1, 0, output)

            if chromosome[i].type == "rectangle":
                    c=chromosome[i]
                    draw.rectangle((c.x, c.y, (c.x+c.w), (c.y +c.h)), fill=(c.R, c.G, c.B, c.A))
                    # cv2.rectangle(frame, (c.x, c.y), (c.w, c.h), (c.B, c.G, c.R ), -1)
                    # cv2.addWeighted(frame, 0.1, output, 1 - 0.1, 0, output)
        return image


    def fitness(self,image):
    # verilen iki resmin(cizim ve orijinal) pixel bazindaki oklit mesafesi hesaplaniyor
        diff =0
        for i in range(self.picture_w):
            for j in range(self.picture_h):
                r1,g1,b1 = image.getpixel((i,j))

                r2,g2,b2 = self.original_image.getpixel((i,j))
                d1=abs(r1-r2)
                d2=abs(g1-g2)
                d3=abs(b1-b2)

                diff+=(d1+d2+d3)

        return int(diff/3)

#hesaplanan mesafeler siralanarak sirali kromozom indisleri cross over icin disari donduruluyor
    def sortPopulation(self,differences):
        dif_dict={}
        sorted_indexes=[]
        for i in range(self.population_size):
            dif_dict[i]=differences[i]
        temp = sorted(dif_dict.items(),key=operator.itemgetter(1))
        for i in range(self.population_size):
            sorted_indexes.append(temp[i][0])
        return sorted_indexes

    def crossingOver(self, chromosome1, chromosome2):

        template = [randint(0, 1) for _ in range(self.chromosome_length)]

        child1 = chromosome1
        child2 = chromosome2

        for i in range(self.chromosome_length):

            if template[i] == 0:
                temp = child1[i]
                child1[i] = child2[i]
                child2[i] = temp

        return (child1, child2)

    def mutation(self, chromosome):

        for i in range(int(self.chromosome_length * self.mutation_rate)):

            mutation_type = randint(1,2)
            gnome_index = randint(0, self.chromosome_length-1)

            # change location
            if mutation_type == 1:

                if chromosome[gnome_index].type=="circle":
                    chromosome[gnome_index].x = randint(0, (self.picture_w - 2*chromosome[gnome_index].r))
                    chromosome[gnome_index].y = randint(0, (self.picture_h - 2*chromosome[gnome_index].r))
                elif chromosome[gnome_index].type=="rectangle":
                    chromosome[gnome_index].x = randint(0, self.picture_w - chromosome[gnome_index].w)
                    chromosome[gnome_index].y = randint(0, self.picture_h - chromosome[gnome_index].h)

            # change color
            if mutation_type == 2:
                rand=random.randint(1,4)
                if rand==1:
                    chromosome[gnome_index].R = random.randrange(0, 255)
                if rand==2:
                    chromosome[gnome_index].G = random.randrange(0, 255)
                if rand==3:
                    chromosome[gnome_index].B = random.randrange(0, 255)
                if rand==4:
                    chromosome[gnome_index].A = random.randrange(0, 256)

    def selection(self, sorted_indexes):
        # yeni populasyon indislerini siralama secimi yaparak cross over icin disari donduren fonksiyon
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
