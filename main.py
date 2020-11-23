import random
import math
from GA import Gene, GA


def func(x):
    return -x * x * x + 10000 * x * x + math.sqrt(x) - 1


l = 1
r = 1e9
l = int(l)
r = int(r)


class FuncGene(Gene):
    encode_length = int(math.log10(r)) + 1
    variation_num = int(math.ceil(encode_length / 1000))

    def __init__(self):
        super().__init__()

    def random_gene(self) -> list:
        return self.encode(random.randint(l, r))

    def encode(self, x):
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
        temp = self.data.copy()
        for i in range(FuncGene.variation_num):
            pos = random.randint(0, FuncGene.encode_length - 1)
            self.data[pos] = random.randint(0, 9)
        if self.decode() > r or self.decode() < l:
            self.data = temp

    def cross(self, another_gene):
        pos = random.randint(0, FuncGene.encode_length - 1)
        gene = FuncGene()
        gene.data = self.data[:pos] + another_gene.data[pos:]
        if gene.decode() > r or gene.decode() < l:
            return self
        return gene


temp = GA(
    gene_generator=lambda: FuncGene()
)
temp.run()
