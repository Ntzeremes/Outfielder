import plots
from plots import trajectory
import random
import pygame
from math import sin, cos
from classes import *
import os

# Constants and parameters
pygame.init()
WIDTH, HEIGHT = 1580, 920
FPS = 33
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PAD = 10


def initialize():
    """Calculates and returns the initial speed of the ball,
    the horizontal angle of the ball, and the vertical angle of the ball during the hit.
    The angles are in radians."""
    return random.uniform(25, 35), random.uniform(0.785, 2.355), random.uniform(0.45, 0.85)


def draw(screen, background, balls, xs, ys, counter, h_angle, glove, pause_button, repeat_button, new_button,
         distance_text, distance, text):
    """Draws all the elements on the screen. Contains all the individual functions for drawing"""
    screen.fill(WHITE)
    background.draw()
    balls.update(xs[counter], ys[counter], h_angle)

    glove.draw()
    balls.draw()
    pause_button.draw(screen)
    repeat_button.draw(screen)
    new_button.draw(screen)
    distance_text.draw(distance, screen)
    text.draw(screen)


# Simulation
def main():

    v, h_angle, v_angle = initialize()
    xs, vx, ys, vy, tmax = trajectory(v, v_angle)

    # PYGAME
    sim_over = False
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    pygame.display.set_caption("Outfielder")
    font = pygame.font.Font(None, 45)

    background = Background(screen)
    balls = Balls(xs, ys, screen)
    glove = Glove(screen)
    text = Text(font, (1132, 570), 200, 150, "Ball and outfielder")
    distance_text = ChangingText(font, (1100, 632), 200, 150, None, '--', "distance", "meters")
    v_angle_text = ChangingText(font, (1100, 684), 200, 150, None, "--", "vertical angle", "degrees")
    h_angle_text = ChangingText(font, (1100, 746), 200, 150, None, "--", "horizontal angle", "degrees")
    start_button = Button("Start", 150, 60, (30, 688), font)
    repeat_button = Button("Repeat", 150, 60, (30, 750), font)
    new_button = Button("New", 150, 60, (30, 820), font)
    glove.draw()
    balls.draw()

    counter = 0
    size = len(ys)

    start = False
    distance = "--"
    ve_angle = "--"
    ho_angle = "--"

    # The basic loop of our simulation
    while not sim_over:

        # A loop that breaks when we click the start button, so that our sim will start.
        # When pause is pressed we enter the loop again.
        while not start:
            draw(screen, background,balls, xs, ys, counter, h_angle, glove, start_button, repeat_button, new_button,
                 distance_text, distance, text)
            v_angle_text.draw(ve_angle, screen)
            h_angle_text.draw(ho_angle, screen)
            pygame.display.flip()
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sim_over = True
                    start = True

            if start_button.check_click():
                start = True
                start_button = Button("Pause", 150, 60, (30, 680), font)

            if repeat_button.check_click():
                counter = 0
                distance = "--"
                glove.reset()

            if new_button.check_click():
                v, h_angle, v_angle = initialize()
                xs, vx, ys, vy, tmax = trajectory(v, v_angle)
                background = Background(screen)
                balls = Balls(xs, ys, screen)
                glove = Glove(screen)
                counter = 0
                size = len(ys)
                distance = "--"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sim_over = True

        if counter < size - 1:

            distance, ve_angle, ho_angle = glove.move((xs[counter]*cos(h_angle), xs[counter]*sin(h_angle), ys[counter]))
            draw(screen, background,balls, xs, ys, counter, h_angle, glove, start_button, repeat_button, new_button,
                 distance_text, distance, text)
            v_angle_text.draw(ve_angle, screen)
            h_angle_text.draw(ho_angle, screen)

            counter += 1

        # The code for the buttons
        if start_button.check_click():
            start = False
            start_button = Button("Start", 150, 60, (30, 680), font)

        if repeat_button.check_click():
            counter = 0
            distance = "--"
            glove.reset()

        if new_button.check_click():
            v, h_angle, v_angle = initialize()
            xs, vx, ys, vy, tmax = trajectory(v, v_angle)
            background = Background(screen)
            balls = Balls(xs, ys, screen)
            glove = Glove(screen)
            counter = 0
            distance = "--"
            size = len(ys)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
