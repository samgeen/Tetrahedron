'''
Created on 28 May 2013

@author: samgeen
'''

from Tetrahedron import Tetrahedron

def Intersect(tet1, tet2):
    '''
    Intersect 2 tetrahedron objects and return the intersecting volume
    '''
    planes = tet1.Surfaces()
    tets = [tet1]
    # Slice tet2 in each tet1 surface
    for plane in planes:
        newtets = list()
        # Run through tetrahedrons in list
        for tet in tets:
            # Find a series of tetrahedrons that form the volume of tet on the correct side of plane
            for newtet in tet.InsidePlane(plane):
                newtets.append(newtet)
        tets = newtets
    # Sum up volumes of tets found
    vol = 0.0
    for tet in tets:
        vol += tet.Volume()
    return vol

if __name__ == '__main__':
    # Tetrahedron 1
    a1 = [0,0,0]
    a2 = [1,0,0]
    a3 = [0,1,0]
    a4 = [0,0,1]
    tet1 = Tetrahedron(a1,a2,a3,a4)
    # Tetrahedron 2
    a1 = [0,0,0]
    a2 = [1,0,0]
    a3 = [0,1,0]
    a4 = [0,0,1]
    tet2 = Tetrahedron(b1,b2,b3,b4)
    # Find the intersecting volume
    print "Intersecting volume of tet1 and tet2:", Intersect(tet1, tet2)