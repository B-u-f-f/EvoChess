from celluloid import Camera
from testfunctions import ShafferF62D

import matplotlib as mat
import matplotlib.pyplot as plt
import numpy as np
import os
import typing as t


class BadData(Exception):
    def __init__(self):
        super().__init__('Bad Data.')



class ScatterAnimation:
    
    # every a in args:
    # a = (x, y, c, a)
    #   x, y is lists of lists where sublists contain x, y coordinates 
    #   len(x) = len(y) < numframes
    # 
    #   c is the colour of the plotted points: (rgb_string, alpha)
    #   a is the axis to plot
    def __init__(self, numframes: int = 100, fig: mat.figure.Figure = None, *args) -> None:
        
        for (x, y, _, _) in args:
            if((len(x) != len(y)) or (len(y) < numframes)):
                raise BadData() 

        self.data = args
        self.numframes: int = numframes
        self.camera = Camera(fig)

    def createAndSaveAnimation(self) -> mat.animation.ArtistAnimation:
        for i in range(self.numframes): 
            for (x, y, c, a) in self.data:
                a.scatter(x = x[i], y = y[i], c = c[0], alpha = c[1])
                
                self.camera.snap()

        anim = self.camera.animate()
        return anim

if __name__ == '__main__':
    fig, ax1 = plt.subplots(nrows = 1, ncols = 1, figsize=(12, 8), dpi = 80)
    sf = ShafferF62D(xshift = np.float32(30.0), yshift = np.float32(-30.0))
    numframes = 10
    x1 = [] 
    y1 = []
    c = ('#2164b0', 0.6)
    
    x2 = [] 
    y2 = []
    c2 = ('#25ba6b', 0.6)
 

    rng = np.random.default_rng()
    for j in range(numframes):
        x1.append(rng.uniform(low = -100, high = 100, size = 10))
        y1.append(rng.uniform(low = -100, high = 100, size = 10))

        x2.append(rng.uniform(low = -100, high = 100, size = 10))
        y2.append(rng.uniform(low = -100, high = 100, size = 10))
 
    
    sa = ScatterAnimation(numframes, fig, (x1, y1, c, ax1), (x2, y2, c2, ax1))
    anim = sa.createAndSaveAnimation() 
    sf.show(ax1)
    anim.save('./images/hello.gif')
