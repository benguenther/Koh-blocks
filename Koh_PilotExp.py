#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual, event
from KohBlocks import KohStimuli
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

def generate_condition_list():
    style = ["solid", "spread"]
    outline = ["black", None]
    position = [1, 2, 3]
    trial_list = []

    for s in style:
        for o in outline:
            for p in position * 2:
                trial_list.append((s,o,p))

    condition_list = []

    for trial in trial_list:
        test_pattern = {
            "name": "test", 
            "position": 0, 
            "size": scale,
            "design": "random",
            "line_color": trial[1],
            "style": trial[0]
        }
        target_pattern = {
            "name": "target", 
            "position": trial[2], 
            "size": scale,
            "design": "random",
            "line_color": trial[1],
            "style": trial[0]
        }
        positions = [1, 2, 3]
        positions.remove(trial[2])
        distractor_1 = {
            "name": "distractor_1", 
            "position": positions.pop(), 
            "size": scale,
            "design": "random",
            "line_color": trial[1],
            "style": trial[0]
        }
        distractor_2 = {
            "name": "distractor_2", 
            "position": positions.pop(), 
            "size": scale,
            "design": "random",
            "line_color": trial[1],
            "style": trial[0]
        }
        condition_list.append([test_pattern, target_pattern, distractor_1, distractor_2])
    return condition_list

trials = generate_condition_list()
random.shuffle(trials)


for trial in trials:
    screen = KohStimuli()
    screen.load_stimulus_conditions(trial, win)

    if trial[0]["style"] == "spread":
        spread_value = 10
    else:
        spread_value = 0
    
    rotation_value = random.choice([0, 1, 2, 3]) 
    
    # TODO add rotation into the trial/condition dictionary. currently randomized
    for key, value in screen.items():
        if key in ["target", "distractor_1", "distractor_2"]:
            value.spread_blocks(spread_value)
            if key == "target" and rotation_value != 0:
                value.rotate_grid(rotation_value)

        value.display_grid()
    
    print(screen.record_stimulus())

    win.flip()
    event.waitKeys()

