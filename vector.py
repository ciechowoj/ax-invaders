from collections import namedtuple
from math import sqrt, sin, cos, tan

_named_tuple2 = namedtuple('vec2', 'x y')
_named_tuple3 = namedtuple('vec3', 'x y z')
_named_tuple4 = namedtuple('vec4', 'x y z w')
_named_tuple44 = namedtuple('mat4', 'xx xy xz xw yx yy yz yw zx zy zz zw wx wy wz ww')

class vec2(_named_tuple2):
    __slots__ = ()
    
    def __new__(cls, x = 0, y = 0):
        return _named_tuple2.__new__(cls, x, y)
        
    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"
        
    def __add__(a, b):
        return vec3(a.x + b.x, a.y + b.y)

    def __sub__(a, b):
        return vec3(a.x - b.x, a.y - b.y)

    def __mul__(a, b):
        return vec3(a.x * b.x, a.y * b.y)

    def __truediv__(a, b):
        return vec3(a.x / b.x, a.y / b.y)

    def __pos__(self):
        return vec3(self.x, self.y)

    def __neg__(self):
        return vec3(-self.x, -self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
        
    def __getattr__(self, name):
        if name == "length":
            return sqrt(self.x * self.x + self.y * self.y)
        elif name == "normal":
            inv = 1 / self.length
            return vec3(self.x * inv, self.y * inv)
            
class vec3(_named_tuple3):
    __slots__ = ()
    
    def __new__(cls, x = 0, y = 0, z = 0):
        return _named_tuple3.__new__(cls, x, y, z)
        
    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + "]"
        
    def __add__(a, b):
        return vec3(a.x + b.x, a.y + b.y, a.z + b.z)

    def __sub__(a, b):
        return vec3(a.x - b.x, a.y - b.y, a.z - b.z)

    def __mul__(a, b):
        return vec3(a.x * b.x, a.y * b.y, a.z * b.z)

    def __truediv__(a, b):
        return vec3(a.x / b.x, a.y / b.y, a.z / b.z)

    def __pos__(self):
        return vec3(self.x, self.y, self.z)

    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
        
    def __getattr__(self, name):
        if name == "length":
            return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        elif name == "normal":
            inv = 1 / self.length
            return vec3(self.x * inv, self.y * inv, self.z * inv)
            
class vec4(namedtuple('vec4', 'x y z w')):
    __slots__ = ()
    
    def __init__(self, x = 0, y = 0, z = 0, w = 0):
        self = (x, y, z, w)
        
    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.w) + "]"
        
    def __add__(a, b):
        return vec4(a.x + b.x, a.y + b.y, a.z + b.z, a.w + b.w)

    def __sub__(a, b):
        return vec4(a.x - b.x, a.y - b.y, a.z - b.z, a.w - b.w)

    def __mul__(a, b):
        return vec4(a.x * b.x, a.y * b.y, a.z * b.z, a.w * b.w)

    def __truediv__(a, b):
        return vec4(a.x / b.x, a.y / b.y, a.z / b.z, a.w / b.w)

    def __pos__(self):
        return vec4(self.x, self.y, self.z, self.w)

    def __neg__(self):
        return vec3(-self.x, -self.y, -self.z, -self.w)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w
        
    def __getattr__(self, name):
        if name == "length":
            return sqrt(self.x * self.x + self.y * self.y + self.z * self.z + self.w * self.w)
        elif name == "normal":
            inv = 1 / self.length
            return vec3(self.x * inv, self.y * inv, self.z * inv, self.w * inv)
           
class mat4(namedtuple('mat4', 'xx xy xz xw yx yy yz yw zx zy zz zw wx wy wz ww')):
    __slots__ = ()
    
    def __new__(cls, xx = 1, xy = 0, xz = 0, xw = 0, yx = 0, yy = 1, yz = 0, yw = 0, zx = 0, zy = 0, zz = 1, zw = 0, wx = 0, wy = 0, wz = 0, ww = 1):
        return _named_tuple44.__new__(cls, xx, xy, xz, xw, yx, yy, yz, yw, zx, zy, zz, zw, wx, wy, wz, ww)
        
    def __mul__(a, b):
        return mat4(
        a.xx * b.xx, a.xy * b.xy, a.xz * b.xz, a.xw * b.xw,
        a.yx * b.yx, a.yy * b.yy, a.yz * b.yz, a.yw * b.yw,
        a.zx * b.zx, a.zy * b.zy, a.zz * b.zz, a.zw * b.zw,
        a.wx * b.wx, a.wy * b.wy, a.wz * b.wz, a.ww * b.ww)

def cross3(a, b):
    return vec3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x)

def dot3(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z
    
def identity4():
    return mat4(
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1)

def translate4(x, y, z):
    return mat4(
        1, 0, 0, x,
        0, 1, 0, y,
        0, 0, 1, z,
        0, 0, 0, 1)

def mul4(a, b):
    return mat4(
    a.xx * b.xx + a.xy * b.yx + a.xz * b.zx + a.xw * b.wx,
    a.xx * b.xy + a.xy * b.yy + a.xz * b.zy + a.xw * b.wy,
    a.xx * b.xz + a.xy * b.yz + a.xz * b.zz + a.xw * b.wz,
    a.xx * b.xw + a.xy * b.yw + a.xz * b.zw + a.xw * b.ww,
    a.yx * b.xx + a.yy * b.yx + a.yz * b.zx + a.yw * b.wx,
    a.yx * b.xy + a.yy * b.yy + a.yz * b.zy + a.yw * b.wy,
    a.yx * b.xz + a.yy * b.yz + a.yz * b.zz + a.yw * b.wz,
    a.yx * b.xw + a.yy * b.yw + a.yz * b.zw + a.yw * b.ww,
    a.zx * b.xx + a.zy * b.yx + a.zz * b.zx + a.zw * b.wx,
    a.zx * b.xy + a.zy * b.yy + a.zz * b.zy + a.zw * b.wy,
    a.zx * b.xz + a.zy * b.yz + a.zz * b.zz + a.zw * b.wz,
    a.zx * b.xw + a.zy * b.yw + a.zz * b.zw + a.zw * b.ww,
    a.wx * b.xx + a.wy * b.yx + a.wz * b.zx + a.ww * b.wx,
    a.wx * b.xy + a.wy * b.yy + a.wz * b.zy + a.ww * b.wy,
    a.wx * b.xz + a.wy * b.yz + a.wz * b.zz + a.ww * b.wz,
    a.wx * b.xw + a.wy * b.yw + a.wz * b.zw + a.ww * b.ww)
          
def mul4v(m, v):
    return vec4(
        v.x * m.xx + v.y * m.xy + v.z * m.xz + v.w * m.xw,
        v.x * m.yx + v.y * m.yy + v.z * m.yz + v.w * m.yw,
        v.x * m.zx + v.y * m.zy + v.z * m.zz + v.w * m.zw,
        v.x * m.wx + v.y * m.wy + v.z * m.wz + v.w * m.ww)
  
def mul4p(m, v):
    return vec4(
        v.x * m.xx + v.y * m.xy + v.z * m.xz + m.xw,
        v.x * m.yx + v.y * m.yy + v.z * m.yz + m.yw,
        v.x * m.zx + v.y * m.zy + v.z * m.zz + m.zw,
        v.x * m.wx + v.y * m.wy + v.z * m.wz + m.ww)

def mul4c(m, v):
    return vec3(
        v.x * m.xx + v.y * m.xy + v.z * m.xz + m.xw,
        v.x * m.yx + v.y * m.yy + v.z * m.yz + m.yw,
        v.x * m.zx + v.y * m.zy + v.z * m.zz + m.zw)

def mul4n(m, v):
    return vec3(
        v.x * m.xx + v.y * m.xy + v.z * m.xz,
        v.x * m.yx + v.y * m.yy + v.z * m.yz,
        v.x * m.zx + v.y * m.zy + v.z * m.zz)

def perspective(fovy, aspect, znear, zfar):
    scale_y = 1 / tan(fovy * 0.5)
    scale_x = scale_y / aspect
    return mat4(xx = scale_x, yy = scale_y, zz = (zfar + znear) / (znear - zfar), wz = -1, zw = (2 * zfar * znear) / (znear - zfar), ww = 0)

def look_at(e, c):
    eye = vec3(e[0], e[1], e[2])
    center = vec3(c[0], c[1], c[2])
    up = vec3(0.0, 1.0, 0.0)
    x = y = z = vec3()
    z = eye - center
    z = z.normal
    x = cross3(up.normal, z).normal
    y = cross3(z, x).normal

    return mat4(
    x.x, x.y, x.z, -dot3(eye, x),
    y.x, y.y, y.z, -dot3(eye, y),
    z.x, z.y, z.z, -dot3(eye, z))
    