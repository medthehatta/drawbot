import pygame
import sys
import numpy as np

#############
# UTILITIES #
#############

def ziplist(*args):
    return list(zip(*args))




##################
# HELPER METHODS #
##################

def scale(value, target_scale = 1.0, source_scale = 1.0):
    return target_scale/source_scale * value

def rot2d(angle, vectors, about=[0,0]):
    """
    Rotates a vector (or group of vectors) about a point by a given angle (in
    degrees)
    """
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
# CLASSES #
###########

class Canvas(object):
    
    def __init__(self, rect, scale=1.0, pxres=72):
        self.rect = rect
        self.scale = scale
        self.pxres = pxres
        self.origin = \
                np.array([self.rect.get_width(), self.rect.get_height()])/2.

    def canvas_coords(self, x, rel=False):
        x = np.array(x)
        if rel:
            our_offset = 0
        else:
            our_offset = self.origin
        return transform(x*[1,-1],
                offset=our_offset,
                scale=self.pxres*self.scale)

    def world_coords(self, x, rel=False):
        x = np.array(x)
        if rel:
            our_offset = 0
        else:
            our_offset = -self.origin/(self.pxres*self.scale)
        return transform(x,
                offset=our_offset,
                scale=1/(self.pxres*self.scale))*[1,-1]

    def clear_canvas(self):
        return self.rect.fill([255]*3)

    def draw_lines(self,lines):
        for lineset in lines:
            lineset = list(self.canvas_coords(lineset))
            pygame.draw.aalines(self.rect,
                [0]*3,
                False,
                lineset)

    def scale_to(self, pos, scale_chg=0.1):
        pos_before = self.world_coords(pos)
        self.scale *= (1 + scale_chg)
        pos_after = self.world_coords(pos)
        delta = pos_after - pos_before
        self.origin += self.canvas_coords(delta, rel=True)



class MechanismDrawing(object):

    def __init__(self, disc_radius=1, arm_length=2):
        # Geometry of the mechanism
        self.disc_radius = disc_radius
        self.arm_length = arm_length
        # arm starts pointing up in the mechanism coords
        self.arm_zero = 0
        # increasing arm angle decreases angle in mechanism coords
        self.arm_angle_direction = -1
        # disc starts pointing up in the mechanism coords
        self.disc_zero = 0
        # increasing disc angle increases angle in mechanism coords
        self.disc_angle_direction = -1

        # Kinematics of the mechanism
        self.disc_angle = 0
        self.arm_angle = 0

    def draw_mechanism(self):
        parts = [
            self.draw_arm(),
            self.draw_disc(),
        ]
        return sum(parts, [])

    def draw_arm(self):
        base_radius = 0.15

        # offset between center of disc and pivot of arm
        arm_offset = [0, -self.arm_length]

        # points in the arm body and head
        # (converted to local coords from greg's VB code
        body_pts = [
            [-0.04971916,  0.94869806],
            [-0.06975647,  0.99756405],
            [-0.05390603,  1.02858842],
            [-0.02722403,  1.03964362],
            [-0.04361939,  0.99904822],
            [-0.03046844,  0.96952136],
            [ 0.        ,  0.96      ],
            [ 0.03046844,  0.96952136],
            [ 0.04361939,  0.99904822],
            [ 0.02722403,  1.03964362],
            [ 0.05390603,  1.02858842],
            [ 0.06975647,  0.99756405],
            [ 0.04971916,  0.94869806],
        ]
        body_pts = transform(body_pts, offset=arm_offset)

        # points that make up a vertical arm
        pts = [ \
            # "base"
            circle(base_radius, end=-180),
            # line across base
            [[-base_radius,0], [base_radius,0]],
            # arm head, with body attached
            [[-base_radius,0]] + \
            (2*np.array(body_pts)).tolist() + \
            [[base_radius,0]],
        ]

        # arm angle in world coordinates
        world_arm_angle = \
            self.arm_zero + self.arm_angle_direction*self.arm_angle
        
        transformed = [\
            transform(pts, 
            offset=arm_offset,
            angle=world_arm_angle)
            for pts in pts]

        return transformed

    def draw_disc(self):
        disc_radius = self.disc_radius

        # points that make up a disc with marks 
        # n.b. that the disc center is at the origin of the world
        pts = [circle(disc_radius, resolution=50)]

        # 8 radial lines, evenly spaced
        pts += [radial_line(0.9*disc_radius, disc_radius, angle=theta)
                for theta in np.linspace(0,360,12)]

        # disc angle in world coordinates
        world_disc_angle = self.disc_angle_direction*self.disc_angle
        
        transformed = [\
            transform(pts, 
            angle=world_disc_angle)
            for pts in pts]

        return transformed



###############
# ENTRY POINT #
###############


def run_game():
    # Game parameters
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

    pygame.init()
    screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    # Instantiate a mechanism drawing
    mechanism = MechanismDrawing()
    canvas = Canvas(screen)

    # The main game loop
    #
    while True:
        # Limit frame speed to 50 FPS
        #
        time_passed = clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    exit_game()
                
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[1]:
                    canvas.origin += event.rel

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if event.button == 3:
                    print("Canvas: " + str(pos))
                    print("World:  " + str(canvas.world_coords(pos)))
  
                elif event.button in [4,5]:
                    pressed = pygame.key.get_pressed()
                    mods = pygame.key.get_mods()

                    diff = 5
                    if mods & pygame.KMOD_SHIFT: diff = 10
                    if mods & pygame.KMOD_CTRL: diff = 1
                    if event.button == 5: diff = -diff 

                    if pressed[pygame.K_a]:
                        mechanism.arm_angle += diff
                    if pressed[pygame.K_d]:
                        mechanism.disc_angle += diff
                    if pressed[pygame.K_l]:
                        mechanism.arm_length += diff/50.
                    if pressed[pygame.K_r]:
                        mechanism.disc_radius += diff/50.

                    if not pressed[pygame.K_d] and \
                       not pressed[pygame.K_a] and \
                       not pressed[pygame.K_l] and \
                       not pressed[pygame.K_r]:
                        canvas.scale_to(pos, (diff/50.))

        # Redraw the mechanism
        canvas.clear_canvas()
        canvas.draw_lines(mechanism.draw_mechanism())

        pygame.display.flip()


def exit_game():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    run_game()

