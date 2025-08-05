#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual, event, gui, clock
from KohBlocks import KohExperiment
import sys, os, math, time

# if/else block to simplify testing/development by hardcoding experiment parameters
if True:
    subj_id = "0001"
    condition = "test"
    win = visual.Window(
        monitor="hp_home_main",
        fullscr=True,
        size=[1920, 1080],
        screen=0,
        color=[.5] * 3,
        units="pix"
    )
    data_path = f"KohBlocks_{subj_id}_test.csv"
else:
    # setup a gui interface to specify experiment parameters
    exp_param = gui.Dlg()
    exp_param.addField("id: ")
    exp_param.addField("condition: ", choices=["near", "far"])

    # log and display the gui for user input
    param_data = exp_param.show()

    # assign subject id variable and condition number based on gui input
    subj_id = param_data["id: "]
    condition = param_data["condition: "]
    data_path = f"KohBlocks_{subj_id}.csv"

        # define the stimulus presentation window
    if condition == "near":
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

# empty list to hold data
exp_data = []

# add header to data if this is the first condition/block of trials
if not os.path.exists(data_path):
    # define the column headings for the data file
    data_header = [
        "ID", # subject ID
        "condition",  # record the condition
        "trial",  # Counter for the Trial Number
        "target_location", # int 1-3 defining target position 1: left, 2: center, 3: right
        "target_rotation", # int 0-3 defomomg target rotation (clockwise) 0: 0deg, 1: 90deg, 2: 180deg, 3: 270deg
        "response",
        "accuarcy"
        "rt", 
    ]
    # attach headings to the data
    exp_data.append(data_header)

# helper function for setting text size
def visual_angle(deg, cond = condition):
    if cond == "test":
        screen_pix = [1920, 1080]
        screen_mm = [529, 297]
        distance = 1000
    elif cond == "far":
        screen_pix = [3840, 2160]
        screen_mm = [1805, 1015]
        distance = 5385 
    elif cond == "near":
        screen_pix = [3840, 2160]
        screen_mm = [597, 335] 
        distance = 400
    
    # assumes that pixels are square
    pix_mm = (screen_pix[0]/screen_mm[0])
    pix = (2 * distance) * math.tan((deg * (math.pi/180))/2) * pix_mm
    return round(pix)

####################################
###### set up data collection ######
####################################

response_box_1 = visual.Rect(
    win = win,
    units = "pix",
    size = visual_angle(3.1),
    fillColor = [1] * 3,
    opacity = 0.0,
    pos = (-300, -150)
)

response_box_2 = visual.Rect(
    win = win,
    units = "pix",
    size = visual_angle(3.1),
    fillColor = [1] * 3,
    opacity = 0.0,
    pos = (0, -150)
)

response_box_3 = visual.Rect(
    win = win,
    units = "pix",
    size = visual_angle(3.1),
    fillColor = [1] * 3,
    opacity = 0.0,
    pos = (300, -150)
)

response_boxes = [response_box_1, response_box_2, response_box_3]

mouse = event.Mouse(
    win = win,
    visible = True,   
)
mouse.clickableStim = response_boxes

def collect_mouse_response(locations = response_boxes):
    for box in locations:
        box.draw()
    win.flip()
    clicked = False
    start_time = clock.getTime()
    while not clicked:
        # check the list of shapes
        for n, box in enumerate(locations):
            if mouse.isPressedIn(box):
                clicked = True
                response = (n + 1) 
                end_time = clock.getTime()
                break # exit this loop
            else: # this runs once at the completion of the for loop
            # breathe for 1 ms
                time.sleep(0.001)
    rt = round((end_time - start_time) * 1000)
    return (response, rt)



##########################
###### Instructions ######
##########################
instructions = visual.TextStim(
    win = win,
    alignText = "center",
    anchorHoriz = "center",
    anchorVert = "center",
    font = "courier new",
    color = [-1] * 3,
    units = "pix",
    height = visual_angle(0.5),
    wrapWidth = visual_angle(18)
)



##########################
#### Practice Trial #####
##########################
instructions.text = """
practice trial:  start
"""
instructions.draw()
win.flip()
event.waitKeys()

practice = KohExperiment(1.5, condition, win)
practice_trial = next(iter(practice))
for key, value in practice[practice_trial].items():
    value.display_grid()
win.flip()
event.waitKeys()


##########################
##### Run Experiment #####
##########################
instructions.text = """
experimental trials: start
"""
instructions.draw()
win.flip()
event.waitKeys()

 # number is the stimulus size in degrees
test = KohExperiment(1.5, condition, win)
for key, value in test.items():
    for x, y in value.items():
        y.display_grid()
    print(f"{key}: {value.record_stimulus()}")
    response = collect_mouse_response()
    

##########################
### Final Data Logging ###
##########################
# check to see if initial datafile exists and open to write or append mode
"""
if os.path.exists(data_path):
    data_file = open(data_path, "a")
else:
    data_file = open(data_path, 'w')

for item in exp_data:
    print(*item, sep = ',', file = data_file)
data_file.close()
"""