import curses
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cli import input_bar, initialize_screen
from setup import create_config_file


def main(stdscr=None):
    if stdscr is None:
        return curses.wrapper(main)

    create_config_file()
    initialize_screen(stdscr)
    input_received = input_bar()
    while input_received != "/exit":
        input_received = input_bar()
    


if __name__ == "__main__":
    curses.wrapper(main)