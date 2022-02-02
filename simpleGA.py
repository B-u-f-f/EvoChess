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

def shafferF62D(x : np.ndarray, y : np.ndarray, xShift : int, yShift : int) -> np.ndarray:
    x += xShift
    y += yShift

    return 0.5 + ((np.sin(np.sqrt(x**2 + y**2)))**2 - 0.5)/((1 + 0.001 * (x**2 + y**2))**2)

def rastrigin2D(x : np.ndarray, y : np.ndarray, xShift : int, yShift : int) -> np.ndarray:
    x += xShift
    y += yShift

    return (x**2 - 10 * np.cos(2 * np.pi * x)) + (y**2 - 10 * np.cos(2 * np.pi * y)) + 20


def saveImage(prefix: str, genCount: int, title: str, 
        populationData: t.Dict, funcData : t.Dict) -> None:
    X = np.linspace(funcData['xmin'], funcData['xmax'], funcData['xiter']) 
    Y = np.linspace(funcData['ymin'], funcData['ymax'], funcData['yiter']) 

    # X_SHAFF += 30
    # Y_SHAFF -= 30

    X, Y = np.meshgrid(X, Y)
    Z = funcData['function'](X, Y) 

    # X_RAS = Y_RAS = np.linspace(-5.12, 5.12, 500)
    # X_RAS, Y_RAS = np.meshgrid(X_RAS, Y_RAS)
    # Z_RAS = (X_RAS**2 - 10 * np.cos(2 * np.pi * X_RAS)) + (Y_RAS**2 - 10 * np.cos(2 * np.pi * Y_RAS)) + 20
     

    # plt.figure(figsize= (12, 8), dpi = 80)
    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=(12, 8), dpi = 80)

    # ax1.imshow(Z_RAS, interpolation='bilinear', extent = [-5.12, 5.12, -5.12, 5.12], origin = 'lower', cmap = mat.colormaps['YlOrBr'])
    # ax1.title.set_text('Rastrigin-2D Function')

    ax1.imshow(Z, interpolation='bilinear', 
            extent = [funcData['xmin'], funcData['xmax'], funcData['ymin'], funcData['ymax']], 
            origin = 'lower', 
            cmap = mat.colormaps['YlOrBr'])
    
    rejectedPopulation = populationData['rejected']
    selectedPopluation = populationData['selected']

    rejectedPlotX = [ rejectedPopulation[i][0] for i in range(0, len(rejectedPopulation)) ] 
    rejectedPlotY = [ rejectedPopulation[i][1] for i in range(0, len(rejectedPopulation)) ]

    selectedPlotX = [ selectedPopluation[i][0] for i in range(0, len(selectedPopluation)) ] 
    selectedPlotY = [ selectedPopluation[i][1] for i in range(0, len(selectedPopluation)) ]


    ax1.scatter(x = rejectedPlotX, y = rejectedPlotY, c = '#2164b0', alpha = 0.6)
    ax1.scatter(x = selectedPlotX, y = selectedPlotY, c = '#25ba6b', alpha = 0.6)
    ax1.title.set_text(title)

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
                    chromLen = orgData['len'], 
                    chromMin = orgData['min'],
                    chromMax = orgData['max']) 
                for _ in range(popSize)]  

        self.popSize : int = popSize
        self.fitFunc : t.Callable = fitness
        self.k : int = int(popSize * clamp(selectPer, 0.0, 1.0))
        self.interpolFac : float = clamp(interpolFac, 0.0, 1.0)
        self.mutRate : float = mutationRate 

    def selection(self) -> (t.List, t.List):
        for o in self.orgList:
            o.fitness = self.fitFunc(o.chromosome)
        
        # using truncation selection
        s = sorted(self.orgList, key = lambda o : o.fitness)
        parents = s[:self.k] 

        return parents, s[(self.k+1):]

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

def GA():

    pop = Population(popSize = 100, 
            orgData = {'len': 2, 'min': -3.0, 'max': -2.0},
            fitness = lambda c : rastrigin2D(c[0], c[1], 0, -0),
            selectPer = 0.20,
            interpolFac = 0.5,
            mutationRate = 0.5)

    funcData = {
            'xmin': -5.12,
            'xmax': +5.12,
            'xiter': 100,
            'ymin': -5.12,
            'ymax': +5.12,
            'yiter': 100,
            'function': lambda x, y : rastrigin2D(x, y, 0, -0)
            }


    for g in bar.tqdm(range(0, 100)):
        
        parents, rejected = pop.selection()
        children = pop.crossover(parents)
        pop.mutation(children)
        pop.updateOrgList(parents, children)
        
        selectedChrom = [p.chromosome for p in parents]
        rejectedChrom = [r.chromosome for r in rejected]

        saveImage('third', g, 'Rastrigin-2D',
                {'selected': selectedChrom, 'rejected': rejectedChrom}, funcData)

if __name__ == '__main__':
    suppress_qt_warnings()
    GA()
