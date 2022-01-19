"""The main elements are divided in classes."""
import math

import pygame
from math import sin, cos, atan
import random


class Background:
    """ Initializes and draws the field, trajectory plot and text for our simulation"""
    def __init__(self, screen):

        self.field = pygame.image.load("images/field.jpg").convert()
        self.trajectory = pygame.image.load("images/trajectory.jpeg").convert()
        self.screen = screen

    def draw(self):
        self.screen.blit(self.field, (0, 2))
        self.screen.blit(self.trajectory, (940, 2))


class Balls:
    """Initializes, updates and draws the balls on the field and on the plot"""

    def __init__(self, xs, ys, screen):
        self.ball_t = pygame.image.load("images/ball.png").convert_alpha()
        self.ball_t_cx = 1042
        self.ball_t_cy = 412
        self.ball_t_rect = self.ball_t.get_rect(center=(self.ball_t_cx, self.ball_t_cy))

        self.ball_f = pygame.image.load("images/ball.png").convert_alpha()
        self.ball_f_cx = 466
        self.ball_f_cy = 822
        self.ball_f_rect = self.ball_t.get_rect(center=(self.ball_f_cx, self.ball_f_cy))

        self.traj_xscale, self.traj_yscale = 450/140, 350/40
        self.field_scale = 1/0.1484

        self.screen = screen

    def draw(self):
        self.screen.blit(self.ball_t, self.ball_t_rect)
        self.screen.blit(self.ball_f, self.ball_f_rect)

    def update(self, x, y, angle):
        self.ball_t_rect.center = (self.ball_t_cx + int(x * self.traj_xscale),
                                   self.ball_t_cy - int(y * self.traj_yscale))
        self.ball_f_rect.center = (self.ball_f_cx + int(cos(angle)*x * self.field_scale),
                                   self.ball_f_cy - int(sin(angle)*x * self.field_scale))


class Glove:
    """Initializes, updates and draws the glove on the field."""

    def __init__(self, screen):
        self.glove = pygame.image.load("images/glove.png").convert_alpha()
        self.screen = screen
        self.max_speed = 22
        self.dt = 1/50

        # this list was created by saving the positions of the mouse when clicked on the field in various places
        self.positions = [(225, 553), (190, 501), (144, 465), (130, 445), (108, 417), (52, 365),
                          (40, 317), (49, 286), (71, 231), (96, 271), (86, 312), (90, 366),
                          (137, 389), (167, 434), (226, 447), (266, 436),  (264, 496),
                          (245, 561), (292, 457), (309, 444), (334, 416),  (408, 381),
                          (525, 379), (549, 380), (631, 413), (687, 461),  (707, 537),
                          (703, 558), (692, 584), (724, 525), (758, 494),  (819, 438),
                          (923, 381), (920, 363), (913, 348), (860, 305), (798, 371),
                          (761, 354), (846, 315), (841, 290), (719, 281),  (635, 376),
                          (605, 346), (712, 290), (801, 238), (863, 236), (924, 356),
                          (662, 83), (575, 35), (529, 16), (466, 15), (377, 24), (283, 72),
                          (168, 135), (117, 164), (96, 193), (70, 248), (58, 305), (279, 140),
                          (163, 339), (286, 211), (260, 344), (206, 431), (293, 462), (309, 395),
                          (350, 140), (337, 271), (253, 366), (214, 297), (278, 262), (324, 153),
                          (232, 246), (366, 339), (366, 368), (410, 364), (386, 305), (327, 225),
                          (379, 62), (411, 74), (369, 151), (439, 207), (389, 239), (447, 296),
                          (448, 345), (489, 365), (512, 335), (431, 259), (491, 232), (521, 237),
                          (450, 132), (540, 108), (516, 65), (468, 38), (485, 33), (557, 113),
                          (537, 230), (579, 277), (526, 329), (548, 377), (522, 387), (560, 394),
                          (577, 348), (559, 295), (633, 274), (543, 231), (603, 186), (598, 181),
                          (579, 120), (572, 98), (597, 65), (626, 58), (626, 104), (723, 146),
                          (657, 85), (676, 160), (713, 190), (647, 209), (652, 255), (672, 264),
                          (608, 294), (647, 309), (674, 339), (582, 353), (579, 371), (577, 392),
                          (616, 419), (620, 448), (636, 437), (629, 400), (705, 325), (703, 395),
                          (674, 451), (694, 473), (711, 514), (775, 492), (733, 451), (776, 428),
                          (809, 411), (686, 338), (785, 315), (724, 402), (868, 371), (934, 362),
                          (837, 284), (836, 236), (682, 273), (734, 334), (763, 234), (772, 221),
                          (587, 308), (444, 279), (292, 390), (232, 374), (336, 191), (496, 179)]

        self.glove_pos = random.choice(self.positions)
        self.x, self.y = self.glove_pos[0], self.glove_pos[1]
        self.xo, self.yo = self.glove_pos[0], self.glove_pos[1]
        self.glove_rect = self.glove.get_rect(center=(self.x, self.y))
        self.pitcher_x = 466
        self.pitcher_y = 822

    def draw(self):
        self.screen.blit(self.glove, self.glove_rect)

    def position_to_pitcher(self):
        """Return the x,y distance of the glover relative to pitcher"""
        x = self.x - self.pitcher_x

        y = -self.y + self.pitcher_y

        return x*0.1484, y*0.1484

    def glove_to_ball(self, ball_pos):
        """ Calculates angle between the outfielder and the projection of the ball
        on the ground. and the distance between them."""

        glove_pos = self.position_to_pitcher()
        distance = ((glove_pos[1] - ball_pos[1])**2 + (glove_pos[0] - ball_pos[0])**2)**0.5

        return atan(abs((glove_pos[1] - ball_pos[1])/abs((glove_pos[0] - ball_pos[0])))), distance

    def vertical_angle(self, distance, ball_pos):
        return math.atan(ball_pos[2]/distance) * 360/6.281

    def move(self, ball_pos):

        angle, distance = self.glove_to_ball(ball_pos)

        v_angle = self.vertical_angle(distance, ball_pos)

        if distance + 0.5 < self.dt * self.max_speed:
            speed = distance/self.dt
        else:
            speed = self.max_speed
        x, y = self.position_to_pitcher()

        if x > ball_pos[0]:
            if y > ball_pos[1]:
                a = -1
                b = 1
            else:
                a = -1
                b = -1
        else:
            if y > ball_pos[1]:
                a = 1
                b = 1
            else:
                a = 1
                b = -1

        self.x += int(speed * self.dt * cos(angle)/0.1418) * a
        self.y += int(speed * self.dt * sin(angle)/0.1418) * b
        self.glove_rect = self.glove.get_rect(center=(self.x, self.y))
        return round(distance, 2), round(v_angle, 2), round(angle*360/6.28, 2)

    def reset(self):
        self.x = self.xo
        self.y = self.yo
        self.glove_rect = self.glove.get_rect(center=(self.x, self.y))


class Button:
    def __init__(self, text, width, height, pos, font):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (200, 200, 200)
        self.pressed = False

        self.text_surf = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(*mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                    return True
        return False


class Text:
    def __init__(self, font, pos, width, height, text):
        self.font = font
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (255, 255, 255)
        self.text = text

        self.text_surf = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, screen):
        self.text_surf = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(self.text_surf, self.text_rect)


class ChangingText(Text):
    def __init__(self, font, pos, width, height, text, value, name, units):
        super().__init__(font, pos, width, height, text)
        self.value = value
        self.name = name
        self.units = units
        self.text_surf = self.font.render(f"{name} in {units}: {self.value}", True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self, value, screen):
        self.value = value

        self.text_surf = self.font.render(f"{self.name} in {self.units} : {self.value}", True, (0, 0, 0))
        screen.blit(self.text_surf, self.text_rect)
