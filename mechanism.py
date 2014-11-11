import numpy as np

class MechanismModel(object):
    def __init__(self, disc_radius=5, arm_length=7):
        # Geometry of the mechanism
        self.disc_radius = disc_radius
        self.arm_length = arm_length

        # Kinematics of the mechanism
        self.disc_angle = 0
        self.arm_angle = 0

    def get_disc_radius(self): return self.disc_radius
    def get_arm_length(self): return self.arm_length
    def get_disc_angle(self): return self.disc_angle
    def get_arm_angle(self): return self.arm_angle



class MechanismDrawing(object):
    def __init__(self, model):
        # Use the passed-in MechanismModel
        self.model = model

        # Geometry data only relevant for display
        # arm starts pointing up in the mechanism coords
        self.arm_zero = 0
        # increasing arm angle decreases angle in mechanism coords
        self.arm_angle_direction = -1
        # disc starts pointing up in the mechanism coords
        self.disc_zero = 0
        # increasing disc angle increases angle in mechanism coords
        self.disc_angle_direction = -1

    def draw_mechanism(self):
        parts = [
            self.draw_arm(),
            self.draw_disc(),
        ]
        return sum(parts, [])

    def draw_arm(self):
        base_radius = self.model.get_disc_radius()/10.

        # offset between center of disc and pivot of arm
        arm_offset = [0, -self.model.get_arm_length()]

        # points in the arm head
        # (converted to local coords from greg's VB code
        head_pts = [
            [-0.04971916,  0.94869806-1],
            [-0.06975647,  0.99756405-1],
            [-0.05390603,  1.02858842-1],
            [-0.02722403,  1.03964362-1],
            [-0.04361939,  0.99904822-1],
            [-0.03046844,  0.96952136-1],
            [ 0.        ,  0.96      -1],
            [ 0.03046844,  0.96952136-1],
            [ 0.04361939,  0.99904822-1],
            [ 0.02722403,  1.03964362-1],
            [ 0.05390603,  1.02858842-1],
            [ 0.06975647,  0.99756405-1],
            [ 0.04971916,  0.94869806-1],
        ]
        # scale the points in the head to match the base, and put the head into
        # the center of the disk
        head_pts = transform(
            head_pts, 
            offset=[0, self.model.get_arm_length()],
            scale=10*base_radius
        ).tolist()

        # points that make up a vertical arm
        pts = [ 
            # "base"
            circle(base_radius, end=-180),
            # line across base
            [[-base_radius,0], [base_radius,0]],
            # arm head, with body attached
            [[-base_radius,0]] + head_pts + [[base_radius,0]],
        ]

        # arm angle in world coordinates
        world_arm_angle = \
            self.arm_zero + self.arm_angle_direction*self.model.get_arm_angle()
 
        transformed = [
            transform(pts, offset=arm_offset, angle=world_arm_angle)
            for pts in pts
        ]

        return transformed

    def draw_disc(self):
        disc_radius = self.model.get_disc_radius()

        # points that make up a disc with marks 
        # n.b. that the disc center is at the origin of the world
        pts = [circle(disc_radius, resolution=50)]

        # 8 radial lines, evenly spaced
        pts += [
            radial_line(0.9*disc_radius, disc_radius, angle=theta)
            for theta in np.linspace(0,360,12)
        ]

        # disc angle in world coordinates
        world_disc_angle = self.disc_angle_direction*self.model.get_disc_angle()
        
        transformed = [
            transform(pts, angle=world_disc_angle)
            for pts in pts
        ]

        return transformed

