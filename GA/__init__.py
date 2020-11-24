import math
import random
from abc import ABC, abstractmethod


class Gene(ABC):
    def __init__(self):
        self._gene = self.random_gene()

    def __eq__(self, other):
        if not isinstance(other, Gene):
            return False
        return self._gene == other._gene

    @property
    def data(self):
        return self._gene

    @data.setter
    def data(self, val):
        self._gene = val

    @property
    @abstractmethod
    def fitness(self) -> float:
        pass

    @abstractmethod
    def random_gene(self) -> list:
        pass

    @abstractmethod
    def vary(self):
        pass

    @abstractmethod
    def cross(self, another_gene):
        pass


class GA:
    def __init__(self, gene_generator, **kwargs):
        self.genes = []
        self.gene_generator = gene_generator  # 随机基因生成器
        self.safe_num = kwargs.get('safe_num', 2000)  # 每一代存活的数量
        self.variation_rate = kwargs.get('variation_rate', 0.01)  # 产生变异率
        self.cross_rate = kwargs.get('cross_rate', 0.3)  # 发生交配率
        self.generations = kwargs.get('generations', 150)  # 迭代次数

    def generate_genes(self):
        self.genes = []
        for i in range(self.safe_num):
            self.genes.append(self.gene_generator())

    def run(self):
        self.generate_genes()
        for i in range(1, self.generations + 1):
            self.before_one_generation(i, self.genes)
            self.one_generation()
            self.after_one_generation(i, self.genes)

    def one_generation(self):
        mi = min([i.fitness for i in self.genes])
        mx = max([i.fitness for i in self.genes])
        rates = [(gene.fitness - mi + 1) ** 2 / (mx - mi + 1) for gene in self.genes]
        children = []
        for i in range(math.floor(len(self.genes) * self.cross_rate)):
            a, b = random.choices(self.genes, weights=rates, k=2)
            children.append(a.cross(b))
        for i in random.choices(self.genes, k=math.floor(len(self.genes) * self.variation_rate)):
            i.vary()
        self.genes += children
        self.genes.sort(key=lambda x: x.fitness, reverse=True)
        self.genes = self.genes[:self.safe_num]

    def before_one_generation(self, generation, genes):
        pass

    def after_one_generation(self, generation, genes):
        pass
