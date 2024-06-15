from turtle import Turtle

STYLE = ('Courier', 16, 'bold')
ALIGN = "center"

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()


    def ship_lost(self):
        self.clear()
        self.color("red")
        self.write("Ship lost!", font=STYLE, align=ALIGN)

    def final_score(self, ships_lost: int):
        self.clear()
        self.color("orange")
        self.write(f"Game over, ships lost: {ships_lost}", font=STYLE, align=ALIGN)



