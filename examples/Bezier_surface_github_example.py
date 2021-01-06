import sys
import os
parentPath = os.path.dirname(os.getcwd()) + '/core'
sys.path.insert(0, parentPath)
import geom_classes as gc
import geom_functions as gf
import visualisation as visual
from math import sqrt

# Bezier surface example - https://gist.github.com/orbingol/05f0f6930331b7c3007644c31ae6e4bc
# currently executed with a NURBS surface object, will update if Bezier functionality is added
surface = gc.NURBS.Surface()

# define control points
surface.controlPoints = [[[0, 0, 0], [0, 4, 0], [0, 8, -3]],
                         [[2, 0, 6], [2, 4, 0], [2, 8, 0]],
                         [[4, 0, 0], [4, 4, 0], [4, 8, 3]],
                         [[6, 0, 0], [6, 4, -3], [6, 8, 0]]]

# define control point weightings
surface.weights = [[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]]

# define order of polynomial segments
surface.degree1 = 3
surface.degree2 = 2

# calculate knot vectors
surface.knotVector1 = gf.KnotVector(len(surface.controlPoints), surface.degree1)
surface.knotVector2 = gf.KnotVector(len(surface.controlPoints[0]), surface.degree2)

# create surface plot
visual.SurfacePlot(surface)

