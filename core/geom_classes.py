import geom_functions as gf
import numpy as np

class BSpline:
    #Class for all B-Spline objects.
    
    def __init__(self, **kwargs):
        pass
    
    class Curve:
        """
        Creates a B-Spline curve object.
    
        Keyword arguments:
        controlPoints -- list of Cartesian control point coordinates
        degree -- degree of polynomial segments
        knotVector -- list of parametric coords that define knot locations
    
        Constraints:
        len(controlPoints) - 1 >= degree >= 1
        """
        def __init__(self, **kwargs):
            self.dimension = 1
        
        def PointCoordinates(self, parameter, **kwargs):
            """
            Returns a list of 3D Cartesian coordinates at a given parametric point on a B-Spline curve.
    	    This is algorithm A3.1 on pg 82 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
    		Arguments:
    		"""
            span = gf.FindSpan(self.degree, parameter, self.knotVector)
            B = gf.BSplineBasisFuns(span, parameter, self.degree, self.knotVector)
            C = 0
            for i in range(self.degree + 1):
                C += B[i] * np.array(self.controlPoints[span-self.degree+i])
            return C

class NURBS:
    # Class for all NURBS objects
    
    def __init__(self, **kwargs):
        pass
    
    class Curve:
        """
        Creates a NURBS curve object.
    
        Keyword arguments:
        controlPoints -- list of Cartesian control point coordinates
        degree -- degree of polynomial segments
        knotVector -- list of parametric coords that define knot locations
        weights -- list of control point weights
    
        Constraints:
        len(controlPoints) - 1 >= degree >= 1
        len(weights) == len(controlPoints)
        """
        def __init__(self, **kwargs):
            self.dimension = 1
        
        def PointCoordinates(self, parameter, **kwargs):
            """
            Returns a list of 3D Cartesian coordinates at a given parametric point on a NURBS curve.
            This is algorithm A4.1 on pg 124 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
            Arguments:
            parameter -- parameteric coordinate
            """
            dimension = 1
            Pw = gf.WeightedControlPoints(self.controlPoints, self.weights, dimension)
            span = gf.FindSpan(self.degree, parameter, self.knotVector)
            B = gf.BSplineBasisFuns(span, parameter, self.degree, self.knotVector)
            Cw = 0
            for j in range(self.degree+1):
                Cw += B[j] * Pw[span-self.degree+j]
            C = np.zeros(len(Cw)-1)
            for k in range(len(C)):
                C[k] = Cw[k] / Cw[-1]
            return C

    class Surface:
        """
        Creates a NURBS surface object.
    
        Keyword arguments:
        controlPoints -- list (structured like array) that contains Cartesian control point coordinates
        degree1, degree2 -- degree of polynomial segments in directions 1 and 2 respectively
        knotVector1, knotVector2 -- list of parametric coords that define knot locations in directions 1 and 2 respectively
        weights -- list of control point weights
    
        Constraints:
        len(controlPoints) = number of control points in direction 1, and len(controlPoints[0]) = number of control points in direction 2
        len(controlPoints) - 1 >= degree1 >= 1
        len(controlPoints[0]) - 1 >= degree2 >= 1
        len(weights) == len(controlPoints)
        len(weights[0]) == len(controlPoints[0])
        """
        def __init__(self, **kwargs):
            self.dimension = 2
        
        def PointCoordinates(self, parameter1, parameter2, **kwargs):
            """
            Returns a list of 3D Cartesian coordinates at a given parametric point on a NURBS surface.
            This is algorithm A4.3 on pg 134 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
            Arguments:
            parameter1, parameter2 -- parametric coordinates in directions 1 and 2 respectively
            """
            dimension = 2
            Pw = gf.WeightedControlPoints(self.controlPoints, self.weights, dimension)
            parameter1span = gf.FindSpan(self.degree1, parameter1, self.knotVector1)
            B1 = gf.BSplineBasisFuns(parameter1span, parameter1, self.degree1, self.knotVector1)
            parameter2span = gf.FindSpan(self.degree2, parameter2, self.knotVector2)
            B2 = gf.BSplineBasisFuns(parameter2span, parameter2, self.degree2, self.knotVector2)
            temp = np.nan * np.ones(self.degree2 + 1, dtype=np.ndarray)
            for l in range(self.degree2 + 1):
                temp[l] = 0
                for k in range(self.degree1 + 1):
                    temp[l] += B1[k] * np.array(Pw[parameter1span-self.degree1+k][parameter2span-self.degree2+l])
            Sw = 0
            for l in range(self.degree2 + 1):
                Sw += B2[l] * temp[l]
            S = np.zeros(len(Sw)-1)
            for k in range(len(S)):
                S[k] = Sw[k] / Sw[-1]
            return S
        
        def SurfaceCoordinates(self, N1=50, N2=50, **kwargs):
            """
            Returns a list (structured like array) that contains Cartesian surface coordinates.
        
            Keyword arguments:.
            start1, start2 -- parametric coordinates at which surface begins in directions 1 and 2 respectively (default value shown below)
            stop1, stop2 -- parametric coordinate at which surface stops in directions 1 and 2 respectively (default value shown below)
            N1 -- number of points evaluated between start and stop in directions 1 and 2 respectively (default = 50)
            """
            start1 = kwargs.get('start1', self.knotVector1[self.degree1])
            stop1 = kwargs.get('stop1', self.knotVector1[-(self.degree1 + 1)])
            parameter1values = np.linspace(start1, stop1, N1)
        
            start2 = kwargs.get('start2', self.knotVector2[self.degree2])
            stop2 = kwargs.get('stop2', self.knotVector2[-(self.degree2 + 1)])
            parameter2values = np.linspace(start2, stop2, N2)
        
            parameter1mesh, parameter2mesh = np.meshgrid(parameter1values, parameter2values)
            S = np.nan * np.ones((len(parameter1mesh), len(parameter1mesh[0])), dtype=np.ndarray)
            for i in range(len(parameter1mesh)):
                for j in range(len(parameter1mesh[0])):
                    S[i][j] = self.PointCoordinates(parameter1mesh[i][j], parameter2mesh[i][j])
            
            surfacePointXs, surfacePointYs, surfacePointZs = np.zeros((N2, N1)), np.zeros((N2, N1)), np.zeros((N2, N1))
            for i in range(len(S)):
                for j in range(len(S[0])):
                    surfacePointXs[i][j] = S[i][j][0]
                    surfacePointYs[i][j] = S[i][j][1]
                    surfacePointZs[i][j] = S[i][j][2]
            return surfacePointXs, surfacePointYs, surfacePointZs
        
    class Volume:
        """
        Creates a NURBS volume object.
        
        Keyword arguments:
        controlPoints -- list (structured like array) that contains Cartesian control point coordinates
        degree1, degree2, degree3 -- degree of polynomial segments in directions 1, 2 and 3 respectively
        knotVector1, knotVector2, knotVector3 -- list of parametric coords that define knot locations in directions 1, 2 and 3 respectively
        weights -- list of control point weights
        """
        def __init__(self, **kwargs):
            self.dimension = 3
        
        def PointCoordinates(self, parameter1, parameter2, parameter3, **kwargs):
            """
            Returns a list of 3D Cartesian coordinates at a given parametric point in a NURBS volume.
            This algorthim is personally adapted from the PointCoordinates functions seen in the NURBS Curve and Surface classes.
    
            Arguments:
            parameter1, parameter2, parameter3 -- parametric coordinates in directions 1, 2 and 3 respectively
            """
            dimension = 3
            Pw = gf.WeightedControlPoints(self.controlPoints, self.weights, dimension)
            parameter1span = gf.FindSpan(self.degree1, parameter1, self.knotVector1)
            B1 = gf.BSplineBasisFuns(parameter1span, parameter1, self.degree1, self.knotVector1)
            parameter2span = gf.FindSpan(self.degree2, parameter2, self.knotVector2)
            B2 = gf.BSplineBasisFuns(parameter2span, parameter2, self.degree2, self.knotVector2)
            parameter3span = gf.FindSpan(self.degree3, parameter3, self.knotVector3)
            B3 = gf.BSplineBasisFuns(parameter3span, parameter3, self.degree3, self.knotVector3)
            temp1 = np.nan * np.ones((self.degree2+1, self.degree3+1), dtype=np.ndarray)
            for m in range(self.degree3+1):
                for l in range(self.degree2+1):
                    temp1[l][m] = 0
                    for k in range(self.degree1+1):
                        temp1[l][m] += B1[k] * Pw[parameter1span-self.degree1+k][parameter3span-self.degree3+m][parameter2span-self.degree2+l]
            temp2 = np.nan * np.ones(self.degree3+1, dtype=np.ndarray)
            for m in range(self.degree3+1):
                temp2[m] = 0
                for l in range(self.degree2+1):
                    temp2[m] += B2[l] * temp1[l][m]
            Vw = 0
            for m in range(self.degree3+1):
                Vw += B3[m] * temp2[m]
            V = np.zeros(len(Vw)-1)
            for k in range(len(V)):
                V[k] = Vw[k] / Vw[-1]
            return V
    
