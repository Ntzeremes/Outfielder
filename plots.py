"""This is the code that calculates the trajectory of the ball.
    It also creates the plot for the trajectory.
"""

from math import sin, cos
import matplotlib.pyplot as plt
import numpy as np


def trajectory(v, angle):
    """Calculates trajectory, the time the ball takes to reach the ground
    , creates a plot of the trajectory and saves it in the folder "images".
    returns the x , y values of the trajectory, total time and the speed components of the ball."""

    g = 9.81
    dt = 1/50

    vx = v * cos(angle)  # x, y components of the speed
    vy = v * sin(angle)

    t_tot = np.roots([-g / 2, vy, 0])[0]  # the roots of y(t)

    def ball_height(x):
        """Using kinematic equations we calculate the trajectory of the ball, the height of the ball
         as a function of horizontal distance x"""
        height = (vy / vx) * x - g * (x ** 2) / (2 * vx ** 2)
        return height

    xs = [vx * t for t in np.arange(0, t_tot, dt)]
    ys = [ball_height(x) for x in xs]

    plt.plot(xs, ys)
    plt.title('The Trajectory of the Ball', pad=15)
    plt.xlabel('Horizontal Position of Ball (meters)')
    plt.ylabel('Vertical Position of Ball (meters)')
    plt.axhline(y=0)
    plt.ylim(0,40)
    plt.xlim(0,140)

    plt.savefig("images/trajectory.jpeg")

    return xs, vx, ys, vy, t_tot



