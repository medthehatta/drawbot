import numpy as np

def scale(value, target_scale = 1.0, source_scale = 1.0):
    return target_scale/source_scale * value

def rot2d(angle, vectors, about=[0,0]):
    """ Rotates a vector (or group of vectors) about a point by a given angle
    (in degrees)"""
    vs = np.array(vectors) - about
    angle_rad = np.radians(angle)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    R = np.array([[c, -s],[s, c]])
    return about + np.array([np.dot(R,v) for v in vs])

def transform(vectors, offset=[0,0], angle=0, scale=1.0):
    vectors = np.array(vectors)
    one = (len(vectors.shape)==1)
    if one: vectors = np.array([vectors])
    rotated = scale*rot2d(angle,vectors)
    transformed = offset + rotated
    # If requested, return a single vector
    if one:
        return transformed[0]
    else:
        return transformed

def circle(radius, center=[0,0], start=0, end=360, resolution=20):
    pts = [rot2d(th, [[1,0]])[0] for th in np.linspace(start, end, resolution)]
    return transform(pts, offset=center, scale=radius)

def radial_line(r0, r1, center=[0,0], angle=0):
    return transform([[0,r0], [0,r1]], offset=center, angle=angle)



###########
# Classes #
###########

class CoordinateSystem(object):
    def __init__(self, scale=1.0, origin=[0,0], angle=0.0):
        self.scale = scale
        self.origin = np.array(origin)
        self.angle = angle

    def to_coords(self, x, rel=False):
        """Coordinates of the system in world coordinates"""
        x = np.array(x)
        if rel:
            our_offset = 0
        else:
            our_offset = self.origin
        return transform(
            x,
            offset=our_offset,
            scale=self.scale,
            angle=self.angle,
        )

    def from_coords(self, x, rel=False):
        """Coordinates of the world in system coords"""
        x = np.array(x)
        if rel:
            our_offset = 0
        else:
            our_offset = -self.origin/self.scale
        return transform(
            x,
            offset=our_offset,
            angle=-self.angle,
            scale=1/self.scale,
        )

