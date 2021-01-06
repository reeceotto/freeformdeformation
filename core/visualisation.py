import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import geom_functions as gf
import geom_classes as gc

def CurvePlot(curve, showControlPoints=True, showKnots=True, showControlPolygon=True, plotDimension='3D', N=100, **kwargs):
    """
    Produces a plot of a given curve.
    
    Arguments & Keyword Arguments:
    curve -- a curve object defined by a class from geom_classes.py
    showControlPoints -- option to plot control points (default = True)
    showKnots -- option to plot knots (default = True)
    showControlPolygon -- option to plot control polygon (default = True)
    dimension -- dimension of plot (either '2D' or '3D', default = '3D')
    N -- number of points evaluated along curve (deafult = 100)
    """
    # evaluate points along curve
    start = kwargs.get('start', curve.knotVector[curve.degree])
    stop = kwargs.get('stop', curve.knotVector[-(curve.degree + 1)])
    curveCoords = gf.CurveCoordinates(curve=curve, start=start, stop=stop, N=N)
    curveXs, curveYs, curveZs = gf.ExtractCoordinates(curveCoords)
    
    # plot curve
    fig = plt.figure()
    if plotDimension == '2D':
        plt.axes()
        plt.plot(curveXs, curveYs,'k', label='Curve')
    elif plotDimension == '3D':
        ax = plt.axes(projection='3d')
        ax.plot(curveXs, curveYs, curveZs, 'k', label='Curve')
    else:
        print('Invalid plot dimension specified.')
    
    # plot control points if desired
    if showControlPoints == True:
        controlPointXs, controlPointYs, controlPointZs = gf.ExtractCoordinates(curve.controlPoints)
        if plotDimension == '2D':
            plt.plot(controlPointXs, controlPointYs, 'ro', label='Control Points')
            
        elif plotDimension == '3D':
            ax.plot(controlPointXs, controlPointYs, controlPointZs, 'ro', label='Control Points')
        
    # plot control polygon if desired
    if showControlPolygon == True:
        if plotDimension == '2D':
            plt.plot(controlPointXs, controlPointYs, 'b-', alpha=0.3, label='Control Polygon')
        if plotDimension == '3D':
            ax.plot(controlPointXs, controlPointYs, controlPointZs, 'b-', alpha=0.3, label='Control Polygon')
    
    # plot knots if desired
    if showKnots == True:
        knots = gf.KnotCoordinates(curve)
        knotXs, knotYs, knotZs = gf.ExtractCoordinates(knots)
        if plotDimension == '2D':
            plt.plot(knotXs, knotYs, 'gx', label='Knots')
        elif plotDimension == '3D':
            ax.plot(knotXs, knotYs, knotZs, 'gx', label='Knots')
    
    # add plot options and show
    if plotDimension == '2D':
        plt.xlabel('$x$')
        plt.ylabel('$y$')
        plt.axis('equal')
        plt.grid()
    elif plotDimension == '3D':
        ax.set_xlabel("$x$")
        ax.set_ylabel("$y$")
        ax.set_zlabel("$z$")
    plt.legend()
    plt.show()

def SurfacePlot(surface, showControlPoints=True, showKnots=True, showControlPolygon=True, N1=50, N2=50, **kwargs):
    """
    Produces a plot of a given surface.
    
    Arguments & Keyword Arguments:
    surface -- a surface object defined by a class from geom_classes.py
    showControlPoints -- option to plot control points (default = True)
    showKnots -- option to plot knots (default = True)
    showControlPolygon -- option to plot control polygon (default = True)
    dimension -- dimension of plot (either '2D' or '3D', default = '3D')
    N1 -- number of points evaluated along surface in direction 1 (deafult = 50)
    N2 -- number of points evaluated along surface in direction 2 (deafult = 50)
    """
    # plotting surface as wireframe
    start1 = kwargs.get('start1', surface.knotVector1[surface.degree1])
    stop1 = kwargs.get('stop1', surface.knotVector1[-(surface.degree1 + 1)])
    start2 = kwargs.get('start2', surface.knotVector2[surface.degree2])
    stop2 = kwargs.get('stop2', surface.knotVector2[-(surface.degree2 + 1)])
    surfacePointXs, surfacePointYs, surfacePointZs = surface.SurfaceCoordinates(N1=N1, N2=N2, start1=start1, stop1=stop1, start2=start2, stop2=stop2)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_wireframe(surfacePointXs, surfacePointYs, surfacePointZs, color='black', label='Surface')
    
    # plotting control points if desired
    if showControlPoints == True:
        controlPointXs, controlPointYs, controlPointZs = SurfaceControlPoints(surface)
        ax.scatter3D(controlPointXs, controlPointYs, controlPointZs, color='red', label='Control Points')
    
    # plotting control polygon if desired (this might need its own function in gf)
    if showControlPolygon == True:
        # plotting control polygon 1
        for i in range(len(surface.controlPoints)):
            tempXs, tempYs, tempZs = [], [], []
            for j in range(len(surface.controlPoints[0])):
                tempXs.append(surface.controlPoints[i][j][0])
                tempYs.append(surface.controlPoints[i][j][1])
                tempZs.append(surface.controlPoints[i][j][2])
            if i == 0:
                ax.plot(tempXs, tempYs, tempZs, color='blue', alpha=0.3, label='Control Polygon')
            else:
                ax.plot(tempXs, tempYs, tempZs, color='blue', alpha=0.3)
        
        # plotting control polygon 2
        for j in range(len(surface.controlPoints[0])):
            tempXs, tempYs, tempZs = [], [], []
            for i in range(len(surface.controlPoints)):
                tempXs.append(surface.controlPoints[i][j][0])
                tempYs.append(surface.controlPoints[i][j][1])
                tempZs.append(surface.controlPoints[i][j][2])
            ax.plot(tempXs, tempYs, tempZs, color='blue', alpha=0.3)
    
    # plotting knots if desired
    if showKnots == True:
        knots = gf.KnotCoordinates(surface)
        knotXs, knotYs, knotZs = gf.ExtractCoordinates(knots)
        ax.plot(knotXs, knotYs, knotZs, 'gx', label='Knots')
    
    # set axis labels, show legend and produce plot
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_zlabel("$z$")
    plt.legend()
    plt.show()

# generalise 'ExtractCoordinates' to support surface and volume control point tensor extraction and the following function will become redundant
def SurfaceControlPoints(surface):
    controlPointXs, controlPointYs, controlPointZs = [], [], []
    Pw = gf.WeightedControlPoints(surface.controlPoints, surface.weights, dimension=2)
    for i in range(len(Pw)):
        for j in range(len(Pw[0])):
            controlPointXs.append(surface.controlPoints[i][j][0])
            controlPointYs.append(surface.controlPoints[i][j][1])
            controlPointZs.append(surface.controlPoints[i][j][2])
    return controlPointXs, controlPointYs, controlPointZs

