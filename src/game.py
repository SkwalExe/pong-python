from time import sleep
from os import get_terminal_size, system
from random import randint
from colors import *
from sys import stdout


PADDLE = f'{BG_PURPLE}  {RESET}'
BALL = f'{BG_RED}  {RESET}'
EMPTY = f'  '

size = get_terminal_size()
top_space = 2

# Divide the width by 2 to account for the fact that a block is 2 characters wide
width = int(size.columns / 2) 
height = int(size.lines) - top_space


def print_at(x, y, value):
    print(f"\033[{y + top_space};{x * 2}H{value}", end="")

class Paddle():
    def __init__(self, position, level, h):
        self.height = h
        self.position = position
        self.pos = {
            "x": 2 if position == "left" else width - 1,
            "y": int(height / 2 - self.height / 2),
        }
        self.level = level


    def go(self, dir):
        if dir == "up":
            self.pos["y"] = max(1, self.pos["y"] - 1)
        elif dir == "down":
            self.pos["y"] = min(height - self.height + 1, self.pos["y"] + 1)
        
        self.draw()

    def draw(self):
        # If the paddle is not drawn yet
        if not "_y" in self.pos:
            for i in range(self.height):
                print_at(self.pos["x"], self.pos["y"] + i, PADDLE)
        # If the paddle went up
        elif self.pos["y"] < self.pos["_y"]:
            # Erase the bottom block of the paddle
            print_at(self.pos["x"], self.pos["_y"] + self.height - 1, EMPTY)
            # Draw the top block of the paddle
            print_at(self.pos["x"], self.pos["y"], PADDLE)
        # If the paddle went down
        elif self.pos["y"] > self.pos["_y"]:
            # Erase the top block of the paddle
            print_at(self.pos["x"], self.pos["_y"], EMPTY)
            # Draw the bottom block of the paddle
            print_at(self.pos["x"], self.pos["y"] + self.height - 1, PADDLE)
        
        self.pos["_y"] = self.pos["y"]

    def automove(self, ball):
        # Just follow the y position of the ball
        if randint(0, 100) < 100 - self.level:
            return False
        if ball.pos["y"] < self.pos["y"]:
            self.go("up")
            return True
        elif ball.pos["y"] >= self.pos["y"] + self.height:
            self.go("down")
            return True


class Ball():
    def __init__(self):
        self.pos = {
            "x": int(width / 2),
            "y": int(height / 2)
        }
        self.reset()

    def update(self):
        # If the ball will hit the top or bottom of the screen
        if self.pos["y"] + self.vel["y"] < 1 or self.pos["y"] + self.vel["y"] > height:
            self.vel["y"] *= -1
        
        self.pos["x"] += self.vel["x"]
        self.pos["y"] += self.vel["y"]

        self.draw()
    
    def draw(self):
        # If the ball is not drawn yet
        if not "_y" in self.pos:
            print_at(int(self.pos["x"]), int(self.pos["y"]), BALL)
        # If the position changed
        elif self.pos["x"] != self.pos["_x"] or self.pos["y"] != self.pos["_y"]:
            # Erase the previous position
            print_at(int(self.pos["_x"]), int(self.pos["_y"]), EMPTY)
            # Draw the new position
            print_at(int(self.pos["x"]), int(self.pos["y"]), BALL)

        self.pos["_x"] = self.pos["x"]
        self.pos["_y"] = self.pos["y"]

    def reset(self):
        self.pos["x"] = int(width / 2)
        self.pos["y"] = int(height / 2)

        self.vel = {
            "x": -1 if randint(0, 1) == 0 else 1,
            "y":  randint(-1000, 1000)/1000
        }



class Game():
    def __init__(self, ai_level, winning_score, left_ai, right_ai, ph, random_yvel):
        # Clear terminal
        print("\x1b[1;1H\x1b[2J", end="")

        self.STATES = {
            "MAIN": 0,
            "PLAYING": 1,
            "GAME_OVER": 2
        }
        self.state = self.STATES["MAIN"]

        self.lpad = Paddle("left", ai_level, ph)
        self.rpad = Paddle("right", ai_level, ph)

        self.lpad.draw()
        self.rpad.draw()

        self.lscore = 0
        self.rscore = 0

        self.ball = Ball()

        self.winning_score = winning_score
        self.winner = None

        self.left_ai = left_ai
        self.right_ai = right_ai

        self.random_yvel = random_yvel

    def draw(self):
        score_left = f"Player1 : {self.lscore}"
        score_right = f"Player2 : {self.rscore}"
        print_at(1, -2, score_left)
        print_at(width - int(len(score_right) / 2), -2, score_right)
        stdout.flush()
        
    

    def update(self):
        self.ball.update()

        # check if the ball hits behind the paddles
        if self.ball.pos["x"] <= 1:
            self.rscore += 1
            self.ball.reset()
            sleep(1)
        elif self.ball.pos["x"] >= width:
            self.lscore += 1
            self.ball.reset()
            sleep(1)

        # Check if the game is over
        if self.lscore == self.winning_score or self.rscore == self.winning_score:
            self.state = self.STATES["GAME_OVER"]
            self.winner = "Player1" if self.lscore == self.winning_score else "Player2" 

        while self.left_ai:
            if not self.lpad.automove(self.ball):
                break

        while self.right_ai:
            if not self.rpad.automove(self.ball):
                break

        # Check if the ball hits a paddle
        if (self.ball.pos["x"] == self.lpad.pos["x"] + 1 and self.ball.pos["y"] >= self.lpad.pos["y"] and self.ball.pos["y"] < self.lpad.pos["y"] + self.lpad.height) or \
            (self.ball.pos["x"] == self.rpad.pos["x"] - 1 and self.ball.pos["y"] >= self.rpad.pos["y"] and self.ball.pos["y"] < self.rpad.pos["y"] + self.rpad.height):
            self.ball.vel["x"] *= -1
            if self.random_yvel:
                self.ball.vel["y"] = randint(-1000, 1000)/1000                

        self.draw()
        return
    
