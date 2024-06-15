from turtle import Screen
from aliens import Aliens
from barrier import Barrier
from defender import Defender
from scoreboard import Scoreboard

from time import sleep

WIDTH = 800
HEIGHT = 800
SLEEP = 0.01
PAUSE = 2
BACKGROUND_COLOR = "black"

ships_lost = 0

game_on = True

screen = Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor(BACKGROUND_COLOR)
screen.title("Space Invaders")
screen.tracer(0)

aliens = Aliens(screen_width=WIDTH, screen_height=HEIGHT, background=BACKGROUND_COLOR, screen=screen)
barrier = Barrier(screen_width=WIDTH)
defender = Defender(screen_height=HEIGHT, screen=screen)
scoreboard = Scoreboard()

screen.update()

screen.listen()
screen.onkey(defender.move_right, "Right")
screen.onkey(defender.move_left, "Left")
screen.onkey(defender.shoot, " ")


def show_final_score():
    aliens.reset_bullets()  # clean the screen
    scoreboard.final_score(ships_lost=ships_lost)


while game_on:
    sleep(SLEEP)
    aliens.move_aliens()
    aliens.hit_barrier(barrier)
    defender.bullet_flies()
    defender.hit_barrier(barrier)
    if aliens.hit_by_defender(defender_bullet=defender.bullet):
        defender.reset_bullet()
        if aliens.check_shot_aliens():
            show_final_score()
            game_on = False
    elif aliens.hit_defender_bullet(defender_bullet=defender.bullet):
        defender.reset_bullet()
    elif aliens.hit_defender(defender=defender):
        aliens.reset_bullets()
        scoreboard.ship_lost()
        defender.hit()
        scoreboard.clear()
        ships_lost += 1
        screen.title(f"Space Invaders - ships lost: {ships_lost}")

    screen.update()

screen.exitonclick()
