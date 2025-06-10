#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual, event
from KohBlocks import KohBlock
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


scale = visual_angle(1)

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
    
    # TODO integrate this into the position function
    def spread_blocks(pos: list, adjust: int):
        spreader = [
            [(-adjust), (adjust)], # cube 1
            [(0), (adjust)], # cube 2
            [(adjust), (adjust)], # cube 3
            [(-adjust), (0)], # cube 4
            [(0), (0)], # cube 5
            [(adjust), (0)], # cube 6
            [(-adjust), (-adjust)], # cube 7
            [(-0), (-adjust)], # cube 8
            [(adjust), (-adjust)], # cube 9
        ]   
        return [[a+b for a, b in zip(*l)] for l in zip(pos, spreader)]



    def block_design(data):
        if data == "random":
            design = [random.randint(1,6) for _ in range(9)]
        elif data == "fixed":
            design = [4,5,6,2,2,2,3,3,3] # need to specify where it will be coming from
        return design


    blocks = block_design(type)
    shape_matrix = []

    type = "spread"

    for row in range(1):
        row_list = []
        # TODO   integrate this into the position functioon
        if type == "connected":
            stim_positions = position_grid(x,y)
        elif type == "spread":
            stim_positions = spread_blocks(position_grid(x,y), 20)
        
        for var, x in zip(stim_positions, blocks): # for col, var, x in zip(range(9), stim_positions, blocks): -- old version that worked but col not used.
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