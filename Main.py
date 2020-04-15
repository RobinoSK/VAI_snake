import time
import Population
import Snake
import pygame as pg
import random as rd
import sys
import os


x = 10
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

def invalid(message = None):
    """
    Výpis hlášky v prípade chyby alebo nesprávneho volania skriptu
    """

    print('INCORRECT USAGE...\n1) To let a specific snake play: python main.py snake {id} {generation}\n2) To run a new population: python main.py {number of snakes} {number of generations}\n3) To load and continue a population: python main.py population {id} {generation}')

    # V prípade doplnkovej správy, zobraz oddelene pre prehľadnosť
    if message != None:
        print('-' * 100)
        print(message)

#............................................................

def main():

    # Nová populácia hadov
    if len(sys.argv) == 3:

        # Kontrola správnosti vstupov
        try:
            size = int(sys.argv[1])
            gens = int(sys.argv[2])
        except ValueError:
            invalid("The inputs must be integers")

        if size < 0 or gens < 0:
            invalid('The inputs must be positive integers.')
            return
        if size < 50:
            invalid('Use at least 50 snakes, otherwise the training does not make much sense.')
            return

        pop = Population.population(size)  # Vytvorenie novej populácie
        folder = 'Data\\Pop_' + str(pop.id)

        # Uistenie, že nebudeme prepisovať dáta už existujúcej populácie
        while os.path.exists(folder):
            pop.id = rd.randint(1, 100000)
            folder = 'Data\\Pop_' + str(pop.id)

        width = 600  # Šírka okna
        height = 600  # Výška okna
        pg.init()
        win = pg.display.set_mode((width, height))  # Zobrazovacia "plocha"
        clock = pg.time.Clock()  # Časovanie
        pg.event.get()
        iterations = gens  # Počet generácii
        it = 1

        while it <= iterations:

           pop.runGeneration(win)  # Priebeh jednej generácie
           it += 1

        return

    # Použitie existujúcich dát
    elif len(sys.argv) == 4:

        # Kontrola správnosti vstupov
        try:
            id = int(sys.argv[2])
            generation = int(sys.argv[3])
        except ValueError:
            invalid("The inputs must be integers")
            return
        if id < 0 or generation < 0:
            invalid('The inputs must be positive integers.')
            return

        # Spustenie konkrétneho hada
        if sys.argv[1].lower() == 'snake':

            s = Snake.snake(500, 300)  # Počatie hada s väčšou životnosťou
            filename = 'Pop_' + str(id) + '\\Snakes\\Pop_' + str(id) + '_gen_' + str(generation)  # Hlavička súborov s uloženou neurónovu sieťou
            # Pokus o načítanie a prípadná chyba
            try:
                s.load(filename)
            except OSError:
                print("Could not open the file with snake data, check if such file exists")
                return

            width = 600  # Šírka okna
            height = 600  # Výška okna
            pg.init()
            win = pg.display.set_mode((width, height))  # Zobrazovacia "plocha"
            clock = pg.time.Clock()  # Časovanie
            pg.event.get()

            # Nechaj hada hrať kým neumrie
            while s.alive:

               pg.time.delay(2)
               for event in pg.event.get():
                   if event.type == pg.QUIT:
                       sys.exit()
               clock.tick(120)  # Max FPS

               s.look()  # Získaj vstupy
               s.setDirection()  # Získaj smer pohybu
               s.move()  # Pohni hada
               s.show(win)  # Ukáž hada
            return

        # Pokračovanie v trénovaní populácie
        elif sys.argv[1].lower() == 'population':
            pop = Population.population(1, generation)  # Vytvorenie populácie
            filename = 'Data\\Pop_' + str(id) + '\\Generations\\Pop_' + str(id) + '_gen_' + str(generation) + '.csv'  # Súbor s dátami o sietiach hadov danej generácie a populácie
            # Pokus o načítanie a prípadná chyba
            try:
                pop.loadPopulation(filename)
            except OSError:
                print("Could not open the file with population data, check if such file exists")
                return

            pop.id = id  # Prepíš id populácie na správnu
            width = 600  # Šírka okna
            height = 600  #Výška okna
            pg.init()
            win = pg.display.set_mode((width, height))  # Zobrazovacia "plocha"
            clock = pg.time.Clock()  # Časovanie
            pg.event.get()
            iterations = 50  # Pokračovanie stanovené na 50 generácii
            it = 1

            while it <= iterations:

               pop.runGeneration(win)  # Priebeh jednej generácie
               it += 1

            return

        # Nesprávne uvedená možnosť
        else:
            invalid("INVALID OPTION: use 'snake' or 'population' as the first argument.")
            return
        return

    # Nesprávne volanie skriptu
    else:
        invalid()
        return
    return

#............................................................

if __name__ == "__main__":
    main()
