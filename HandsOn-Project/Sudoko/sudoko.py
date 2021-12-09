import numpy as np
import random
import copy
import time
ROWS = 9
COLS = 9
POP_SIZE = 200 #1000
CROSSOVER_P = 1 #0.8
MUTATION_P = 1 #0.8
SELECTION_P = 0.7 #0.6 
random.seed(time.time())

class population:
    def __init__(self, initial_chromosome, size):
        self.startover(initial_chromosome, size)
    
    def startover(self, initial_chromosome, size):
        self.crossover_p = CROSSOVER_P
        self.mutation_p = MUTATION_P
        self.selection_p = SELECTION_P
        self.initial_chromosome = initial_chromosome
        self.popz = []
        for s in range(size):
            new_chromosome = chromosome(initial_chromosome)
            new_chromosome.set_fitness()
            self.popz.append(new_chromosome)
        self.popz.sort(key=lambda x: x.fitness, reverse=False)

    def build_next_population(self):
        new_generation = []
        #old_generation = []
        for i in range(0, len(self.popz) - 1):
            index1 = i
            r = random.uniform(0, 1)
            if r > self.selection_p:
                #old_generation.append(self.popz[index1])
                continue
            index2 = i + 1
            first_chrom = self.popz[index1]
            second_chrom = self.popz[index2]
            r = random.uniform(0, 1)
            if r < self.crossover_p:
                chromosome1, chromosome2 = self.generate_by_crossover(first_chrom, second_chrom)
                new_generation.append(chromosome1)
                new_generation.append(chromosome2)
        
        for i in range(0, len(self.popz)):
            first_chrom = self.popz[i]
            r = random.uniform(0, 1)
            if r < self.mutation_p:
                # you can use generate_by_mutation or generate_by_mutation2 for a different solve
                chromosome1 = self.generate_by_mutation(first_chrom)
                new_generation.append(chromosome1)
        print("New generation size is: ", len(new_generation))
        self.popz = self.popz + new_generation
        self.popz.sort(key=lambda x: x.fitness, reverse=False)
        del self.popz[POP_SIZE: ]
        # self.popz = self.popz + old_generation
        # self.popz.sort(key=lambda x: x.fitness, reverse=False)
        #del self.popz[POP_SIZE: ]
        if self.popz[POP_SIZE//20].fitness == self.popz[0].fitness:
            print("Updated Mutation Chance")
            self.mutation_p += 0.2
        else:
            self.mutation_p = MUTATION_P
        if self.popz[POP_SIZE//10].fitness == self.popz[0].fitness:
            print("Updated Crossover Chance")
            self.crossover_p += 0.1
        else:
            self.crossover_p = CROSSOVER_P
        # if self.popz[POP_SIZE - 1].fitness == self.popz[0].fitness:
        #     print("Starting Over")
        #     self.startover(self.initial_chromosome, POP_SIZE)
        # else:
        #     self.selection_p = SELECTION_P
        
    def generate_by_crossover(self, first_chrom, second_chrom):
        starting_row = random.randint(0, ROWS - 1)
        length_crossover = random.randint(1, ROWS - 1)
        chromosome1 = chromosome(first_chrom.genes)
        chromosome2 = chromosome(second_chrom.genes)
        for row in range(starting_row, starting_row + length_crossover):
            for col in range(COLS):
                chromosome1.genes[row % ROWS][col], chromosome2.genes[row % ROWS][col] = chromosome2.genes[row % ROWS][col], chromosome1.genes[row % ROWS][col]
        chromosome1.set_fitness()
        chromosome2.set_fitness()
        return chromosome1, chromosome2
    def generate_by_mutation(self, first_chrom):
        chosen_row = random.randint(0, ROWS - 1)
        chosen_col1 = random.randint(0, COLS - 1)
        while self.initial_chromosome[chosen_row][chosen_col1] != 0:
            chosen_col1 = random.randint(0, COLS - 1)
        chosen_col2 = random.randint(0, COLS - 1)
        while chosen_col2 == chosen_col1 or self.initial_chromosome[chosen_row][chosen_col2] != 0:
            chosen_col2 = random.randint(0, COLS - 1)
        chromosome1 = chromosome(first_chrom.genes)
        chromosome1.genes[chosen_row][chosen_col1], chromosome1.genes[chosen_row][chosen_col2]  = chromosome1.genes[chosen_row][chosen_col2], chromosome1.genes[chosen_row][chosen_col1] 
        chromosome1.set_fitness()
        return chromosome1
    def generate_by_mutation2(self, first_chrom):
        chosen_row = random.randint(0, ROWS - 1)
        chosen_col1 = random.randint(0, COLS - 1)
        while self.initial_chromosome[chosen_row][chosen_col1] != 0:
            chosen_col1 = random.randint(0, COLS - 1)
        chromosome1 = chromosome(first_chrom.genes)
        value = random.randint(1, 9)
        while (chromosome1.is_candidate(chosen_row, chosen_col1, value)):
            value = random.randint(1, 9)
        chromosome1.genes[chosen_row][chosen_col1] = value  
        chromosome1.set_fitness()
        return chromosome1
class chromosome:
    def __init__(self, genes):
        self.initial = copy.deepcopy(genes) #nmd byd deep copy she ya na
        self.genes = copy.deepcopy(genes)
        self.fill_genes()
    def is_candidate(self, row, col, value):
        cnt = 0
        for c in range(COLS):
            if self.initial[row][c] == value:
                cnt += 1
        if cnt > 0:
            return False
        for r in range(ROWS):
            if self.initial[r][col] == value:
                cnt += 1
        if cnt > 0:
            return False
        grid_i = 3 * (row // 3)
        grid_j = 3 * (col // 3)
        for i in range(0, ROWS//3):
            for j in range(0 , COLS//3):
                if self.initial[grid_i + i][grid_j + j] == value:
                    cnt += 1
        if cnt > 0:
            return False
        return True
    def set_fitness(self):
        self.fitness = self.calc_fitness()
    def fill_genes(self):
        #                               uncomment for a different solve

        # for row in range(ROWS):
        #     for col in range(COLS):
        #         if self.genes[row][col] == 0:
        #             rand_index = random.randint(1, 9)
        #             while (self.is_candidate(row, col, rand_index) ==  False):
        #                 rand_index = random.randint(1, 9)
        #             self.genes[row][col] = rand_index
                    

        #                    comment the following lines if you want to change the solve
        for row in range(ROWS):
            fillable = self.get_fillable_values(row)
            for col in range(COLS):
                if self.genes[row][col] == 0:
                    rand_index = random.randint(0, len(fillable) - 1)
                    self.genes[row][col] = fillable[rand_index]
                    fillable.pop(rand_index)
    def calc_fitness(self):
        sum = 0
        for row in range(ROWS):
            for col in range(COLS):
                value = self.genes[row][col]
                sum += self.find_occurrence_in_row(row, value)
                sum += self.find_occurrence_in_col(col, value)
                sum += self.find_occurrence_in_grid(row, col, value)
        return sum
    def get_fillable_values(self, row):
        fillable = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for c in range(COLS):
            if self.genes[row][c] in fillable:
                fillable.remove(self.genes[row][c])
        return fillable
    def find_occurrence_in_row(self, row, value):
        cnt = 0
        for c in range(COLS):
            if self.genes[row][c] == value:
                cnt += 1
        return cnt
    def find_occurrence_in_col(self, col, value):
        cnt = 0
        for r in range(ROWS):
            if self.genes[r][col] == value:
                cnt += 1
        return cnt
    def find_occurrence_in_grid(self, row, col, value):
        cnt = 0
        grid_i = 3 * (row // 3)
        grid_j = 3 * (col // 3)
        for i in range(0, ROWS//3):
            for j in range(0 , COLS//3):
                if self.genes[grid_i + i][grid_j + j] == value:
                    cnt += 1
        return cnt

if __name__ == '__main__':
    input = np.loadtxt("./SampleSudoku/Test1.txt", dtype=int, delimiter=' ')
    sample_pop = population(input, POP_SIZE)
    while 1:
        if sample_pop.popz[0].fitness == 243:
            print("FOUND AN ANSWER!")
            print(sample_pop.popz[0].genes)
            #np.savetxt("ans1.txt", np.array(sample_pop.popz[0].genes, dtype = int), delimiter=' ')
            break
        for popu in sample_pop.popz[0: 15]:
            print(popu.fitness, end=' ')
        print()
        print()
        sample_pop.build_next_population()
    