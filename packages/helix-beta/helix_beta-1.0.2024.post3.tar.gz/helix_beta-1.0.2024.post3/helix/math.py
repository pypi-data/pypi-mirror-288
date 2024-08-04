from .defines import *
from math import sqrt, atan, atan2, degrees, radians, sin, exp, log

vec2:pg.math.Vector2=pg.math.Vector2
vec3:pg.math.Vector3=pg.math.Vector3

def create_vector(x:float|int, y:float|int) -> pg.math.Vector2 :
    return vec2(x,y)

def get_magnitude(vector:pg.math.Vector2) -> pg.math.Vector2 :
    return sqrt( vector.x*vector.x + vector.y*vector.y )

def normalize(vector:pg.math.Vector2) -> pg.math.Vector2 :
    m = get_magnitude(vector)
    return vec2( vector.x/m, vector.y/m )

def pythag(v1:int|float, v2:int|float) -> float :
    return sqrt( (v1*v1) + (v2*v2) )

def dist_to(origin_vector2, target_vector2) -> pg.math.Vector2 :
    """
    Calculate the distance between the origin and the target vector along both the x and y axes.
    """
    delta_x = target_vector2.x - origin_vector2.x
    delta_y = target_vector2.y - origin_vector2.y
    return vec2((delta_x), (delta_y))

def clamp(num: int, min_value: int, max_value: int) -> int :
    """ Returns the number you input as long as its between the max and min values. """
    return max(min(num, max_value), min_value)

def sine_wave(phase, amplitude, frequency):
    return amplitude * sin(phase * frequency)
