import random
import math
from GA import Gene, GA
import numpy as np
import matplotlib.pyplot as plt


def func(x):
    return np.log(np.abs(-(x - 5e6) * (x - 1e6) * (-2 * x + 2e6) * (x - 3e6) * (x - 4e6) * (-x + 6e6)) + 1)


l = 0.5e6
r = 6e6
l = int(l)
r = int(r)


class FuncGene(Gene):
    encode_length = int(math.log10(r)) + 1
    variation_num = int(math.ceil(encode_length / 1000))

    def __init__(self):
        super().__init__()

    def random_gene(self) -> list:
        return self.encode(random.randint(l, r))

    @staticmethod
    def encode(x):
        if x < 0:
            raise Exception(f'Number: {x} is negative')
        temp = [ord(i) - ord('0') for i in str(x)]
        t = FuncGene.encode_length - len(temp)
        if t < 0:
            raise Exception(f'Number: {x} is too big to encode with length: {FuncGene.encode_length}')
        return [0] * t + temp

    def decode(self):
        s = ''
        for i in self.data:
            s += chr(ord('0') + i)
        res = int(s)
        return res

    @property
    def fitness(self) -> float:
        return func(self.decode())

    def vary(self):
        for i in range(FuncGene.variation_num):
            pos = random.randint(0, FuncGene.encode_length - 1)
            self.data[pos] = random.randint(0, 9)
        if self.decode() > r:
            self.data = self.encode(r)
        if self.decode() < l:
            self.data = self.encode(l)

    def cross(self, another_gene):
        pos = random.randint(0, FuncGene.encode_length - 1)
        gene = FuncGene()
        gene.data = self.data[:pos] + another_gene.data[pos:]
        if gene.decode() > r:
            gene.data = self.encode(r)
        if gene.decode() < l:
            gene.data = self.encode(l)
        return gene


plt.ion()
x = np.linspace(l, r, 100000)
y = func(x)
plt.figure()


def paint(genes):
    plt.xlim((l, r))
    plt.cla()
    plt.title(f'Now answer: x={genes[0].decode()}, y={genes[0].fitness}')
    plt.plot(x, y)
    plt.plot([gene.decode() for gene in genes], [gene.fitness for gene in genes], '.r', ms=0.5)
    plt.pause(1)


class FuncGA(GA):
    def before_one_generation(self, generation, genes):
        if generation != 1:
            return
        paint(genes)

    def after_one_generation(self, generation, genes):
        paint(genes)
        print(f'generation={generation}, x={genes[0].decode()}, y={genes[0].fitness}')


FuncGA(
    gene_generator=lambda: FuncGene(),
    variation_rate=0.1,
    safe_num=2000
).run()
plt.ioff()
plt.show()
