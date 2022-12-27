from mathutils import *

def StripToTriangle(triangleStripList, reverse_face_winding = False):
    faces = []
    cte = 0
    for i in range(2, len(triangleStripList)):
        if triangleStripList[i] == 65535 or triangleStripList[i - 1] == 65535 or triangleStripList[i - 2] == 65535:
            if i % 2 == 0:
                cte = -1
            else:
                cte = 0
            pass
        else:
            if (i + cte) % 2 == 0:
                a = triangleStripList[i - 2]
                b = triangleStripList[i - 1]
                c = triangleStripList[i]
            else:
                a = triangleStripList[i - 1]
                b = triangleStripList[i - 2]
                c = triangleStripList[i]

            if a != b and b != c and c != a:
                if reverse_face_winding:
                    faces.append([c, b, a])
                else: 
                    faces.append([a, b, c])

    return faces

def StripToTriangle2(triangleStripList, vertexList):
    faces = []
    check_flip = False
    flip = False
    for i in range(len(triangleStripList) - 2):
        a = triangleStripList[i]
        b = triangleStripList[i + 1]
        c = triangleStripList[i + 2]
        if (a == 0xFFFF or b == 0xFFFF or c == 0xFFFF):
            check_flip = True
        elif (a != b and a != c and b != c):

            if check_flip:
                v1 = vertexList[a]
                v2 = vertexList[b]
                v3 = vertexList[c]
                n1 = v1.normal
                n2 = v2.normal
                n3 = v3.normal
                vertex_normal = ((n1 + n2 + n3) / 3).normalized()
                face_normal = ((v3.co - v1.co).cross(v2.co - v1.co)).normalized()
                if face_normal.length != 0 and vertex_normal.length != 0:
                    angle = face_normal.dot(vertex_normal) / (face_normal.length * vertex_normal.length)
                    flip = angle >= 0
                check_flip = False
            
            if (flip == False):
                faces.append([a,b,c])
            else:
                faces.append([c,b,a])

            flip = not flip

    return faces



def ToTriangle(triangleList):
    faces = []
    for i in range(2, len(triangleList), 3):
        a  = triangleList[i - 2]
        b  = triangleList[i - 1]
        c  = triangleList[i]
        faces.append([a,b,c])
    return faces

def reverseBits(value):
    return (((value & 1) << 7)  | 
            ((value & 2) << 5)  | 
            ((value & 4) << 3)  | 
            ((value & 8) << 1)  | 
            ((value & 16) >> 1) |
            ((value & 32) >> 3) | 
            ((value & 64) >> 5) | 
            ((value & 128) >> 7))