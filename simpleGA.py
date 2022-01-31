from __future__ import annotations
import os 

import numpy as np
import matplotlib as mat
import matplotlib.pyplot as plt

import typing as t
import tqdm as bar

rng = np.random.default_rng()

def suppress_qt_warnings() -> None:
    os.environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"

def saveImage(prefix: str, genCount: int, population: t.List) -> None:
    X_SHAFF = np.linspace(-100, 100, 500) 
    Y_SHAFF = np.linspace(-100, 100, 500) 

    X_SHAFF += 30
    Y_SHAFF -= 30

    X_SHAFF, Y_SHAFF = np.meshgrid(X_SHAFF, Y_SHAFF)
    Z_SHAFF = 0.5 + ((np.sin(np.sqrt(X_SHAFF**2 + Y_SHAFF**2)))**2 - 0.5)/((1 + 0.001 * (X_SHAFF**2 + Y_SHAFF**2))**2)


# X_RAS = Y_RAS = np.linspace(-5.12, 5.12, 500)
# X_RAS, Y_RAS = np.meshgrid(X_RAS, Y_RAS)
# Z_RAS = (X_RAS**2 - 10 * np.cos(2 * np.pi * X_RAS)) + (Y_RAS**2 - 10 * np.cos(2 * np.pi * Y_RAS)) + 20
     

    # plt.figure(figsize= (12, 8), dpi = 80)
    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=(12, 8), dpi = 80)

# ax1.imshow(Z_RAS, interpolation='bilinear', extent = [-5.12, 5.12, -5.12, 5.12], origin = 'lower', cmap = mat.colormaps['YlOrBr'])
# ax1.title.set_text('Rastrigin-2D Function')

    ax1.imshow(Z_SHAFF, interpolation='bilinear', extent = [-100, 100, -100, 100], origin = 'lower', cmap = mat.colormaps['YlOrBr'])
    plotX = [ population[i][0] for i in range(0, len(population)) ] 
    plotY = [ population[i][1] for i in range(0, len(population)) ]

    ax1.scatter(x = plotX, y = plotY, c = '#ffc800', alpha = 0.8)
    ax1.title.set_text('Schaffer-2D Function')

# plt.show()
    fig.savefig(f'images/{prefix}/{genCount}.png')
    plt.close(fig)


def clamp(val, minval, maxval):
    return sorted((minval, val, maxval))[1]

class Organism:
    def __init__(self, chromLen: int = 1, chromMin: float = 0.0, chromMax: float = 1.0, chrom: np.ndarray = None) -> None:

        if chrom is None:
            self.chromosome : np.ndarray = rng.uniform(size = chromLen, low = chromMin, high = chromMax)
        else:
            self.chromosome = chrom
        self.fitness : float = 0.0 
    
    def mutate(self, mRate):
        self.chromosome += rng.normal(loc = 0, scale = mRate, size = self.chromosome.shape)
    
    @staticmethod
    def getChild(parent1 : Organism, parent2 : Organism, interpolFac : float) -> Organism:
        childChrom = parent1.chromosome * interpolFac + (1 - interpolFac) * parent2.chromosome 

        return Organism(chrom = childChrom)
    
class Population:
    
    def __init__(self, popSize: int, 
            orgData : t.Dict, 
            fitness : t.Callable, 
            selectPer : float, 
            interpolFac : float, 
            mutationRate : float) -> None:

        self.orgList : t.List = [
                Organism(
                    chromLen=orgData['len'], 
                    chromMin=orgData['min'],
                    chromMax=orgData['max']) for _ in range(popSize)]  

        self.popSize = popSize
        self.fitFunc : t.Callable = fitness
        self.k : int = int(popSize * clamp(selectPer, 0.0, 1.0))
        self.interpolFac : float = clamp(interpolFac, 0.0, 1.0)
        self.mutRate : float = mutationRate 

    def selection(self) -> t.List:
        for o in self.orgList:
            o.fitness = self.fitFunc(o.chromosome)
        
        # using truncation selection
        parents = sorted(self.orgList, key = lambda o : o.fitness)[:self.k] 

        return parents

    def crossover(self, parentsList : t.List) -> t.List:
        numChildren = self.popSize - self.k 
        children : t.List = []
        high = len(parentsList) - 1 
        for _ in range(0, numChildren):
            p : np.ndarray = rng.integers(low = 0, high = high, size = 2) 

            p1 = parentsList[p[0]]
            p2 = parentsList[p[1]]

            children.append(Organism.getChild(p1, p2, self.interpolFac))

        return children

    def mutation(self, childrenList: t.List):
        for c in childrenList:
            c.mutate(self.mutRate)

    def updateOrgList(self, parentsList: t.List, childrenList: t.List):
        self.orgList = parentsList + childrenList


def calcFitness(chrom : np.ndarray) -> float:
    x = chrom[0] + 30
    y = chrom[1] - 30
    return ((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5)/((1 + 0.001 * (x**2 + y**2))**2)


def GA():
    pop = Population(popSize = 100, 
            orgData = {'len': 2, 'min': -100.0, 'max': 100.0 },
            fitness = calcFitness,
            selectPer = 0.20,
            interpolFac = 0.5,
            mutationRate = 0.5)


    for g in bar.tqdm(range(0, 100)):
        
        saveImage('first', g, [o.chromosome for o in pop.orgList])

        parents = pop.selection()
        children = pop.crossover(parents)
        pop.mutation(children)
        pop.updateOrgList(parents, children)

if __name__ == '__main__':
    suppress_qt_warnings()
    GA()

