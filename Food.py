import random as rd
import numpy as np


class food(object):
    """
    Trieda reprezentujúca potravu, obsahuje súradnice potravy
    """

#............................................................

    def __init__(self, width, height):
        """
        K vytvoreniu instancie potravy stačí poznať šírku a výšku herného okna, počet pixelov na hernú bunku je pevne daný rovno 10
        """

        # Náhodné umiestnenie potravy
        x = round(rd.randint(0, (width-10) / 10)) * 10
        y = round(rd.randint(0, (height-10) / 10)) * 10
        # Reprezentované array z numpy knižnice
        self.pos = np.array([x, y])
