'''
Created on 28 May 2013

@author: samgeen
'''

import numpy as np

import Plane

def PlanesToTetrahedron(planes):
    '''
    Convert 4 planes to a tetrahedron object
    '''
    p1, p2, p3, p4 = planes
    # Find the 4 points of intersecting
    v1 = p1.Intersect(p2,p3)
    v2 = p2.Intersect(p3,p4)
    v3 = p3.Intersect(p4,p1)
    v4 = p4.Intersect(p1,p2)
    # Make and return a tetrahedron
    tet = Tetrahedron(v1,v2,v3,v4)
    return tet

def Slice1(plane, ins, outs):
    '''
    Slice the tetrahedron with a plane that has 1 point inside it
    '''
    i1 = ins[0]
    o1,o2,o3 = outs
    p1 = Plane(i1, o1, o2)
    p2 = Plane(i1, o2, o3)
    p3 = Plane(i1, o3, o1)
    return [PlanesToTetrahedron((plane, p1, p2, p3))]

def Slice2(plane, ins, outs):
    '''
    Slice the tetrahedron with a plane that has 2 points inside it
    e.g. a Toblerone-style shape
    '''
    raise NotImplementedError

def Slice3(plane, ins, outs):
    '''
    Slice the tetrahedron with a plane that has 3 points inside it
    The reverse of Slice1 BUT we need to divide the result into 3 tetrahedrons
    '''
    # Get 3 points intersecting the 3 faces
    i1, i2, i3 = ins
    o1 = outs[0]
    p1 = Plane(o1, i1, i2)
    p2 = Plane(o1, i2, i3)
    p3 = Plane(o1, i3, i1)
    v1 = p1.Intersect(plane, p2)
    v2 = p2.Intersect(plane, p3)
    v3 = p3.Intersect(plane, p1)
    tet1 = Tetrahedron(v1,v2,v3,i1)
    # TODO: FIGURE OUT EXTRA TETRAHEDRONS HERE!
    raise NotImplementedError
    #tet1 = Tetrahedron(v1,v2,v3,i1)
    #tet1 = Tetrahedron(v1,v2,v3,i1)
    return 

class Tetrahedron(object):
    '''
    A tetrahedron
    '''


    def __init__(self, v1, v2, v3, v4):
        '''
        Constructor
        v1-4: 4 vertices of the tetrahedron 
        '''
        #self._vs = [[v1],[v2],[v3],[v4]]
        v1 = np.array(v1)
        v2 = np.array(v2)
        v3 = np.array(v3)
        v4 = np.array(v4)
        self._origin = v1
        self._v1 = v2
        self._v2 = v3
        self._v3 = v4
        self._vol = np.linalg.det(np.array([v2-v1,v3-v1,v4-v1])) / 6.0
        
    def Volume(self):
        '''
        Return the volume of the tetrahedron
        '''
        return self._vol
    
    def Surfaces(self):
        '''
        Return a list of planes that make up the 4 surfaces of the tetrahedron 
        '''
        o = self._origin
        v1 = self._v1
        v2 = self._v2
        v3 = self._v3
        # TODO: MAKE SURE THESE ALL POINT INWARDS!!!
        p1 = Plane(o,v1,v2)
        p2 = Plane(o,v2,v3)
        p3 = Plane(o,v3,v1)
        p4 = Plane(v1,v2,v3)
        return [p1,p2,p3,p4]
        
    def InsidePlane(self, plane):
        '''
        Create a list of tetrahedrons that make up the volume of this object on the +ve side of an infinite plane 
        '''
        o, v1, v2, v3 = (self._origin, self._v1, self._v2, self._v3)
        # Find the number of points on the inside of the plane
        ho = plane.Height(o)
        h1 = plane.Height(v1)
        h2 = plane.Height(v2)
        h3 = plane.Height(v3)
        vs = [o,v1,v2,v3]
        hs = [ho,h1,h2,h3]
        numIn = 0
        ins = list()
        outs = list()
        for (v, h) in (vs, hs):
            # NOTE - normals point *outwards*!
            # TODO: Check that this is consistent throughout
            if h < 0:
                ins.append(v)
            else:
                outs.append(v)
        numIn = len(ins)
        # Step through special cases
        if numIn == 0:
            # Nothing is inside the plane!
            return []
        if numIn == 1:
            Slice1(plane, ins, outs)
        if numIn == 2:
            Slice2(plane, ins, outs)
        if numIn == 3:
            Slice3(plane, ins, outs)
        if numIn == 4:
            # Everything is inside the plane, return this tetrahedron unchanged
            return [self]
        # Oops! Shouldn't be here
        print "Error: numIn should be 0-4, a value of", numIn, "found!"
        raise ValueError
    
if __name__=="__main__":
    v1 = [0,0,0]
    v2 = [1,0,0]
    v3 = [0,1,0]
    v4 = [0,0,1]
    tet = Tetrahedron(v1,v2,v3,v4)
    print tet.Volume() 