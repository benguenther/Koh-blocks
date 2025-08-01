#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual, event
from KohBlocks import KohGrid
import math, random, sys


condition = "test"

# define the stimulus presentation window
if condition == "test":
    win = visual.Window(
        monitor="hp_home_main", #"hp_home_main", #"surface", #"testMonitor",  # "BlackLaptop",,
        fullscr=True,
        size=[1920, 1080],  # [1920, 1080],# [1280, 1024], #[2736, 1824], #[1600, 900],
        screen=0,
        color=[.5] * 3,
        units="pix"
    )
elif condition == "near":
    win = visual.Window(
        monitor="LG",
        fullscr=True,
        size=[3840, 2160],
        screen=1,
        color=[+1] * 3,
        units="pix"
    )
elif condition == "far":
    win = visual.Window(
        monitor="BigTV",
        fullscr=True,
        size=[3840, 2160],
        screen=1,
        color=[.5] * 3,
        units="pix"
    )
else:
    sys.exit("error in condition settings")


# function to convert stimulus dimensions from visual angle to pixels
def visual_angle(deg, cond = condition):
    if cond == "test":
        screen_pix = [1920, 1080]
        screen_mm = [529, 297]
        distance = 610
    elif cond == "far":
        screen_pix = [3840, 2160]
        screen_mm = [1805, 1015]
        distance = 5385
    elif cond == "near":
        screen_pix = [3840, 2160]
        screen_mm = [597, 335] 
        distance = 400  
    # assumes pixels are squaare
    pix_mm = (screen_pix[0]/screen_mm[0])
    pix = (2 * distance) * math.tan((deg * (math.pi/180))/2) * pix_mm
    # returns the number of pixels producing an object of the entered visual angle
    return round(pix)


scale = visual_angle(1.5)
print(scale)

for e in range(2):
    stim = KohGrid(0,0, scale, win, "random")
    target = stim.log_design()  
    stim2 = KohGrid(300,300, scale, win, "random")
    stim3 = KohGrid(300, 0, scale, win, pat = target)
    stim4 = KohGrid(300, -300, scale, win, "random")
    stim2.spread_blocks(20)
    stim3.spread_blocks(20)
    stim4.spread_blocks(20)
    stim3.rotate_grid(1)
    stim2.display_grid()
    stim3.display_grid()
    stim4.display_grid()
    stim.display_grid()
    win.flip()
    event.waitKeys()

"""
consider handling position of the target by moving the h/v coordinates into a tuple.  
list of tuples randomized and then iterated through to determine stim location
"""
    
    


