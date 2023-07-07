#!/usr/bin/env python3

import pynput
from os import system
from time import sleep
from game import *
import cursor
from sys import argv

# Prevent user input from being displayed on the terminal
def hide_stdin():
    system("stty -echo")
    cursor.hide()

# Allow user input to be displayed on the terminal
def show_stdin():
    system("stty echo")
    cursor.show()

VERSION = "0.1.0"

def main():
    speed = 20
    winning_score = 10
    paddle = "left"
    ai_level = 70
    paddle_height = 7
    sensibility = 2
    random_yvel = True
    


    argv.pop(0)
    while len(argv) > 0:
        arg = argv.pop(0)
        match arg:
            case "-h" | "--help":
                bar = f"{PURPLE}━━━━━━━━━━━━━━━━━{RESET}"
                print()
                print(f"{BG_PURPLE} Pong Python {RESET}")
                print(bar)
                print(f"Author: {PURPLE}SkwalExe <Leopold Koprivnik>{RESET}")
                print(f"Github: {PURPLE}https://github.com/SkwalExe{RESET}")
                print(bar)
                print(f"A simple pong game written in Python.")
                print(bar)
                print(f"Options:")
                print(f"\t{PURPLE}-h, --help : {YELLOW}Show this help message and exit")
                print(f"\t{PURPLE}-v, --version : {YELLOW}Show the version number and exit")
                print(f"\t{PURPLE}-s, --speed : {YELLOW}Set the speed of the game from 1 to 100 (default: {speed})")
                print(f"\t{PURPLE}-w, --winning-score : {YELLOW}Set the winning score of the game (default: 10), no end if set to -1")
                print(f"\t{PURPLE}-p, --play-as : {YELLOW}left|right -> Play as the [left] or [right] paddle (default: left)")
                print(f"\t{PURPLE}-a, --ai-only : {YELLOW}Make the two paddles play against each other (default: false), overwrites -p")
                print(f"\t{PURPLE}-l, --ai-level : {YELLOW}The level of the AI (default: {ai_level}), 100 is invincible")
                print(f"\t{PURPLE}-ph, --paddle-height : {YELLOW}Set the height of the paddles (default: 5)")
                print(f"\t{PURPLE}-n, --sensibility : {YELLOW}Set the sensibility of the user controlled paddle (default: {sensibility})")
                print(f"\t{PURPLE}-r, --random-yvel : {YELLOW}true|false -> Set the y velocity of the ball to a random value when it hits a paddle (default: true)")
                print(f"\t{PURPLE}-c, --cursor : {YELLOW}If you left the game with Ctrl+C (you should use ESC instead), this option will show make the cursor visible again and exit")
                print(bar)
                print(f"Controls:")
                print(f"\t{PURPLE}Up Arrow : {YELLOW}Move the left paddle up")
                print(f"\t{PURPLE}Down Arrow : {YELLOW}Move the left paddle down")
                print(f"\t{PURPLE}Esc : {YELLOW}Quit the game")
                print(f"\t{PURPLE}Space : {YELLOW}Pause the game")
                print(bar)
                print(f"Additional information:")
                print(f"\t{PURPLE}If you want to keep your cursor and stdin visible after the game, exit with ESC instead of Ctrl+C (also, see -c option){RESET}")
                print(f"\t{PURPLE}If you encounter any bugs, please report them on the Github repository or at koprivnik@skwal.net{RESET}")
                print()
                
                quit(0)

            case "-v" | "--version":
                print(f"{BG_PURPLE} Pong Python {RESET}")
                print(f"Version: {PURPLE}{VERSION}{RESET}")
                quit(0)

            case "-s" | "--speed":
                if len(argv) == 0:
                    print(f"{RED}Error: {YELLOW}Missing speed value{RESET}")
                    quit(1)
                try:
                    speed = int(argv.pop(0))
                except:
                    print(f"{RED}Error: {YELLOW}Invalid speed value{RESET}")
                    quit(1)
                if speed < 1 or speed > 100:
                    print(f"{RED}Error: {YELLOW}Speed must be between 1 and 100{RESET}")
                    quit(1)

            case "-w" | "--winning-score":
                if len(argv) == 0:
                    print(f"{RED}Error: {YELLOW}Missing winning score value{RESET}")
                    quit(1)
                try:
                    winning_score = int(argv.pop(0))
                except:
                    print(f"{RED}Error: {YELLOW}Invalid winning score value{RESET}")
                    quit(1)

            case "-p" | "--play-as":
                if len(argv) == 0:
                    print(f"{RED}Error: {YELLOW}Missing paddle value{RESET}")
                    quit(1)
                paddle = argv.pop(0)
                if not paddle in ["left", "right"]:
                    print(f"{RED}Error: {YELLOW}Invalid paddle value, must be 'left' or 'right'{RESET}")
                    quit(1)
                
            case "-a" | "--ai-only":
                paddle = None

            case "-ph" | "--paddle-height":
                if len(argv) == 0:
                    print(f"{RED}Error: {YELLOW}Missing paddle height value{RESET}")
                    quit(1)
                try:
                    paddle_height = int(argv.pop(0))
                except:
                    print(f"{RED}Error: {YELLOW}Invalid paddle height value{RESET}")
                    quit(1)
                if paddle_height < 1 or paddle_height > height - 3:
                    print(f"{RED}Error: {YELLOW}Paddle height must be greater than 0 and not bigger than the terminal{RESET}")
                    quit(1)
            case "-l" | "--ai-level":
                if len(argv) == 0:
                    print(f"{RED}Error: {YELLOW}Missing AI level value{RESET}")
                    quit(1)
                try:
                    ai_level = int(argv.pop(0))
                except:
                    print(f"{RED}Error: {YELLOW}Invalid AI level value{RESET}")
                    quit(1)
                if ai_level < 0 or ai_level > 100:
                    print(f"{RED}Error: {YELLOW}AI level must be between 0 and 100{RESET}")
                    quit(1)
            case "-n" | "--sensibility":
                if len(argv) == 0:
                    print(f"{RED}Error: {YELLOW}Missing sensibility value{RESET}")
                    quit(1)
                try:
                    sensibility = int(argv.pop(0))
                except:
                    print(f"{RED}Error: {YELLOW}Invalid sensibility value{RESET}")
                    quit(1)
                if sensibility < 1:
                    print(f"{RED}Error: {YELLOW}Sensibility must be greater than 0{RESET}")
                    quit(1)
            case "-r" | "--random-yvel":
                if len(argv) == 0:
                    print(f"{RED}Error: {YELLOW}Missing random y velocity value{RESET}")
                    quit(1)
                random_yvel = argv.pop(0)
                if not random_yvel in ["true", "false"]:
                    print(f"{RED}Error: {YELLOW}Invalid random y velocity value, must be 'true' or 'false'{RESET}")
                    quit(1)
                random_yvel = random_yvel == "true"
            case "-c" | "--cursor":
                show_stdin()
                quit(0)
            case _:
                print(f"{RED}Error: {YELLOW}Unknown argument : {PURPLE}{arg}{RESET}")
                quit(1)


    hide_stdin()
    paused = False
    game = Game(ai_level, winning_score, not paddle == "left", not paddle == "right", paddle_height, random_yvel)
    def on_press(key):
        if key == pynput.keyboard.Key.up:
            for _ in range(sensibility):
                if paddle == "left":
                    game.lpad.go("up")
                elif paddle == "right":
                    game.rpad.go("up")
        elif key == pynput.keyboard.Key.down:
            for _ in range(sensibility):
                if paddle == "left":
                    game.lpad.go("down")
                elif paddle == "right":
                    game.rpad.go("down")
        elif key == pynput.keyboard.Key.esc:
            game.state = game.STATES["GAME_OVER"]
        elif key == pynput.keyboard.Key.space:
            nonlocal paused
            paused = not paused
            print_at(int(width / 2) - 1, int(height / 2), "Paused" if paused else "      ")
            stdout.flush()
            


    timeout = 1 / speed


    with pynput.keyboard.Listener(on_press=on_press) as listener:
        while not game.state == game.STATES["GAME_OVER"]:
            if not paused:
                game.update()
            sleep(timeout)
        print_at(0, height + 1, "Game Over!\n")
        if game.winner is not None:
            print(f"{game.winner} won the game!\n")
        show_stdin()

if __name__ == "__main__":
    main()