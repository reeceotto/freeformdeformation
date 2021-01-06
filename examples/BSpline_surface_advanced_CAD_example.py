import sys
import os
parentPath = os.path.dirname(os.getcwd()) + '/core'
sys.path.insert(0, parentPath)
import geom_classes as gc
import geom_functions as gf
import visualisation as visual
from math import sqrt

# BSpline surface example - Fig 1.25 from 'Advanced CAD Modelling' - Nikola Vukašinović & Jože Duhovnik, 2019
surface = gc.NURBSSurface()

# define control points
surface.controlPoints = [[[0, 0, 0], [0.214, 0.538, 0], [0.660, 1.020, 0], [2.107, 1.207, 0], [2.495, 0.042, 0], [3.367, 0.997, 0], [4, 2, 0]],
                         [[0, 0.321, 0.691], [0.201, 1.332, 0.691], [0.634, 2.291, 0.691], [1.938, 1.737, 0.691], [2.474, 0.729, 0.691], [3.259, 1.454, 0.691], [3.808, 2.296, 0.691]],
                         [[0, 0.668, 2.079], [0.186, 2.164, 2.079], [0.622, 3.625, 2.079], [1.723, 2.299, 2.079], [2.589, 1.559, 2.079], [3.216, 1.833, 2.079], [3.599, 2.296, 2.079]],
                         [[0, 0.347, 3.362], [0.200, 1.285, 3.362], [0.698, 2.220, 3.362], [1.792, 1.731, 3.362], [3.030, 1.142, 3.362], [3.550, 1.017, 3.362], [3.792, 1.103, 3.362]],
                         [[0, 0, 4], [0.214, 0.365, 4], [0.760, 0.751, 4], [1.903, 1.130, 4], [3.347, 0.588, 4], [3.825, 0.271, 4], [4, 0, 4]]]

# define control point weightings
surface.weights = [[1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1],
                   [1, 1, 1, 1, 1, 1, 1]]

# define order of polynomial segments
surface.degree1 = 3
surface.degree2 = 3

# calculate knot vectors (note: in the textbook example, the knot vector is normalised such that the last component = 1)
surface.knotVector1 = gf.KnotVector(len(surface.controlPoints), surface.degree1)
surface.knotVector2 = gf.KnotVector(len(surface.controlPoints[0]), surface.degree2)

# create surface plot
visual.SurfacePlot(surface, N1=50, N2=50, start1=0, stop1=0.5)

