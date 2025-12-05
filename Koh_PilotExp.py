#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual, event, gui
from KohBlocks import KohExperiment, KohPatternLogs, ExperimentData, MouseResponse
from Survey.survey_data import SurveyData
import sys, math

# if/else block to simplify testing/development by hardcoding experiment parameters
if True:
    subj_id = "99999"
    condition = "test"
    vis_acuity = "0.05"
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
    exp_param = gui.Dlg(title = "Experiment Information")
    exp_param.addField("id: ", "id:")
    exp_param.addField("LogMAR: ", "LogMAR")
    exp_param.addField("condition: ", choices=["near", "far"])

    # log and display the gui for user input
    param_data = exp_param.show()

    # assign subject id variable and condition number based on gui input
    subj_id = param_data["id: "]
    vis_acuity = param_data["LogMAR: "]
    condition = param_data["condition: "]
    data_path = f"KohBlocks_{subj_id}.csv"

        # define the stimulus presentation window
    if condition == "near":
        win = visual.Window(
            monitor="LG",
            fullscr=True,
            size=[3840, 2160],
            screen=1,
            color=[.5] * 3,
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

# helper function for setting text size
# TODO add to an experiment helper class/file yet to be defined
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
#### Practice Trials #####
##########################

instructions.text = """
Welcome to the Experiment \n
\n
Press any key to begin the practice trials
"""
instructions.draw()
win.flip()
event.waitKeys()

instructions.text = "+"

practice_trials = KohExperiment(1.25, condition, win, "practice", 3)
practice_responses = MouseResponse(1.25, condition, win, 3)
for key, value in practice_trials.items():
    instructions.draw()
    win.flip()
    event.waitKeys()

    for practice_n, trial_n in value.items():
        trial_n.display_grid()
    # not assigned to a variable because not logging the data
    practice_responses.collect_mouse_response()

instructions.text = """
Do you have any questions before we continue? \n
\n
Press any key to continue
"""
instructions.draw()
win.flip()
event.waitKeys()


##########################
##### Run Experiment #####
##########################

instructions.text = f"""
The {condition} condition consists of 28 trials. \n
\n
Press any key to begin
"""
instructions.draw()
win.flip()
event.waitKeys()

# class for tracking the test/target Koh patterns
# loads a dict and methods for tracking current and past test/target patterns
koh_block_patterns = KohPatternLogs()

# Object for managing the experiment and trial data
exp_data = ExperimentData(data_path)

exp_data.load_data_header(
    "Subject ID",
    "visual acuity",
    "Condition",
    "Trial Number",
    "Target Position",
    "Target Rotation",
    "Target Spread",
    "trial type",
    "Outline",
    "Response",
    "Response Accuracy",
    "RT",
    "KohPattern Number",
    # survey variables
    "sex", 
    "gender",
    "age",
    "english", # is enlish your first language
    "self_handedness",
    "survey_handedness"
)
exp_data.check_for_existing_data()

# load survey data
survey = SurveyData(subj_id)

# class object that loads the experimetn and corresponding conditions
# number is the size in degrees
main_experiment = KohExperiment(1.25, condition, win, "experiment", 3)
main_exp_responses = MouseResponse(1.25, condition, win, 3)

instructions.text = "+"

for key, value in main_experiment.items():
    instructions.draw()
    win.flip()
    event.waitKeys()

    # add the used test pattern to the log and return the int key value for that pattern in the log
    test_pattern = koh_block_patterns.add_pattern_to_log(value._stimuli["test"])

    # value is for a KohStimuli object which contains a dictionary the 4 Koh patterns displayed
    # Each pattern is a KohGrid object.  Keys: "test", "target", "distractor_1", "distractor_2"
    for x, y in value.items():
        y.display_grid()
    
    # call exp function to collect a mouse response.  returns int (1-3) for object selected and trial rt
    response = main_exp_responses.collect_mouse_response()
    
    # variable to identify correct response.  If it is a catch trial, the correct response is 0
    # if it is a "target" trial then the correct response is the logged target location.
    # note there is always a logged target location.  Catch trials are managed by the trial_type variable
    # when a trial is listed as "catch", the pattern at the target location is not set to match the test
    correct_response = 0 if value.log_trial_type() == "catch" else value._stimuli["target"].log_position()
   
    # compare mouse click to correct target position to log accuracy.  Correct == 1, incorrect == 0
    resp_acc = 1 if response[0] == correct_response else 0
    
    # log trial data using the ExperimentData object
    exp_data.add_trial_data(
        subj_id, # subject ID
        vis_acuity, # LogMar score
        condition, # record the condition
        int(key.split()[1]), # Counter for the Trial Number
        value._stimuli["target"].log_position(), # int 1-3 defining target position 1: left, 2: center, 3: right
        value._stimuli["target"].log_rotation(), # int 0-3 defining target rotation (clockwise) 0: 0deg, 1: 90deg, 2: 180deg, 3: 270deg
        value._stimuli["target"].log_spread(), # True or False
        value._stimuli["target"].log_outline(), # outline, True or False
        value.log_trial_type(), # "target" or "catch"
        response[0], #response",
        resp_acc, #accuracy"
        response[1], #rt", 
        test_pattern, # number (key) linking to a dict of the specific pattern used
        # survey variables
        survey.data["sex"], # sex assigned at birth
        survey.data["gen"], # self report gender
        survey.data["age"], # age
        survey.data["english"], # Y/N if english is first language
        survey.data["handedness"], # self report handedness R/L
        survey.data["calc_hand"],  # handedness based on scale inventory
        )


instructions.text = f"""
The {condition} condtion has successfully been completed.
\n
Thank you for your participation.
"""
instructions.draw()
win.flip()
event.waitKeys()

##########################
### Final Data Logging ###
##########################

koh_block_patterns.save_pattern_data() 
exp_data.save_data()   