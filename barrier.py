from turtle import Turtle

SIZE = 6
GAP = 2
STAMP_SIZE = 20
BLOCK_SIZE = 10
BARRIER_Y = -200
COLOR = "bisque"

class Barrier:

    def __init__(self, screen_width: int):
        self.blocks = []
        self.removed_blocks = []  # to reuse on game restart
        for m in range(-5, 5):  # int(screen_width/(SIZE + GAP)/(STAMP_SIZE*STAMP_BASE))):
            self.build_barrier(m*80)


    def build_barrier(self, init_x):
        for k in range(SIZE):
            for m in range(-1, 2):
                block = Turtle("square")
                block.color(COLOR)
                block.shapesize(BLOCK_SIZE / STAMP_SIZE, BLOCK_SIZE / STAMP_SIZE)
                block.penup()
                block.goto(init_x + GAP * BLOCK_SIZE // 2 + BLOCK_SIZE * k, BARRIER_Y + BLOCK_SIZE * m)
                self.blocks.append(block)
        for k in range(1, SIZE - 1):
            for m in (-2, 2):
                block = Turtle("square")
                block.color(COLOR)
                block.shapesize(BLOCK_SIZE / STAMP_SIZE, BLOCK_SIZE / STAMP_SIZE)
                block.penup()
                block.goto(init_x + GAP * BLOCK_SIZE // 2 + BLOCK_SIZE * k, BARRIER_Y + BLOCK_SIZE * m)
                self.blocks.append(block)
        for k in range(2, SIZE - 2):
            for m in (-3, 3):
                block = Turtle("square")
                block.color(COLOR)
                block.shapesize(BLOCK_SIZE / STAMP_SIZE, BLOCK_SIZE / STAMP_SIZE)
                block.penup()
                block.goto(init_x + GAP * BLOCK_SIZE // 2 + BLOCK_SIZE * k, BARRIER_Y + BLOCK_SIZE * m)
                self.blocks.append(block)

    def check_hit(self, bullet: Turtle, by_defender: bool) -> bool:
        for block in self.blocks:
            vertical_gap = bullet.pos()[1] - block.pos()[1]
            if by_defender:
                vertical_gap = -vertical_gap
            vertical_gap += 3
            if block.pos()[0] - BLOCK_SIZE/2 - 3 <= bullet.pos()[0] <= block.pos()[0] + BLOCK_SIZE/2 and vertical_gap < BLOCK_SIZE:
                    self.blocks.remove(block)
                    block.goto(0, 1000)  # outside the screen
                    self.removed_blocks.append(block)
                    return True
        return False

