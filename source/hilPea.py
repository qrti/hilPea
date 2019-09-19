# hilbert + peano 2D + 3D, blender script
# V0.9 190916, qrt@qland.de

import bpy
from math import *
from collections import namedtuple

Triple = namedtuple('Triple', 'x y z')

scale = Triple(1, 1, 1)
verts = []
edges = []

class L:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __neg__(self):
        return L(-self.x, -self.y, -self.z)

    def cor(self, s, x, y, z=0, f=1):
        if self.x < 0: x -= s * self.x * f
        if self.y < 0: y -= s * self.y * f
        if self.z < 0: z -= s * self.z * f
        return (x, y, z)

def draw(x, y, z):
    global verts, edges

    verts += [(x*scale.x, y*scale.y, z*scale.z)]
    n = len(verts)

    if n > 1:
        edges += [(n-2, n-1)]

def pointOnLine(p, a, b):
    i = 0

    while b.x-a.x==0 and i<2:
        a = Triple(a.y, a.z, a.x)
        b = Triple(b.y, b.z, b.x)
        p = Triple(p.y, p.z, p.x)
        i += 1

    if i==2 and b.x-a.x==0:
        return False

    t = (p.x - a.x) / (b.x - a.x)
    return abs(a.y + t * (b.y - a.y) - p.y) < 1E-4 and abs(a.z + t * (b.z - a.z) - p.z) < 1E-4

def pointOnEdge(p, a, b):
    minx = min(a.x, b.x)
    maxx = max(a.x, b.x)

    miny = min(a.y, b.y)
    maxy = max(a.y, b.y)

    minz = min(a.z, b.z)
    maxz = max(a.z, b.z)

    return p.x<=maxx and p.x>=minx and \
           p.y<=maxy and p.y>=miny and \
           p.z<=maxz and p.z>=minz and \
           pointOnLine(p, a, b)

def pointOnEdgeEx(p, a, b):
    minx = min(a.x, b.x)
    maxx = max(a.x, b.x)

    miny = min(a.y, b.y)
    maxy = max(a.y, b.y)

    minz = min(a.z, b.z)
    maxz = max(a.z, b.z)

    return p.x<maxx and p.x>minx and \
           p.y<maxy and p.y>miny and \
           p.z<maxz and p.z>minz and \
           pointOnLine(p, a, b)

def cleanEdges():
    global verts, edges

    for i in range(len(verts)-2, 0, -1):
        if pointOnEdge(Triple(*verts[i]), Triple(*verts[i-1]), Triple(*verts[i+1])):
            del verts[i]

    edges = []

    for i in range(1, len(verts)):
        edges += [(i-1, i)]

    return

def hilbert2d(s, x, y, a, b):
    if s == 1:
        draw(x, y, 0)
        return

    s >>= 1

    x, y, _ = a.cor(s, x, y)           
    x, y, _ = b.cor(s, x, y)

    hilbert2d(s, x,             y,              b,  a)
    hilbert2d(s, x+s*b.x,       y+s*b.y,        a,  b)
    hilbert2d(s, x+s*(a.x+b.x), y+s*(a.y+b.y),  a,  b)
    hilbert2d(s, x+s*a.x,       y+s*a.y,       -b, -a)

def hilbert3d(s, x, y, z, a, b, c):
    if s == 1:
        draw(x, y, z)
        return

    s >>= 1
    
    x, y, z = a.cor(s, x, y, z)         # correction factor 1
    x, y, z = b.cor(s, x, y, z)
    x, y, z = c.cor(s, x, y, z)

    hilbert3d(s, x,                 y,                 z,                  b,  c,  a)
    hilbert3d(s, x+s*a.x,           y+s*a.y,           z+s*a.z,            c,  a,  b)
    hilbert3d(s, x+s*(a.x+b.x),     y+s*(a.y+b.y),     z+s*(a.z+b.z),      c,  a,  b)
    hilbert3d(s, x+s*b.x,           y+s*b.y,           z+s*b.z,           -a, -b,  c)
    hilbert3d(s, x+s*(b.x+c.x),     y+s*(b.y+c.y),     z+s*(b.z+c.z),     -a, -b,  c)
    hilbert3d(s, x+s*(a.x+b.x+c.x), y+s*(a.y+b.y+c.y), z+s*(a.z+b.z+c.z), -c,  a, -b)
    hilbert3d(s, x+s*(a.x+c.x),     y+s*(a.y+c.y),     z+s*(a.z+c.z),     -c,  a, -b)
    hilbert3d(s, x+s*c.x,           y+s*c.y,           z+s*c.z,            b, -c, -a)

def peano2d(s, x, y, a, b):
    if s == 1:
        draw(x, y, 0)
        return

    s //=  3

    x, y, _ = a.cor(s, x, y, f=2)           # correction factor 2
    x, y, _ = b.cor(s, x, y, f=2)

    peano2d(s, x,               y,                a,  b)
    peano2d(s, x+s*b.x,         y+s*b.y,         -a,  b)
    peano2d(s, x+s*2*b.x,       y+s*2*b.y,        a,  b)
    peano2d(s, x+s*(a.x+2*b.x), y+s*(a.y+2*b.y),  a, -b)
    peano2d(s, x+s*(a.x+b.x),   y+s*(a.y+b.y),   -a, -b)
    peano2d(s, x+s*a.x,         y+s*a.y,          a, -b)
    peano2d(s, x+s*2*a.x,       y+s*2*a.y,        a,  b)
    peano2d(s, x+s*(2*a.x+b.x), y+s*(2*a.y+b.y), -a,  b)
    peano2d(s, x+s*2*(a.x+b.x), y+s*2*(a.y+b.y),  a,  b)

def peano3d(s, x, y, z, a, b, c):
    if s == 1:
        draw(x, y, z)
        return

    s //= 3

    x, y, z = a.cor(s, x, y, z, 2)          # correction factor 2
    x, y, z = b.cor(s, x, y, z, 2)
    x, y, z = c.cor(s, x, y, z, 2)

    peano3d(s, x,                     y,                     z,                      b,  a,  c)
    peano3d(s, x+s*a.x,               y+s*a.y,               z+s*a.z,                a, -b, -c)
    peano3d(s, x+s*2*a.x,             y+s*2*a.y,             z+s*2*a.z,              b,  a,  c)
    peano3d(s, x+s*(2*a.x+b.x),       y+s*(2*a.y+b.y),       z+s*(2*a.z+b.z),       -a,  b, -c)
    peano3d(s, x+s*(a.x+b.x),         y+s*(a.y+b.y),         z+s*(a.z+b.z),         -b, -a,  c)
    peano3d(s, x+s*b.x,               y+s*b.y,               z+s*b.z,               -a,  b, -c)
    peano3d(s, x+s*2*b.x,             y+s*2*b.y,             z+s*2*b.z,              b,  a,  c)
    peano3d(s, x+s*(a.x+2*b.x),       y+s*(a.y+2*b.y),       z+s*(a.z+2*b.z),        a, -b, -c)
    peano3d(s, x+s*2*(a.x+b.x),       y+s*2*(a.y+b.y),       z+s*2*(a.z+b.z),        b,  a,  c)
    
    peano3d(s, x+s*(2*a.x+2*b.x+c.x), y+s*(2*a.y+2*b.y+c.y), z+s*(2*a.z+2*b.z+c.z), -a, -b,  c)
    peano3d(s, x+s*(a.x+2*b.x+c.x),   y+s*(a.y+2*b.y+c.y),   z+s*(a.z+2*b.z+c.z),    b, -a, -c)
    peano3d(s, x+s*(2*b.x+c.x),       y+s*(2*b.y+c.y),       z+s*(2*b.z+c.z),       -a, -b,  c)
    peano3d(s, x+s*(b.x+c.x),         y+s*(b.y+c.y),         z+s*(b.z+c.z),         -b,  a, -c)
    peano3d(s, x+s*(a.x+b.x+c.x),     y+s*(a.y+b.y+c.y),     z+s*(a.z+b.z+c.z),      a,  b,  c)
    peano3d(s, x+s*(2*a.x+b.x+c.x),   y+s*(2*a.y+b.y+c.y),   z+s*(2*a.z+b.z+c.z),   -b,  a, -c)
    peano3d(s, x+s*(2*a.x+c.x),       y+s*(2*a.y+c.y),       z+s*(2*a.z+c.z),       -a, -b,  c)
    peano3d(s, x+s*(a.x+c.x),         y+s*(a.y+c.y),         z+s*(a.z+c.z),          b, -a, -c)
    peano3d(s, x+s*c.x,               y+s*c.y,               z+s*c.z,               -a, -b,  c)

    peano3d(s, x+s*2*c.x,             y+s*2*c.y,             z+s*2*c.z,              b,  a,  c)
    peano3d(s, x+s*(a.x+2*c.x),       y+s*(a.y+2*c.y),       z+s*(a.z+2*c.z),        a, -b, -c)
    peano3d(s, x+s*2*(a.x+c.x),       y+s*2*(a.y+c.y),       z+s*2*(a.z+c.z),        b,  a,  c)
    peano3d(s, x+s*(2*a.x+b.x+2*c.x), y+s*(2*a.y+b.y+2*c.y), z+s*(2*a.z+b.z+2*c.z), -a,  b, -c)
    peano3d(s, x+s*(a.x+b.x+2*c.x),   y+s*(a.y+b.y+2*c.y),   z+s*(a.z+b.z+2*c.z),   -b, -a,  c)
    peano3d(s, x+s*(b.x+2*c.x),       y+s*(b.y+2*c.y),       z+s*(b.z+2*c.z),       -a,  b, -c)
    peano3d(s, x+s*2*(b.x+c.x),       y+s*2*(b.y+c.y),       z+s*2*(b.z+c.z),        b,  a,  c)
    peano3d(s, x+s*(a.x+2*b.x+2*c.x), y+s*(a.y+2*b.y+2*c.y), z+s*(a.z+2*b.z+2*c.z),  a, -b, -c)
    peano3d(s, x+s*2*(a.x+b.x+c.x),   y+s*2*(a.y+b.y+c.y),   z+s*2*(a.z+b.z+c.z),    b,  a,  c)


def createMeshFromData(name, origin):
    me = bpy.data.meshes.new(name + 'Mesh')     # create mesh and object
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = False

    bpy.context.collection.objects.link(ob)     # link object to scene and make active
    ob.select_set(True)

    me.from_pydata(verts, edges, [])            # create mesh from given verts, edges, faces
    me.update()                                 # update mesh with new data

    return ob         


name = "hilbert"
hilbert2d(8, 0, 0, L(1, 0), L(0, 1))
# hilbert3d(16, 0, 0, 0, L(1, 0, 0), L(0, 1, 0), L(0, 0, 1))
#
# name = "peano"
# peano2d(27, 0, 0, L(1, 0), L(0, 1))	
# peano3d(3, 0, 0, 0, L(1, 0, 0), L(0, 1, 0), L(0, 0, 1))
#
cleanEdges()
createMeshFromData(name, (0, 0, 0))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# point on line alternative (little slower)
#
# def pointOnLine(p, a, b): 
#     dx = b.x - a.x
#     dy = b.y - a.y
#     dz = b.z - a.z 
#     d = dx*dx + dy*dy + dz*dz 
# 
#     if d == 0:
#         return False
# 
#     ex = p.x - a.x
#     ey = p.y - a.y
#     ez = p.z - a.z
#     e = ex*ex + ey*ey + ez*ez
# 
#     if e == 0:
#         return False
# 
#     q = dx*ex + dy*ey + dz*ez
#     q = (q * q) / (d * e)
# 
#     return q >= 1.0 - 1E-10

# mark start points of curves
#     
# def markStart():
#     global verts, edges
# 
#     verts += [(verts[0][0]-.2, verts[0][1], verts[0][2])]
#     verts += [(verts[0][0]+.2, verts[0][1], verts[0][2])]
#     edges += [(len(verts)-2, len(verts)-1)]
# 
#     verts += [(verts[0][0], verts[0][1]-.2, verts[0][2])]
#     verts += [(verts[0][0], verts[0][1]+.2, verts[0][2])]
#     edges += [(len(verts)-2, len(verts)-1)]
# 
#     verts += [(verts[0][0], verts[0][1], verts[0][2]-.2)]
#     verts += [(verts[0][0], verts[0][1], verts[0][2]+.2)]
#     edges += [(len(verts)-2, len(verts)-1)]

# list variations hilbert/peano 2d
#
# dir = { 'a': L(1, 0), 'b': L(0, 1) }
# x = -3 * 4
# 
# for s in range(4):
#     for i in sorted(dir):    
#         for j in sorted(dir):
#             if(i[-1] != j[-1]):
#                 verts = []
#                 edges = []
# 
#                 si = '-' if i=='a' and s&2 or i=='b' and s&1 else '+'
#                 sj = '-' if j=='a' and s&2 or j=='b' and s&1 else '+'
# 
#                 name = "{}{}".format(si+i, sj+j)
# 
#                 a = dir[i] if si=='+' else -dir[i]
#                 b = dir[j] if sj=='+' else -dir[j]
# 
#                 # hilbert2d(2, 0, 0, a, b)
#                 peano2d(3, 0, 0, a, b)
# 
#                 markStart()
#                 createMeshFromData(name, (x, 0, 0))
#                 x += 3

# list variations hilbert/peano 3d
#
# dir = { 'a': L(1, 0, 0), 'b': L(0, 1, 0), 'c': L(0, 0, 1) }
# 
# x = -2.75
# y = - 3.25
# 
# for s in range(8):
#     for i in sorted(dir):    
#         for j in sorted(dir):
#             for k in sorted(dir):
#                 if(i!=j and i!=k and j!=k):
#                     verts = []
#                     edges = []
# 
#                     si = '-' if i=='a' and s&4 or i=='b' and s&2 or i=='c' and s&1 else '+'
#                     sj = '-' if j=='a' and s&4 or j=='b' and s&2 or j=='c' and s&1 else '+'
#                     sk = '-' if k=='a' and s&4 or k=='b' and s&2 or k=='c' and s&1 else '+'
# 
#                     name = "{}{}{}".format(si+i, sj+j, sk+k)
# 
#                     a = dir[i] if si=='+' else -dir[i]
#                     b = dir[j] if sj=='+' else -dir[j]
#                     c = dir[k] if sk=='+' else -dir[k]
# 
#                     hilbert3d(2, 0, 0, 0, a, b, c)
#                     # peano3d(3, 0, 0, 0, a, b, c)
# 
#                     markStart()
#                     createMeshFromData(name, (x*4, y*4, 0))
# 
#                     x += 1
#                     
#                     if x >= 3:
#                         y += 1
#                         x = -2.75

# draw edges without vertices in between, not entirely developed, last vertex missing
#
# lc = Triple(0, 0, 0)                            # last coordinate
# c0 = Triple(True, True, True)                   # change state 0
# 
# def draw(x, y, z):
#     global verts, edges, lc, c0
# 
#     c1 = Triple(lc.x!=x, lc.y!=y, lc.z!=z)      # change state 1
# 
#     if c0.x ^ c1.x or c0.y ^ c1.y or c0.z ^ c1.z:
#         verts += [(lc.x*scale.x, lc.y*scale.y, lc.z*scale.z)]
#         n = len(verts)
# 
#         if n > 1:
#             edges += [(n-2, n-1)]
# 
#     lc = Triple(x, y, z)
#     c0 = c1

# hilbert 2d
# 
# def hilbert2d(s, x, y, a, b):
#     if s == 1:
#         draw(x, y, 0)
#         return
# 
#     s >>= 1
# 
#     hilbert2d(s, x+s*a,     y+s*a,       a, 1-b)
#     hilbert2d(s, x+s*b,     y+s*(1-b),   a,   b)
#     hilbert2d(s, x+s*(1-a), y+s*(1-a),   a,   b)
#     hilbert2d(s, x+s*(1-b), y+s*b,     1-a,   b)

# peano 2d, variation
#
# peano2d(3, 0, 0, 0, 0)	
# 
# def peano2d_2(s, x, y, a, b):
#     if s == 1:
#         draw(x, y, 0)
#         return
# 
#     s //= 3
# 
#     peano2d(s, x+s*2*a,     y+s*2*a,       a,   b)
#     peano2d(s, x+s*(a-b+1), y+s*(a+b),     a, 1-b)
#     peano2d(s, x+s,         y+s,           a, 1-b)
#     peano2d(s, x+s*(a+b),   y+s*(a-b+1), 1-a, 1-b)
#     peano2d(s, x+s*2*b,     y+s*2*(1-b),   a,   b)
#     peano2d(s, x+s*(1+b-a), y+s*(2-a-b),   a,   b)
#     peano2d(s, x+s*2*(1-a), y+s*2*(1-a),   a,   b)
#     peano2d(s, x+s*(2-a-b), y+s*(1+b-a), 1-a,   b)
#     peano2d(s, x+s*2*(1-b), y+s*2*b,     1-a,   b)

# some math
#
# Z-axis
#     |cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|        -90: x*0 + y*1       90: x*0 - y*1
#     |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|            -x*1 + y*0           x*1 + y*0 
#     |  0       0      1| |z|   |        z        |   |z'|             z                   z

#  Y-axis               
#     | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|       -90: x*0 - z*1      90: x*0 + z*1
#     |   0      1       0| |y| = |         y        | = |y'|            y                  y
#     |−sin θ    0   cos θ| |z|   |−x sin θ + z cos θ|   |z'|            x*1 + z*0         -x*1 + z*0

# X-axis
#     |1     0           0| |x|   |        x        |   |x'|        -90: x              90: x
#     |0   cos θ    −sin θ| |y| = |y cos θ − z sin θ| = |y'|             y*0 + z*1          y*0 - z*1
#     |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|            -y*1 + z*0          y*1 + z*0

# links
#
# https://stackoverflow.com/questions/48296165/check-if-a-3d-point-lies-on-a-given-3d-linebetween-two-3d-points
