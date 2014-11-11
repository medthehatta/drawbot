import pygame
import sys
import numpy as np

import drawing
import geometry
import mechanism

from utilities import ziplist



###############
# ENTRY POINT #
###############


def run():
    # Game parameters
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

    pygame.init()
    screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    clock = pygame.time.Clock()

    # Instantiate a mechanism drawing
    model = mechanism.MechanismModel()
    mechanism = mechanism.MechanismDrawing(model)
    canvas = drawing.Canvas(screen)

    # The main game loop
    #
    while True:
        # Limit frame speed to 50 FPS
        #
        time_passed = clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

            # Keypresses
            elif event.type == pygame.KEYDOWN:

                # Exit
                if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    exit_game()

                # Recenter
                elif event.key == pygame.K_c:
                    print("centering")
                    canvas.set_scale(1.0)
                    canvas.center_to_rect()
 
            # Pan with middle-click
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[1]:
                    canvas.origin += event.rel

            # Other button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Print the position of the cursor with right click
                if event.button == 3:
                    print("Canvas: " + str(pos))
                    print("World:  " + str(canvas.world_coords(pos)))
  
                # Tune parameters with mousewheel and holding down key:
                # a - arm angle
                # d - disc angle
                # l - arm length
                # r - disc radius
                elif event.button in [4,5]:
                    pressed = pygame.key.get_pressed()
                    mods = pygame.key.get_mods()

                    diff = 5
                    if mods & pygame.KMOD_SHIFT: diff = 10
                    if mods & pygame.KMOD_CTRL: diff = 1
                    if event.button == 5: diff = -diff 

                    if pressed[pygame.K_a]:
                        model.arm_angle += diff
                    if pressed[pygame.K_d]:
                        model.disc_angle += diff
                    if pressed[pygame.K_l]:
                        model.arm_length += diff/50.
                    if pressed[pygame.K_r]:
                        model.disc_radius += diff/50.

                    # Otherwise, zoom in and out
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
    run()

