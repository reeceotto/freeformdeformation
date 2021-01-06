import sys
import os
parentPath = os.path.dirname(os.getcwd()) + '/core'
sys.path.insert(0, parentPath)
import geom_classes as gc
import geom_functions as gf
import visualisation as visual

curve = gc.BSpline.Curve()

# define control points
curve.controlPoints = [[1, -3, 2], [1, 2, 1], [2, 1, 0], [3, 3, -2]]

# define degree of curve
curve.degree = 3

# define knot vector
nControlPoints = len(curve.controlPoints)
curve.knotVector = gf.KnotVector(nControlPoints, curve.degree)

# create 3D curve plot
visual.CurvePlot(curve, showControlPoints=True, showKnots=True, plotDimension='3D', start=0.1, stop=0.9)

# uncomment the following to produce 3D curve plot without knots, control points or control polygon
#visual.CurvePlot(curve, dimension='3D', showControlPoints=False, showKnots=False, showControlPolygon=False, N=200)
