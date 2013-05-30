'''
Created on 28 May 2013

@author: samgeen
'''

import numpy as np

class Plane(object):
    '''
    A plane object corresponding to an infinite plane in 3-space
    '''


    def __init__(self, v1, v2, v3):
        '''
        Constructor
        v1-3: 3 vertices defining the plane
        '''
        v1 = np.array(v1)
        v2 = np.array(v2)
        v3 = np.array(v3)
        # Vertices of the plane
        self._v1 = v1
        self._v2 = v2
        self._v3 = v3
        # Normal of plane is the cross product of 2 vectors in it
        norm = np.cross(v2-v1, v3-v1)
        norm /= np.sqrt(np.sum(norm*norm))
        # The height of the plane is the dot product of the normal to a point in the plane
        dist = np.sum(norm*v1)
        self._norm = norm
        self._dist = dist
        
    def Intersect(self, p1, p2):
        '''
        Find the point of intersection of this and 2 other planes
        See http://mathworld.wolfram.com/Plane-PlaneIntersection.html
        '''
        p0 = self
        a0 = np.array(p0._v1, p0._v2, p0._v3)
        a1 = np.array(p1._v1, p1._v2, p1._v3)
        a2 = np.array(p2._v1, p2._v2, p2._v3)
        det = np.linalg.det(np.array(a0,a1,a2))
        pos = p0._dist * np.cross(p1._norm, p2._norm) + \
                p1._dist * np.cross(p2._norm, p0._norm) + \
                p2._dist * np.cross(p0._norm, p1._norm)
        try: 
            pos /= det
        except:
            "Determinant of intersection is zero! i.e. 2 or all planes are parallel"
            raise ValueError
        return pos
    
    def Height(self, v):
        '''
        Find the height of vertex v in the plane
        '''
        return np.sum(v * self._norm - self._dist)

        