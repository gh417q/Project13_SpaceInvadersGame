from turtle import Screen, Turtle
from barrier import Barrier
from time import sleep

INIT_Y = 30
DEFENDER_IMAGE_WIDTH = 50
DEFENDER_IMAGE_HEIGHT = 64
BULLET_COLOR = "red"
BULLET_SPEED = 8
DEFENDER_IMAGE = "images/defender.gif"
DEFENDER_HIT_IMAGE = "images/defender_hit.gif"
OUTSIDE = 1000
STEP = 10

class Defender(Turtle):

    def __init__(self, screen_height, screen: Screen):

        super().__init__()
        self.screen_top = screen_height//2 + 10
        screen.addshape(DEFENDER_IMAGE)
        screen.addshape(DEFENDER_HIT_IMAGE)
        self.screen = screen
        self.shape(DEFENDER_IMAGE)
        self.penup()
        self.pos_Y = -screen_height//2 + INIT_Y
        self.goto(0, self.pos_Y)
        self.bullet = Turtle()
        self.bullet.color(BULLET_COLOR)
        self.bullet.setheading(90)
        self.bullet.penup()
        self.bullet.goto(0, OUTSIDE)  # outside the screen

    def move(self, direction: int):
        self.goto(self.pos()[0] + STEP*direction, self.pos_Y)

    def move_left(self):
        self.move(direction=-1)

    def move_right(self):
        self.move(direction=1)

    def shoot(self):
        if self.bullet.pos()[1] == OUTSIDE:  # not on screen, can be used as no shooting while previously shot bullet is still flying
            self.bullet.goto(self.pos()[0], self.pos()[1] + DEFENDER_IMAGE_HEIGHT - 10)

    def reset_bullet(self):
        self.bullet.goto(0, OUTSIDE)  # outside the screen

    def bullet_flies(self):
        if self.bullet.pos()[1] != OUTSIDE:
            self.bullet.forward(BULLET_SPEED)
        if self.bullet.pos()[1] > self.screen_top:  # recycle it
            self.reset_bullet()

    def hit_barrier(self, barrier: Barrier):
        if self.bullet.pos()[1] != OUTSIDE:
            if barrier.check_hit(bullet=self.bullet, by_defender=True):
                self.reset_bullet()

    def hit(self):
        self.shape(DEFENDER_HIT_IMAGE)
        self.screen.update()
        sleep(1)
        self.shape(DEFENDER_IMAGE)


