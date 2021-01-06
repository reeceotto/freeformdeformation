import sys
import os
parentPath = os.path.dirname(os.getcwd()) + '/core'
sys.path.insert(0, parentPath)
import geom_classes as gc
import geom_functions as gf
import visualisation as visual
from math import sqrt

surface = gc.NURBS.Surface()

# define control points
surface.controlPoints = [[[0, 1, 0], [1, 1, 0], [1, 0, 0], [1, -1, 0], [0, -1, 0], [-1, -1, 0], [-1, 0, 0], [-1, 1, 0], [0, 1, 0]],
                         [[0, 1, 1], [1, 1, 1], [1, 0, 1], [1, -1, 1], [0, -1, 1], [-1, -1, 1], [-1, 0, 1], [-1, 1, 1], [0, 1, 1]]]

# define control point weightings
surface.weights = [[1, sqrt(2)/2, 1, sqrt(2)/2, 1, sqrt(2)/2, 1, sqrt(2)/2, 1],
                   [1, sqrt(2)/2, 1, sqrt(2)/2, 1, sqrt(2)/2, 1, sqrt(2)/2, 1]]

# define order of polynomial segments
surface.degree1 = 1
surface.degree2 = 2

# calculate knot vectors
surface.knotVector1 = gf.KnotVector(len(surface.controlPoints), surface.degree1)
surface.knotVector2 = [0, 0, 0, 1/4, 1/4, 1/2, 1/2, 3/4, 3/4, 1, 1, 1]

# create surface plot
visual.SurfacePlot(surface)

# uncomment for circular arc at half height
#visual.SurfacePlot(surface, showControlPoints=False, showControlPolygon=False, showKnots=False, N1=100, N2=100, start1=0.0, stop1=0.5, start2=0, stop2=0.5)
