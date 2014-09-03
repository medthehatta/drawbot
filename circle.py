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

def transform(vectors, offset=[0,0], angle=0, scale=1.0, one=False):
    vectors = np.array(vectors)
    rotated = scale*rot2d(angle,vectors)
    transformed = offset + rotated
    # If requested, return a single vector
    if one:
        return transformed[0]
    else:
        return transformed

def circle(radius, center=[0,0], start=0, end=360, resolution=10):
    pts = [rot2d(th, [[1,0]])[0] for th in np.linspace(start, end, resolution)]
    return transform(pts, offset=center, scale=radius)





###########
# CLASSES #
###########

class Canvas(object):
    
    def __init__(self):
        self.SCREEN_WIDTH = 400
        self.SCREEN_HEIGHT = 400
        self.BG_COLOR = (255, 255, 255)

        self.scale = 1.0
        self.pxres = 72
        self.origin = np.array([self.SCREEN_WIDTH, self.SCREEN_HEIGHT])/2.

    def canvas_coords(x):
        return transform(x, 
                offset=self.origin, 
                scale=self.pxres*self.scale,
                one=1)


class MechanismDrawing(object):

    def __init__(self, disc_radius=1, arm_length=1):
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
        # offset between center of disc and pivot of arm
        self.arm_offset = [0, -self.arm_length]

        # Kinematics of the mechanism
        self.disc_angle = 0
        self.arm_angle = 0

    def draw_arm(self):
        base_radius = 0.1*self.arm_length

        # points that make up a vertical arm
        arm_pts = [ \
            # "base"
            circle(base_radius, end=-180),
            # line across base
            [[-base_radius,0], [base_radius,0]],
            # lines connecting head and base
            [[-base_radius,0], [-base_radius,self.arm_length]],
            [[base_radius,0], [base_radius,self.arm_length]],
            # "head"
            circle(base_radius, end=180, center=[0,self.arm_length])]

        # arm angle in world coordinates
        world_arm_angle = \
            self.arm_zero + self.arm_angle_direction*self.arm_angle
        
        transformed = [\
            transform(pts, 
            offset=self.arm_offset,
            angle=world_arm_angle)
            for pts in arm_pts]

        return transformed



###############
# ENTRY POINT #
###############


def run_game():
    # Game parameters
    SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
    BG_COLOR = (255, 255, 255)

    pygame.init()
    screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()

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
                if event.key == pygame.K_ESCAPE:
                    exit_game()

        # Redraw the background
        screen.fill(BG_COLOR)

        pygame.display.flip()


def exit_game():
    sys.exit()

if __name__ == '__main__':
    pass
    #run_game()

