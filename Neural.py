import numpy as np
import random as rd
import copy


class neural(object):
    """
    Trieda reprezentujúca neurónovú sieť
    """

#............................................................

    def __init__(self, inp, outp):
        """
        Vytvorenie neurónovej siete

        inp - počet vstupných neuronov
        outp - počet výstupných neurónov
        """

        # Koeficienty neurónovej siete sú inicializované náhodne v rozpätí od -1 do 1, tento interval nikdy neopustia
        self.Wout = np.random.rand(outp, inp) * 2 - np.ones([outp, inp])  # Váhy výstupnej vrstvy

        # Stĺpcový vektor
        self.Bout = np.random.rand(outp, 1) * 2 - np.ones([outp, 1])  # Bias výstupnej vrstvy

#............................................................

    def save(self, filename):
        """
        Uloženie koeficientov neorónovej siete do podpriečinku Data/. Knižnica numpy má preddefinovaé ukladanie numpy arrayov
        """

        name1 = 'Data\\' + filename + '_Wout.npy'
        name2 = 'Data\\' + filename + '_Bout.npy'

        np.save(name1, self.Wout)
        np.save(name2, self.Bout)

#............................................................

    def load(self, filename):
        """
        Načítanie parametrov neurónovej siete z podpriečinku Data. Knižnica numpy má preddefinovaé čítanie numpy arrayov
        """

        name1 = 'Data\\' + filename + '_Wout.npy'
        name2 = 'Data\\' + filename + '_Bout.npy'

        self.Wout = np.load(name1)
        self.Bout = np.load(name2)

#............................................................

    def output(self, inputval):
        """
        Vypočíta výstup neurónovej siete

        inputval - vstupné hodnoty, v našom prípade hadove videnie
        """

        # inputval - stĺpcový vektor
        return self.sigmoid(np.dot(self.Wout, inputval) + self.Bout)

#............................................................

    def sigmoid(self,x):
        """
        Vykonáva aktivačnú funkciu neurónovej siete, sigmoid
        """

        return 1 / (1 + np.exp(-x))

#............................................................

    def mutate(self, probability):
        """
        Mutácia hadovho génu, náhodné zmeny v parametroch hadovho mozgu s danou pravdepodobnosťou
        """

        self.Bout = self.mutateArray(self.Bout, probability)
        self.Wout = self.mutateArray(self.Wout, probability)

#............................................................

    def mutateArray(self, arr, probability):
        """
        Pomocná funkcia na mutáciu numpy arrayu
        """

        hshape = np.shape(arr)  # Dimenzia arrayu
        result = copy.deepcopy(arr)

        for i in range(hshape[0]):
            for j in range(hshape[1]):

                rnd = rd.random()
                if rnd < probability:

                    result[i][j] = result[i][j] + np.random.normal()/5  # Pripočítanie čísla z normálneho rozdelenia
                # Udržanie parametru v medzi -1 až 1
                if result[i][j] > 1:
                    result[i][j] = 1
                if result[i][j] < -1:
                    result[i][j] = -1

        return result
