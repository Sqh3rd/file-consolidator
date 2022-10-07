# ----- General Imports -----
from os import *

# ----- test_program/auxilary.py -----

class Something:
    pass

# ----- test_program/stuff.py -----

def add(x:float, y:float):
    return x + y

def subtract(x:float, y:float):
    return x - y

# ----- test_program/main.py -----

def main():
    hub = PrimeHub()
    while True:
        hub.light_matrix.show_image('HAPPY')
        wait_for_seconds(5)
        hub.light_matrix.show_image('SAD')
        wait_for_seconds(5)