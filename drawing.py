import geometry
import pygame

from numpy import array

class Canvas(object):
    def __init__(self, rect, coords=None, pxres=72, 
                 scale=1.0, origin=[0,0], angle=0.0, parent=None):
        self.coords = coords or geometry.CoordinateSystem()
        parent_coords = None
        if parent is not None: parent_coords = parent.get_coords()
        self.coords.__init__(scale,origin,angle,parent_coords)
        self.rect = rect
        self.pxres = pxres
        self.origin = [self.rect.get_width()/2., self.rect.get_height()/2.]

    def get_coords(self):
        return self.coords

    def canvas_coords(self, x, rel=False):
        """Coordinates on the canvas, given coordinates in the world"""
        trans = (array(x) - self.origin)*[1,-1]/self.pxres
        return self.get_coords().from_coords(trans, rel)

    def world_coords(self, x, rel=False):
        """Coordinates in the world, given coordinates on the canvas"""
        trans = array(self.get_coords().to_coords(x,rel))
        return trans*[1,-1]*self.pxres + self.origin

    def clear_canvas(self):
        return self.rect.fill([255]*3)

    def draw_lines(self,lines):
        """For a list consisting of lists of points, draw lines connecting the
        points in each list.  (Each list is a disjoint image)."""
        for lineset in lines:
            lineset = list([self.canvas_coords(line) for line in lineset])
            pygame.draw.aalines(self.rect, [0]*3, False, lineset)
        return self

    def draw_points(self,pts):
        for pt in pts:
            pt = self.canvas_coords(pt)
            pygame.draw.circle(self.rect, [0]*3, pt, radius=1)
        return self

    def scale_to(self, pos=[0,0], scale_chg=0.1):
        """Scale the canvas, but also ensure that the cursor remains at the
        same point in world coordinates."""
        pos_before = self.world_coords(pos)
        self.stretch(1 + scale_chg)
        pos_after = self.world_coords(pos)
        delta = pos_after - pos_before
        self.origin += self.canvas_coords(delta, rel=True)
        return self

    def stretch(self, factor=1.0):
        self.coords.scale = self.coords.scale*factor
        return self

