import numpy as np

def KnotVector(nControlPoints, degree):
    """
    Returns a list of parametric knot locations.
    This is Eqn 5 from 'Freeform Deformation Versus B-Spline Representation in Inverse Airfoil Design' - Eleftherios I. Amoiralis, Ioannis K. Nikolos, 2008
    """
    a = nControlPoints - 1
    if degree > a:
        if degree < 1:
            print("Error: 1 <= degree <= a condition not satisfied!")  
    q = a + degree + 1
    knotVector = [None] * (q + 1) 
    for i in range(len(knotVector)):
        if 0 <= i:
            if i <= degree:
                knotVector[i] = 0
        if degree < i:
            if i <= q - degree - 1:
                knotVector[i] = i - degree
        if q - degree - 1 < i:
            if i <= q:
                knotVector[i] = q - 2*degree
    return np.array(knotVector)

def FindSpan(degree, parameter, knotVector):
    """
    Returns the index of the knot vector whose value is less than the parameter.
    This is algorithm A2.1 on pg 68 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
    Arguments:
    degree -- degree of polynomial segments
    parameter -- parameteric coordinate of B-Spline
    knotVector -- list of parametric coords that define knot locations
    """
    if parameter < knotVector[0] or parameter > knotVector[-1]:
        raise IndexError("parameter == {} out of range: [{}, {}]".format(parameter, knotVector[0], knotVector[-1]))
    m = len(knotVector) - 1
    n = m - degree - 1
    assert n + degree + 1 == m, "Invalid n. Should be: {} not {}".format(m - degree - 1, n)
    if parameter == knotVector[n+1]: return n # Special case
    # Do binary search
    low = degree
    high = n + 1
    mid = (low + high) // 2
    while parameter < knotVector[mid] or parameter >= knotVector[mid+1]:
        if parameter < knotVector[mid]: 
            high = mid
        else:
            low = mid
        mid = (low + high) // 2
    return mid

def WeightedControlPoints(controlPoints, weights, dimension):
    """
    Returns weight control point tensor with each 
    
    Arguments:
    controlPoints -- list of control point coordinates
    weights -- list of control point weights
    dimension -- dimension of geometric object
    
    Constraints:
    number of control points = number of weights
    dimension = 1 for curve
    dimension = 2 for surface
    dimension = 3 for volume
    """
    if dimension == 1:
        Pw = np.zeros((len(controlPoints), len(controlPoints[0]) + 1))
        for i in range(len(controlPoints)):
            Pw[i][len(controlPoints[0])] = weights[i]    
            for j in range(len(controlPoints[0])):
                Pw[i][j] = weights[i] * controlPoints[i][j]
    
    if dimension == 2:
        Pw = np.zeros((len(controlPoints), len(controlPoints[0]), len(controlPoints[0][0]) + 1))
        for i in range(len(controlPoints)):
            for j in range(len(controlPoints[0])):
                Pw[i][j][-1] = weights[i][j]
                for k in range(len(controlPoints[0][0])):
                    Pw[i][j][k] = weights[i][j] * np.array(controlPoints[i][j][k])
    
    if dimension == 3:
        Pw = np.zeros((len(controlPoints), len(controlPoints[0]), len(controlPoints[0][0]), len(controlPoints[0][0][0]) + 1))
        for i in range(len(controlPoints)):
            for j in range(len(controlPoints[0])):
                for k in range(len(controlPoints[0][0])):
                    Pw[i][j][k][-1] = weights[i][j][k]
                    for l in range(len(controlPoints[0][0][0])):
                       Pw[i][j][k][l] = weights[i][j][k] * np.array(controlPoints[i][j][k][l]) 
    return Pw

def BSplineBasisFuns(i, parameter, degree, knotVector):
    """
    Returns list of all non-zero B-Spline basis functions.
    This is algorthim A2.2 on pg 70 of 'The NURBS Book' - Les Piegl & Wayne Tiller, 1997.
    
    Arguments:
    i -- index
    parameter -- parameteric coordinate
    degree -- degree of polynomial segments
    knotVector -- list of parametric coords that define knot locations
    """
    # 
    B = np.nan * np.ones(degree + 1)
    B[0] = 1.0
    left = np.nan * np.ones_like(B)
    right = np.nan * np.ones_like(B)
    for j in range(1, degree + 1):
        left[j] = parameter - knotVector[i+1-j]
        right[j] = knotVector[i+j]-parameter
        saved = 0.0
        for r in range(j):
            temp = B[r] / (right[r+1] + left[j-r])
            B[r] = saved + right[r+1] * temp
            saved = left[j-r] * temp
        B[j] = saved
    return B

def ExtractCoordinates(listOfCoords):
    """
    Takes a list of coordinates and returns separate lists organised into x, y and z components respectively.
    """
    xCoords, yCoords = [], []
    for i in range(len(listOfCoords)):
        xCoords.append(listOfCoords[i][0])
        yCoords.append(listOfCoords[i][1])
    if len(listOfCoords[0]) == 3:
        zCoords = [listOfCoords[i][2] for i in range(len(listOfCoords))]
    if len(listOfCoords[0]) == 2:
        return xCoords, yCoords
    elif len(listOfCoords[0]) == 3:
        return xCoords, yCoords, zCoords
    else:
        print('Invalid dimension.')

def CurveCoordinates(curve, N=100, **kwargs):
    """
    Returns a list of Cartesian curve coordinates.
        
    start -- parametric coordinate at which curve begins (default value shown below)
    stop -- parametric coordinate at which curve stops (default value shown below)
    N -- number of points evaluated between start and stop (default = 100)
    """
    start = kwargs.get('start', curve.knotVector[curve.degree])
    stop = kwargs.get('stop', curve.knotVector[-(curve.degree + 1)])
    parameterValues = np.linspace(start, stop, N)
    return [curve.PointCoordinates(x) for x in parameterValues]
    
def KnotCoordinates(geometricObject):
    # Returns a list Cartesian knot coordinates of a given geometric object.
    if geometricObject.dimension == 1:
        return [geometricObject.PointCoordinates(x) for x in geometricObject.knotVector]
    elif geometricObject.dimension == 2:
        knots = []
        for x in geometricObject.knotVector1:
            for y in geometricObject.knotVector2:
                knots.append(geometricObject.PointCoordinates(x, y))
        return knots
    else:
        print('Geometric object has invalid dimension.')


