import geometry
from numpy import array

class Canvas(geometry.CoordinateSystem):
    def __init__(self, rect, scale=1.0, pxres=72, parent=None):
        self.rect = rect
        self.parent = parent
        self.children = []
        self.pxres = pxres
        self.real_scale=scale
        super().__init__(
            origin=[self.rect.get_width()/2., self.rect.get_height()/2.],
        )
        self.set_scale(scale)

    def parent_to(self, parent):
        self.parent = parent
        self.parent.children.append(self)
        return self

    def set_scale(self, scale=1.0):
        self.real_scale = scale
        self.scale = self.pxres*self.real_scale
        return self

    def stretch(self, factor=1.0):
        return self.set_scale(self.real_scale*factor)

    def center_to_rect(self):
        origin = [self.rect.get_width()/2., self.rect.get_height()/2.]
        self.origin = array(origin)
        return self

    def canvas_coords(self, x, rel=False):
        """Coordinates on the canvas, given coordinates in the world"""
        return self.to_coords(x,rel)

    def world_coords(self, x, rel=False):
        """Coordinates in the world, given coordinates on the canvas"""
        return self.from_coords(x,rel)

    def clear_canvas(self):
        return self.rect.fill([255]*3)

    def draw_lines(self,lines):
        """For a list consisting of lists of points, draw lines connecting the
        points in each list.  (Each list is a disjoint image)."""
        for lineset in lines:
            lineset = list(self.canvas_coords(lineset))
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
        self.origin += self.canvas_coords(delta, rel=True)/self.pxres
        return self

