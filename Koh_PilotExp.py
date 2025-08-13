#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual, event, gui, clock
from KohBlocks import KohExperiment, KohPatternLogs
import sys, os, math, time, csv

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
        "spread", # True or False
        "response",
        "accuracy"
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
    pos = (-visual_angle(4.0), -visual_angle(2.0))
)

response_box_2 = visual.Rect(
    win = win,
    units = "pix",
    size = visual_angle(3.1),
    fillColor = [1] * 3,
    opacity = 0.0,
    pos = (0, -visual_angle(2.0))
)

response_box_3 = visual.Rect(
    win = win,
    units = "pix",
    size = visual_angle(3.1),
    fillColor = [1] * 3,
    opacity = 0.0,
    pos = (visual_angle(4.0), -visual_angle(2.0))
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


def record_test_pattern(pattern, record: dict):
    if pattern not in record.values():
        record[len(record) + 1] = pattern
    
    for key, value in record.items():
        if value == pattern:
            return key

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

# class for tracking the test/target Koh patterns
# loads a dict and methods for tracking current and past test/target patterns
koh_block_patterns = KohPatternLogs()

# class object that loads the experimetn and corresponding conditions
# number is the size in degrees
test = KohExperiment(1.5, condition, win)

for key, value in test.items():
    # add the used test pattern to the log and return the int key value for that pattern in the log
    test_pattern = koh_block_patterns.add_pattern_to_log(value._stimuli["test"])

    # value is for a KohStimuli object which contains a dictionary the 4 Koh patterns displayed
    # Each pattern is a KohGrid object.  Keys: "test", "target", "distractor_1", "distractor_2"
    for x, y in value.items():
        y.display_grid()
    #print(f"{key}: {value.record_stimulus()}")
    
    # call exp function to collect a mouse response.  returns int (1-3) for object selected and trial rt
    response = collect_mouse_response()
    # compare mouse click to correct target position to log accuracy.  Correct == 1, incorrect == 0
    resp_acc = 1 if response[0] == value._stimuli["target"].log_position() else 0
    
    # list of data to be recorded for each trial
    trial_data = [
        subj_id, # subject ID
        condition, # record the condition
        int(key.split()[1]), # Counter for the Trial Number
        value._stimuli["target"].log_position(), # int 1-3 defining target position 1: left, 2: center, 3: right
        value._stimuli["target"].log_rotation(), # int 0-3 defomomg target rotation (clockwise) 0: 0deg, 1: 90deg, 2: 180deg, 3: 270deg
        value._stimuli["target"].log_spread(), # True or False
        response[0], #response",
        resp_acc, #accuracy"
        response[1], #rt", 
        test_pattern # number (key) linking to a dict of the specific pattern used
        # outline, True or False
    ]

    # add trials data to the overall experiment datafile    
    exp_data.append(trial_data)


##########################
### Final Data Logging ###
##########################

# save the current list of used Koh test patterns.
# this overwrites the old list
koh_block_patterns.save_pattern_data()    

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