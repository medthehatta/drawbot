import geometry
import pygame

from numpy import array

class Canvas(geometry.CoordinateSystem):
    def __init__(self, rect, scale=1.0, pxres=72, parent=None):
        self.rect = rect
        self.children = []
        self.parent = None
        if parent: self.parent_to(parent)
        self.pxres = pxres
        self.scale = scale
        super().__init__(
            origin=[self.rect.width/2., self.rect.height/2.],
        )

    def parent_to(self, parent):
        self.parent = parent
        self.parent.children.append(self)
        return self

    def stretch(self, factor=1.0):
        self.scale = self.scale*factor
        return self

    def center_to_rect(self):
        origin = [self.rect.width/2., self.rect.get_height()/2.]
        self.origin = array(origin)
        return self

    def canvas_coords(self, x, rel=False):
        """Coordinates on the canvas, given coordinates in the world"""
        return self.from_coords(x,rel)*[1,-1]

    def world_coords(self, x, rel=False):
        """Coordinates in the world, given coordinates on the canvas"""
        print(str(self) + ' converting coordinates ' + str(x))
        if self.parent is None:
            print(str(self) + ' parent is None')
            return self.to_coords(x,rel)
        else:
            print(str(self) + ' parent is ' + str(self.parent))
            return self.parent.world_coords(self.to_coords(x,rel),rel)

    def clear_canvas(self):
        return self.rect.fill([255]*3)

    def draw_lines(self,lines):
        """For a list consisting of lists of points, draw lines connecting the
        points in each list.  (Each list is a disjoint image)."""
        for lineset in lines:
            lineset_x = self.pxres*self.canvas_coords(lineset)*[1,1,-0]
            lineset = list(lineset_x)
            pygame.draw.aalines(self.rect, [0]*3, False, lineset)
        return self

    def draw_points(self,pts):
        for pt in pts:
            pt = self.pxres*self.canvas_coords(pt)*[1,-1]
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

