from turtle import Screen, Turtle
from random import randint
from barrier import Barrier
from time import sleep

ALIENS_WIDTH = 8
ALIENS_DEPTH = 3
GAP_X = 30
INIT_Y = 30
ALIEN_IMAGE = "images/alien.gif"
ALIEN_SHOT_IMAGE = "images/alien_shot.gif"
HIT_BULLET_IMAGE = "images/hit_bullet.gif"
ALIEN_IMAGE_WIDTH = 50
ALIEN_IMAGE_HEIGHT = 30
ALIEN_GAP = 10
DIRECTION_RIGHT = 1
DIRECTION_LEFT = -1
STEP = 1
TOTAL_BULLETS = 100
BULLET_COLOR = "yellow"
SHOOTING = 10
SHOOTING_PROBABILITY = 8
SHOOTING_PROBABILITY_BASE = 1000
SHOOTING_PROBABILITY_INCREASE_RATE = 3
BULLET_SPEED = 12
# HIT_SLEEP = 0.03


class Aliens:

    def __init__(self, screen_width: int, screen_height: int, background: str, screen: Screen):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background = background
        self.aliens = []
        self.shot_aliens = 0
        self.active_aliens = []
        screen.addshape(ALIEN_IMAGE)
        screen.addshape(ALIEN_SHOT_IMAGE)
        screen.addshape(HIT_BULLET_IMAGE)
        self.screen = screen
        self.left_column = 0
        self.right_column = ALIENS_WIDTH - 1
        self.direction = DIRECTION_RIGHT
        self.left_border = -self.screen_width//2 + GAP_X + ALIEN_IMAGE_WIDTH//2
        self.right_border = self.screen_width//2 - GAP_X - ALIEN_IMAGE_WIDTH//2
        self.shooting_probability = SHOOTING_PROBABILITY
        self.bullets = []
        self.shooting_bullets = []
        self.build_aliens()
        self.init_bullets()

    def build_aliens(self):
        start_y = self.screen_height//2 - INIT_Y - ALIEN_IMAGE_HEIGHT//2
        for k in range(ALIENS_WIDTH*ALIENS_DEPTH):
            alien = Turtle()
            alien.shape(ALIEN_IMAGE)
            alien.penup()
            alien_x = self.left_border + (ALIEN_IMAGE_WIDTH + ALIEN_GAP)*(k%ALIENS_WIDTH)
            alien_y = start_y - (ALIEN_IMAGE_HEIGHT + ALIEN_GAP)*(k//ALIENS_WIDTH)
            alien.goto(alien_x, alien_y)
            if k >= ALIENS_WIDTH*(ALIENS_DEPTH - 1):
                alien.pensize(SHOOTING)  # "active" (in shooting position) flag
            self.aliens.append(alien)


    def init_bullets(self):
        for _ in range(TOTAL_BULLETS):
            bullet = Turtle()  # leave it triangle
            bullet.setheading(270)
            bullet.color(BULLET_COLOR)
            bullet.penup()
            bullet.goto(0, self.screen_height + 50)  # outside the screen
            self.bullets.append(bullet)


    def check_columns(self):
        # check left
        for current_column in range(self.left_column, self.right_column + 1):
            for k in range(ALIENS_DEPTH):
                # print(f"checking column from LEFT {current_column}")
                if self.aliens[current_column + ALIENS_WIDTH*k].isvisible():
                    self.left_column = current_column
                    break
            else:
                continue
            break
        # now check right
        for current_column in range(self.right_column, self.left_column - 1, -1):
            # print(f"checking column from RIGHT {current_column}")
            for k in range(ALIENS_DEPTH):
                if self.aliens[current_column + ALIENS_WIDTH*k].isvisible():
                    self.right_column = current_column
                    return


    def move_aliens(self):
        # left_column / right_column check the upper row which will survive the longest
        if self.direction == DIRECTION_RIGHT:
            for m in range(self.right_column, len(self.aliens), ALIENS_WIDTH):
                if self.aliens[m].pos()[0] >= self.right_border:
                    self.direction = DIRECTION_LEFT
                    break
        elif self.direction == DIRECTION_LEFT:
            for m in range(self.left_column, len(self.aliens), ALIENS_WIDTH):
                if self.aliens[m].pos()[0] <= self.left_border:
                    self.direction = DIRECTION_RIGHT
                    break
        for alien in self.aliens:
            if alien.isvisible():
                alien.goto(alien.pos()[0] + STEP*self.direction, alien.pos()[1])
                if alien.pensize() == SHOOTING:
                    if randint(1, SHOOTING_PROBABILITY_BASE) < self.shooting_probability:
                        bullet = self.bullets.pop()
                        bullet.goto(alien.pos()[0], alien.pos()[1] - ALIEN_IMAGE_HEIGHT)
                        self.shooting_bullets.append(bullet)
        for bullet in self.shooting_bullets:
            bullet.forward(BULLET_SPEED)
            if bullet.pos()[1] < -self.screen_height//2:  # recycle it
                self.shooting_bullets.remove(bullet)
                self.bullets.append(bullet)

    def hit_barrier(self, barrier: Barrier):
        for bullet in self.shooting_bullets:
            if barrier.check_hit(bullet=bullet, by_defender=False):
                self.shooting_bullets.remove(bullet)
                bullet.goto(0, self.screen_height + 50)  # outside the screen
                self.bullets.append(bullet)

    def hit_by_defender(self, defender_bullet: Turtle) -> bool:
        for k in range(len(self.aliens)):
            alien = self.aliens[k]
            if not alien.isvisible():  # "transparent"
                continue
            if alien.pos()[0] - ALIEN_IMAGE_WIDTH//2 < defender_bullet.pos()[0] < alien.pos()[0] + ALIEN_IMAGE_WIDTH//2 and -6 < alien.pos()[1] - defender_bullet.pos()[1] < 4:
                alien.shape(ALIEN_SHOT_IMAGE)
                self.shot_aliens += 1
                if alien.pensize() == SHOOTING:  # was in the shooting line...
                    # print(f"Index {k} hit")
                    for m in range(k - ALIENS_WIDTH, -1, -ALIENS_WIDTH):  # ...check those behind
                        # print(f"Check if index {m} can shoot...")
                        if self.aliens[m].isvisible():  # if it's there...
                            # print("...It can")
                            self.aliens[m].pensize(SHOOTING)  # ...it can shoot now
                            break
                # sleep(HIT_SLEEP)
                self.screen.update()
                alien.hideturtle()
                self.check_columns()
                print(f"LEFT: {self.left_column}, RIGHT: {self.right_column}")
                self.shooting_probability += self.shot_aliens//SHOOTING_PROBABILITY_INCREASE_RATE
                return True
        return False


    def hit_defender_bullet(self, defender_bullet: Turtle) -> bool:
        for bullet in self.shooting_bullets:
            if bullet.pos()[0] - 8 < defender_bullet.pos()[0] < bullet.pos()[0] + 8 and -16 < bullet.pos()[1] - defender_bullet.pos()[1] < 4:
                print("HIT")
                bullet.shape(HIT_BULLET_IMAGE)
                self.shooting_bullets.remove(bullet)
                self.bullets.append(bullet)
                # sleep(HIT_SLEEP)
                self.screen.update()
                bullet.goto(0, self.screen_height + 50)  # outside the screen
                bullet.shape("classic")
                return True
        return False

    def hit_defender(self, defender):
        for bullet in self.shooting_bullets:
            if defender.pos()[0] - 25 < bullet.pos()[0] < defender.pos()[0] + 25 and 0 < bullet.pos()[1] - defender.pos()[1] < 20:
                # bullet.goto(0, self.screen_height + 50)  # outside the screen
                return True
        return False

    def reset_bullets(self):
        while len(self.shooting_bullets) > 0:
            bullet = self.shooting_bullets.pop()
            bullet.goto(0, self.screen_height + 50)  # outside the screen
            self.bullets.append(bullet)

    def check_shot_aliens(self):
        return self.shot_aliens == len(self.aliens)








