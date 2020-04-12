import pygame as pg
import numpy as np
import random as rd
import Snake
import Neural
import copy
import csv
import sys
import os


class population(object):
    """
    Trieda reprezentujúca populáciu hadov
    """
#............................................................

    def __init__(self, size, gen=1):
        """
        Konštruktor populáciu hadov
        """

        self.snakes = []  # List všetkých hadov
        self.size = size  # Počet hadov v populácii

        self.generation = gen  # Číšlo generácie
        self.bestfitness = 0  # Najlepšie fitness ohodnotenie
        self.bestfitnessindex = 0  # Index hada s najelpším fitness ohodnotením
        self.mutationrate = 0.01  # Pravdepodobnosť mutácie
        self.bestsnakeIndex = 0
        self.id = rd.randint(1, 100000)  # Id populácie, pre zapisovanie do súboru

        for i in range(size):
            self.snakes.append(Snake.snake())

        self.bestsnake = copy.deepcopy(self.snakes[0]) # najlepši had na základe fitness

#............................................................

    def crossoverSnakes(self, snake1, snake2):
        """
        Kríženie jedincov
        """

        child = Snake.snake()  # Predchystanie nového hada
        child.brain = self.crossoverBrains(snake1.brain, snake2.brain)  # Premiešanie génov

        return child

#............................................................

    def crossoverBrains(self, brain1, brain2):
        """
        Kríženie, miešanie génov - koeficientov mozgu
        """

        chbrain = Neural.neural(24, 4)  # Predchystanie neurónovej siete
        # Kríženie jednotlivých numpy arrayov, váh a biasov
        chbrain.Wout = self.crossoverArray(brain1.Wout, brain2.Wout)
        chbrain.Bout = self.crossoverArray(brain1.Bout, brain2.Bout)

        return chbrain

#............................................................

    def crossoverArray(self, arr1, arr2):
        """
        Pomocné kríženie dvoch numpy arrayov
        """

        hshape = np.shape(arr1)  # Dimenzia arrayu
        # Kríženie spravíme tak, že vyberieme náhodný element z arrayu, ktorý bude hranica medzi vloženými génmi prvého a génmi druhého hada
        randrow = rd.randint(0, hshape[0] - 1)
        randcol = rd.randint(0, hshape[1] - 1)

        result = np.zeros(hshape)  # Nachystanie výsledného arrayu

        for i in range(hshape[0]):
            for j in range(hshape[1]):

                if i < randrow or (i == randrow and j <= randcol):
                    result[i][j] = arr1[i][j]
                else:
                    result[i][j] = arr2[i][j]

        return result

#............................................................
    def setBestsnake(self):
        """
        Nájde najlepšieho hada z aktuálnej generácie podla jeho fitness hodnoty
        """

        top = 0  # Najlepšie fitness ohodnotenie
        ind = 0  # Index hada s najlepším fitness
        # Nájdenie najlepšieho v liste hadov
        for i in range(len(self.snakes)):
            if self.snakes[i].fitness > top:
                top = self.snakes[i].fitness
                ind = i

        self.bestfitness = top
        self.bestfitnessindex = ind
        self.bestsnake = copy.deepcopy(self.snakes[ind])

#............................................................

    def mutate(self, mutationrate):
        """
        Vykoná mutáciu každého hada v populácii
        """

        for snake in self.snakes:
            snake.mutate(mutationrate)

#............................................................

    def selectSnake(self, collection):
        """
        Náhodný výber hada z generacie. Čím má had väčší fitness, tým je pravdepodobnejšie,
        že bude vybraný
        """

        fitsum = 0  # Celková suma fitnessov
        for snake in collection:
            fitsum += snake.fitness

        rand = rd.random() * fitsum  # Náhodné vybratie

        runsum = 0
        for snake in collection:
            runsum += snake.fitness
            if runsum > rand:  # Jedna z možností, ako simulovať diskrétnu pravdepodobnostnú funkciu
                return copy.deepcopy(snake)

#............................................................

    def duplicates(self, lst, item):
        """
        Nájde indexy duplikátov.
        """
        # Nakoniec nepoužitá funkcia, ale nechávam ju tu

        return [i for i, x in enumerate(lst) if x == item]

#............................................................

    def selection(self):
        """
        Vykoná proces náhodného kríženia silných jedincov
        """

        self.getFitness()  # Aktualizácia fitness jednotlivých hadov
        newsnakes = []  # Nová generácia hadov

        self.setBestsnake()  # Stanov najlepšieho hada
        self.printmaxfit()  # Informuj o stave učenia
        tempsnake = Snake.snake()
        # Zachovaj najlešieho z predchádzajúce generácie
        tempsnake.brain = copy.deepcopy(self.bestsnake.brain)
        newsnakes.append(tempsnake)
        del tempsnake

        for i in range(1, len(self.snakes)):

            # Každý had bude rodičom nejakého ďalšieho hada, druhý rodič sa vyberie na základe fitness ohodnotenia
            parent1 = copy.deepcopy(self.snakes[i])
            parent2 = self.selectSnake(self.snakes)

            # Tvorba potomka + mutácia
            rand = rd.random()
            if rand > 0.5:
                child = self.crossoverSnakes(parent1, parent2)
            else:
                child = self.crossoverSnakes(parent2, parent1)
            rand = rd.random()
            if rand > 0.95:
               child.mutate(2 * self.mutationrate)
            else:
               child.mutate(self.mutationrate)
            newsnakes.append(child)

        del self.snakes
        self.snakes = []
        # Prekopírovanie nových hadov do zoznamu hadov
        for i in range(len(newsnakes)):
            self.snakes.append(Snake.snake())
            self.snakes[i] = copy.deepcopy(newsnakes[i])

        self.generation += 1

#............................................................

    def printmaxfit(self):
        """
        Vypísanie fitnessu najlešieho hada
        """

        print("Population #{}, generation #{} - FITNESS: {}".format(self.id, self.generation, self.bestfitness))

#............................................................

    def runGeneration(self,surface):
        """
        Prebehne jedna generácia hadov
        """

        while not self.finished():
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
            pg.time.delay(5)
            self.updateSnakes(surface)  # Vykonaj pohyb hadov

        self.getFitness()  # Spočítaj fitness hadov
        self.setBestsnake()  # Stanov najlepšieho hada
        self.selection()  # Vykonaj selekciu hadov do ďalšej generácie
        self.savePopulation()  # Ulož aktuálnu generáciu
        self.saveBest()  # Ulož najlepšieho hada

#............................................................

    def getFitness(self):
        """
        Spočíta fitness každého hada
        """

        for snake in self.snakes:
            snake.getFitness()

#............................................................

    def finished(self):
        """
        Zistí, či už všetky hady zomreli
        """

        for snake in self.snakes:
            if snake.alive:
                return False

        return True

#............................................................

    def updateSnakes(self,surface):
        """
        Vykoná ťah každého živého hada
        """

        for i in range(len(self.snakes)):
            if self.snakes[i].alive:
                self.snakes[i].look()  # Získaj vstupy siete
                self.snakes[i].setDirection()  # Zisti smer
                self.snakes[i].move()  # Vykonaj pohyb
                if self.snakes[i].alive and i == self.bestsnakeIndex:
                    pg.event.get()
                    self.snakes[i].show(surface)  # Vykreslenie, ak sa jedná o najlešpieho hada

        self.getbestsnakeIndex()

#............................................................

    def getbestsnakeIndex(self):
        """
        Zistí aktuálne najúspešnejšieho hada pre vykreslenie na obrazovku
        """

        if not self.finished():

            top = 0
            topindex = 0
            # Hľadanie najdlhšieho hada
            for i in range(len(self.snakes)):
                if self.snakes[i].alive and self.snakes[i].length > top:
                    top = self.snakes[i].length
                    topindex = i

            if not self.snakes[self.bestsnakeIndex].alive or top > self.snakes[self.bestsnakeIndex].length:
                self.bestsnakeIndex = topindex

#............................................................

    def saveBest(self):
        """
        Uloží parametre najlepšieho hada z generácie
        """

        filename = 'Pop_' + str(self.id) + '\\Snakes\\Pop_' + str(self.id) + '_gen_' + str(self.generation)
        self.snakes[self.bestfitnessindex].save(filename)

#............................................................

    def createNeural(self, row):
        """
        Z prečítaného riadku zo súboru vytvorí neurónovú sieť
        """
        result = Neural.neural(24, 4)  # Predchystanie siete

        Wo = np.zeros((4, 24))
        Bo = np.zeros((4, 1))

        # Dodržanie poradia, aké bolo pri zapisovaní riadkov
        r1 = row[0 : 4*24]
        r2 = row[4*24 : 4*24 + 4]

        for i in range(4):
            for j in range(24):
                Wo[i][j] = r1[i*24 + j]
        for i in range(4):
                Bo[i][0] = r2[i]

        result.Wout = copy.deepcopy(Wo)
        result.Bout = copy.deepcopy(Bo)

        return result

#............................................................

    def loadPopulation(self, filename):
        """
        Načíta populáciu hadov
        """
        readsnakes = []
        csv_file = open(filename,'r')
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:

            line_count += 1

            # Každý riadok reprezentuje hadov mozog
            if line_count % 2 == 1:
                tempsnake = Snake.snake()
                tempbrain = self.createNeural(row)

                tempsnake.brain = copy.deepcopy(tempbrain)

                readsnakes.append(tempsnake)
                del tempsnake
                del tempbrain

        del self.snakes
        self.snakes = copy.deepcopy(readsnakes)
        self.size = len(self.snakes)

#............................................................

    def savePopulation(self):
        """
        Uloží populáciu hadov
        """

        folder = 'Data\\Pop_' + str(self.id)
        if not os.path.exists(folder):
            os.makedirs(folder)
            os.makedirs(folder + '\\Generations')
            os.makedirs(folder + '\\Snakes')
        filename = folder + '\\Generations\\Pop_' + str(self.id) + '_gen_' + str(self.generation) + '.csv'
        with open(filename, mode='w') as datafile:
            datawriter = csv.writer(datafile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)


            for snake in self.snakes:


                Wo = self.convertMatrix(snake.brain.Wout)
                Bo = self.convertMatrix(snake.brain.Bout)

                scheme = Wo + Bo
                datawriter.writerow(scheme)

#............................................................

    def convertMatrix(self, arr):
        """
        Konverzia numpy arrayu do listu pre zapísanie do súboru
        """

        result = []
        hshape = np.shape(arr)

        for i in range(hshape[0]):
            for j in range(hshape[1]):
                result.append(str(arr[i][j]))

        return result
