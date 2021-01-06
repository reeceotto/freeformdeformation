import sys
import os
parentPath = os.path.dirname(os.getcwd()) + '/core'
sys.path.insert(0, parentPath)
import geom_classes as gc
import geom_functions as gf
import visualisation as visual
from math import sqrt

# Free-form deformation example - deforming a NURBS surface within a NURBS volume
volume = gc.NURBS.Volume()

# first, construct the NURBS volume
# define control points
volume.controlPoints = [[[[-1, -1, -1], [-1, 2/3, -1], [-1, 7/3, -1], [-1, 4, -1]],
                          [[-1, -1, 0.5], [-1, 2/3, 0.5], [-1, 7/3, 0.5], [-1, 4, 0.5]],
                          [[-1, -1, 2], [-1, 2/3, 2], [-1, 7/3, 2], [-1, 4, 2]],
                          [[-1, -1, 3.5], [-1, 2/3, 3.5], [-1, 7/3, 3.5], [-1, 4, 3.5]],
                          [[-1, -1, 5], [-1, 2/3, 5], [-1, 7/3, 5], [-1, 4, 5]]],
               
                         [[[2, -1, -1,], [2, 2/3, -1], [2, 7/3, -1], [2, 4, -1]],
                          [[2, -1, 0.5], [2, 2/3, 0.5], [2, 7/3, 0.5], [2, 4, 0.5]],
                          [[2, -1, 2], [2, 2/3, 2], [2, 7/3, 2], [2, 4, 2]],
                          [[2, -1, 3.5], [2, 2/3, 3.5], [2, 7/3, 3.5], [2, 4, 3.5]],
                          [[2, -1, 5], [2, 2/3, 5], [2, 7/3, 5], [2, 4, 5]]],
               
                         [[[5, -1, -1], [5, 2/3, -1], [5, 7/3, -1], [5, 4, -1]],
                          [[5, -1, 0.5], [5, 2/3, 0.5], [5, 7/3, 0.5], [5, 4, 0.5]],
                          [[5, -1, 2], [5, 2/3, 2], [5, 7/3, 2], [5, 4, 2]],
                          [[5, -1, 3.5], [5, 2/3, 3.5], [5, 7/3, 3.5], [5, 4, 3.5]],
                          [[5, -1, 5], [5, 2/3, 5], [5, 7/3, 5], [5, 4, 5]]]]

# define control point weightings
volume.weights = [[[1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1]],
               
                  [[1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1]],
               
                  [[1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1],
                   [1, 1, 1, 1]]]

# define order of polynomial segments
volume.degree1 = 2
volume.degree2 = 3
volume.degree3 = 4

# calculate knot vectors
volume.knotVector1 = gf.KnotVector(len(volume.controlPoints), volume.degree1)
volume.knotVector2 = gf.KnotVector(len(volume.controlPoints[0][0]), volume.degree2)
volume.knotVector3 = gf.KnotVector(len(volume.controlPoints[0]), volume.degree3)

print(volume.PointCoordinates(0.5, 0.5, 0.5))


