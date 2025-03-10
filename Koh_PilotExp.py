#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual, event
from KohBlocks import KohBlock
import math, random, sys


condition = "far"

# define the stimulus presentation window
if condition == "test":
    win = visual.Window(
        monitor="hp_home_main", #"surface", #"testMonitor",  # "BlackLaptop",,
        fullscr=True,
        size=[1920, 1080],  # [1920, 1080],# [1280, 1024], #[2736, 1824], #[1600, 900],
        screen=0,
        color=[+1] * 3,
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
        color=[+1] * 3,
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


scale = visual_angle(2)

# function to present the KohBlock Pattern
def present_Koh_Blocks(x, y, type, scale = scale):
    def position_grid(h_center, v_center, scale = scale):
        positions = [
                [(h_center - scale), (v_center + scale)], # cube 1
                [(h_center),(v_center + scale)], # cube 2
                [(h_center + scale),(v_center + scale)], # cube 3
                [(h_center - scale),(v_center)], # cube 4
                [(h_center),(v_center)], # cube 5
                [(h_center + scale),(v_center)], # cube 6
                [(h_center - scale),(v_center - scale)], # cube 7
                [(h_center),(v_center - scale)], # cube 8
                [(h_center + scale),(v_center - scale)] # cube 9
            ]
        return positions


    def block_design(data):
        if data == "random":
            design = [random.randint(1,6) for _ in range(9)]
        elif data == "fixed":
            design = [1,2,3,3,3,3,5,4,1] # need to specify where it will be coming from
        return design


    blocks = block_design(type)
    shape_matrix = []

    for row in range(1):
        row_list = []
        for col, var, x in zip(range(9), position_grid(x,y), blocks):
            block = KohBlock(
                win = win,
                line = "black",
                scale = scale,
                pos = (var[0], var[1]),
                shape = x
            )       
            row_list.append(block)
        shape_matrix.append(row_list)

    for row in shape_matrix:
        for stim in row:
            stim.draw()


for e in range(25):
    present_Koh_Blocks(random.randint(-200,200), random.randint(-200,200), "random")
    win.flip()
    event.waitKeys()