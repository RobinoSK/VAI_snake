import numpy as np
import pygame as pg
import Neural
import Food


class snake(object):
    """
    Trieda reprezentujúca herného hada
    """
    # parametre herného okna
    height = 600
    width = 600

#............................................................

    def __init__(self, foodboost = 100):
        """
        Vytvorenie instancie hada
        """

        self.length = 1  # Dĺžka hada
        self.foodboost = foodboost  # Koľko sily pridá potrava hadovi
        self.head = np.array([round(self.width /2 ),round(self.height / 2)])  # Array obsahujúci pozíciu hlavy hada; x,y
        self.velocity = np.array([10, 0])  # Array obsahujúci smer pohybu hada; x,y
        self.body = []  # List obsahujúci celé telo hada

        self.sight = np.zeros([1, 24]).transpose()  # Vstupy do neuoronovej siete
        self.decision = np.zeros([1, 4]).transpose()  # Výstupy neuorónovej siete, hodnotenia smerov
        self.lifetime = 0  # Životnosť hada
        self.fitness = 0  # Hadovo ohodnotenie v rámci genetického algoritmu
        self.deathtime = 1000  # Čas dokým had umrie hladom
        self.growcount = 0  # O koľko had narastie
        self.alive = True  # Či je had nažive

        # Dáme hadovi hneď z úvodu nejaké to telo
        pieceone = np.array([self.head[0] - 30, self.head[1]])
        piecetwo = np.array([self.head[0] - 20, self.head[1]])
        piecethree = np.array([self.head[0] - 10, self.head[1]])
        self.body.append(pieceone)
        self.body.append(piecetwo)
        self.body.append(piecethree)
        self.length += 3

        self.brain = Neural.neural(24, 4) # Neurónova sieť hada
        self.food = Food.food(self.width, self.height) # aktuálna potrava, ktorú treba zjesť


#............................................................

    def setDirection(self):
        """
        Stanovenie smeru pohybu
        """
        # Použitie neurónovej siete na informácie z okolia
        self.decision = self.brain.output(self.sight)

        # Nájdeme maximum z outputov a ten prehlásime za víťazný smer, v ktorom sa had bude pohybovať
        ind = np.where(self.decision == np.amax(self.decision))[0]

        if ind == 0:
            self.velocity = np.array([10, 0])  # Doprava

        elif ind == 1:
            self.velocity = np.array([-10, 0])  # Dolava

        elif ind == 2:
            self.velocity = np.array([0, 10])  # Nahor

        elif ind == 3:
            self.velocity = np.array([0, -10])  # Nadol


#............................................................

    def save(self, filename):
        """
        Uloží údaje o danom hadovi, aby sa dali použiť neskôr, napríklad
        najlepší had z danej generácie pre neskoršie porovnávanie
        """

        # Jediné, čo treba uložiť je jeho sieť
        self.brain.save(filename)

#............................................................

    def load(self, filename):
        """
        Načíta údaje o hadovi
        """

        # Jediné, čo treba načítať je jeho sieť
        self.brain.load(filename)

#............................................................

    def mutate(self, probability):
        """
        Mutácia hadovho génu
        """

        # Mutácia koeficientov neurónovej siete
        self.brain.mutate(probability)

#............................................................

    def getFitness(self):
        """
        Vypočíta fitness ohodnotenie daného hada, ako veľmi je úspešný
        """

        if self.length < 10:
            self.fitness = self.lifetime * self.lifetime * (2 ** self.length)
        else:  # Ak je už had dostatočne dlhý, nebudeme brať jeho dĺžku za podstatnú
            self.fitness = self.lifetime * self.lifetime * (2 ** 10)

#............................................................

    def eat(self):
        """
        Spustí sa po zjedení potravy
        """

        self.food = Food.food(self.width,self.height)  # Nová potrava

        # Nechceme, aby sa potrava objavila na hadovi
        dummy = True
        while dummy:
            a = 0
            for pos in self.body:
                if np.array_equal(pos, self.food.pos):
                    self.food = Food.food(self.width, self.height)
                    break
                a += 1
            if np.array_equal(self.head, self.food.pos):
                self.food = Food.food(self.width, self.height)
            else:
                a += 1
            if a == len(self.body) + 1:  # Potrava neleží na hadovi
                dummy = False

        self.deathtime += self.foodboost  # Had sa najedol, žije dlhšie

        # O koľko narastie, pri dlhšom hadovi bude odmena za jedlo väčšia
        if self.length >= 10:
            self.growcount += 3
        else:
            self.growcount += 1

#............................................................

    def grow(self):
        """
        Pridá kus tela hadovi
        """

        self.body.append(self.head)
        self.length += 1

#............................................................

    def move(self):
        """
        Vykoná hadov pohyb
        """

        self.lifetime += 1
        self.deathtime -= 1

        if self.deathtime < 0:  # Had umrel
            self.alive = False

        # Had narazil a umrel
        if self.gonnaDie(self.head[0] + self.velocity[0], self.head[1] + self.velocity[1]):
            self.alive = False

        # Had narazil na potravu a zjedol ju
        if self.head[0] + self.velocity[0] == self.food.pos[0] and  self.head[1] + self.velocity[1] == self.food.pos[1]:
            self.eat()

        # Had má rásť, tak porastie
        if self.growcount > 0:
            self.growcount -= 1
            self.grow()
        else:
            # Posúvanie hadovho tela
            for i in range(len(self.body) - 1):
                temp = np.array([self.body[i + 1][0], self.body[i + 1][1]])
                self.body[i] = temp
            temp = np.array([self.head[0], self.head[1]])
            self.body[self.length-2] = temp

        # Posun hadovej hlavy
        self.head = np.add(self.head,self.velocity)

#............................................................

    def show(self, surface):
        """
        Zobrazí hada do pygame okna
        """

        surface.fill((0,0,0))
        for cube in self.body:
            # Biely obdĺžnik pre hadove telo
            pg.draw.rect(surface, (255, 255, 255), (cube[0], cube[1], 10, 10))

        # Modrý obdĺžnik pre hadovu hlavu
        pg.draw.rect(surface, (0, 0, 255), (self.head[0], self.head[1], 10, 10))
        pg.draw.rect(surface, (255, 0, 0), (self.food.pos[0], self.food.pos[1], 10, 10))
        pg.display.update()

#............................................................

    def gonnaDie(self, x, y):
        """
        Zistí, či had po vykonaní pohybu narazí buď do seba alebo do steny
        """

        # náraz do steny
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True

        # náraz do tela/chvostu
        return self.onTail(x, y)

#............................................................

    def onTail(self, x, y):
        """
        Zistí, či had narazil do svojho tela
        """

        # Pre každý kus tela sa pozrieme, či sa zhodujú súradnice so vstupom
        for cube in self.body:
            if x == cube[0] and y == cube[1]:
                return True

        return False

#............................................................

    def look(self):
        """
        Získa vstupy pre hadovu neurónovú sieť, videnie
        """

        self.sight = np.zeros([1, 24]).transpose()

        # Doprava
        values = self.lookDirection(np.array([10, 0]))
        self.sight[0][0] = values[0]
        self.sight[1][0] = values[1]
        self.sight[2][0] = values[2]

        # Doprava dole
        values = self.lookDirection(np.array([10, -10]))
        self.sight[3][0] = values[0]
        self.sight[4][0] = values[1]
        self.sight[5][0] = values[2]

        # Dole
        values = self.lookDirection(np.array([0, -10]))
        self.sight[6][0] = values[0]
        self.sight[7][0] = values[1]
        self.sight[8][0] = values[2]

        # Dolava dole
        values = self.lookDirection(np.array([-10, -10]))
        self.sight[9][0] = values[0]
        self.sight[10][0] = values[1]
        self.sight[11][0] = values[2]

        # Dolava
        values = self.lookDirection(np.array([-10, 0]))
        self.sight[12][0] = values[0]
        self.sight[13][0] = values[1]
        self.sight[14][0] = values[2]

        # Dolava hore
        values = self.lookDirection(np.array([-10, 10]))
        self.sight[15][0] = values[0]
        self.sight[16][0] = values[1]
        self.sight[17][0] = values[2]

        # Hore
        values = self.lookDirection(np.array([0, 10]))
        self.sight[18][0] = values[0]
        self.sight[19][0] = values[1]
        self.sight[20][0] = values[2]

        # Doprava hore
        values = self.lookDirection(np.array([10, 10]))
        self.sight[21][0] = values[0]
        self.sight[22][0] = values[1]
        self.sight[23][0] = values[2]

#............................................................

    def lookDirection(self, direction):
        """
        Získa informácie zo špecifického smeru
        """

        position = self.head # Prehľadávame od hlavy
        foundfood = False
        foundtail = False
        isfood = 0
        taildir = 0  # Vzdialenosť od tela
        walldir = 1  # Vzdialenosť od steny

        distance = 0  # Ako ďaleko prehľadávame
        position = np.add(position, direction)  # Úvodný prehľadávací pohyb
        distance += 1

        # Dívame sa až dokým nenarazíme na stenu
        while not (position[0] < 0 or position[0] >= self.width or position[1] < 0 or position[1] >= self.height):

            # Kontrola potravy
            if not foundfood and position[0] == self.food.pos[0] and position[1] == self.food.pos[1] :
                isfood = 1
                foundfood = True

            # Kontrola chvostu
            if not foundtail and self.onTail(position[0], position[1]):
                taildir = 1 / distance
                foundtail = True

            position = np.add(position, direction) # Posun v prehľadávaní
            distance += 1

            walldir = 1 / distance;

        return np.array([isfood, taildir, walldir])
#............................................................
