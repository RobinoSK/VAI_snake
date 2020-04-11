import time
import Population
import Snake
import pygame as pg
import sys


x = 10
y = 30
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

def invalid(message=None):

    print('INCORRECT USAGE...\nTo let a specific snake play: python main.py snake {id} {generation}\nTo run a new population: python main.py {number of snakes} {number of generations}\nTo load and continue a population: python main.py population {id} {generation}')
    if message != None:
        print('-' * 100)
        print(message)

#............................................................

def main():

    if len(sys.argv) == 3:

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

        pop = Population.population(size)
        width = 600
        height = 600
        pg.init()
        win = pg.display.set_mode((width, height))
        clock = pg.time.Clock()
        pg.event.get()
        iterations = gens
        it = 1

        while it <= iterations:

           pop.runGeneration(win)
           it += 1

        return

    elif len(sys.argv) == 4:

        try:
            id = int(sys.argv[2])
            generation = int(sys.argv[3])
        except ValueError:
            invalid("The inputs must be integers")
            return
        if id < 0 or generation < 0:
            invalid('The inputs must be positive integers.')
            return
        # Play a snakes
        if sys.argv[1] == 'snake':

            s = Snake.snake(300)
            filename = 'Pop_' + str(id) + '_gen_' + str(generation)
            try:
                s.load(filename)
            except OSError:
                print("Could not open the file with snake data, check if such file exists")
                return

            width = 600
            height = 600
            pg.init()
            win = pg.display.set_mode((width, height))
            clock = pg.time.Clock()
            pg.event.get()

            while s.alive:

               pg.time.delay(2)
               for event in pg.event.get():
                   if event.type == pg.QUIT:
                       sys.exit()
               clock.tick(120)

               s.look()
               s.setDirection()
               s.move()
               s.show(win)
            return


        # Continue a generation
        elif sys.argv[1] == 'population':
            pop = Population.population(1, generation)
            filename = 'Pop_' + str(id) + '_gen_' + str(generation) + '.csv'
            try:
                pop.loadPopulation(filename)
            except OSError:
                print("Could not open the file with population data, check if such file exists")
                return

            pop.id = id
            width = 600
            height = 600
            pg.init()
            win = pg.display.set_mode((width, height))
            clock = pg.time.Clock()
            pg.event.get()
            iterations = 50
            it = 1

            while it <= iterations:

               pop.runGeneration(win)
               it += 1

            return

        # Invalid input
        else:
            invalid("INVALID OPTION: use 'snake' or 'population' as the first argument.")
            return
        return
    else:
        invalid()
        return
    return

#............................................................

if __name__ == "__main__":
    main()
