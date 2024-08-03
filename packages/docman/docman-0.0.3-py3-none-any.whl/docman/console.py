import os

clear = lambda: os.system('clear')
red = '\x1b[1;31m'
black = '\x1b[0m'
green = '\x1b[1;32m'
yellow = '\x1b[1;33m'
blue = '\x1b[1;34m'
purple = '\x1b[1;35m'
cyan = '\x1b[1;36m'
white = '\x1b[1;37m'


def press_enter_to_continue():
    input(f'\n{yellow}Press ENTER to continue{black}')
