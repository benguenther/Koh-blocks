#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual, clock, event
import random, math, csv, os, time
import numpy as np

class KohBlock:
    
    def __init__(self, win, scale, line, pos, shape: int):
        self.shape = shape
        self.triangle1 = visual.ShapeStim(
            win = win,
            units = "pix",
            vertices = (
                ((-1*(scale/2)), (-1*(scale/2))), 
                ((scale/2), (-1*(scale/2))), 
                ((-1*(scale/2)), (scale/2))
            ),
            pos = pos,
            fillColor = "red",
            lineColor = line,
        )
        self.triangle2 = visual.ShapeStim(
            win = win,
            units = "pix",
            vertices = (
                ((scale/2), (scale/2)), 
                ((-1*(scale/2)), (scale/2)), 
                ((scale/2), (-1*(scale/2)))
            ),
            pos = pos,
            fillColor = "white",
            lineColor = line,
        )
        self.square = visual.ShapeStim(
            win = win,
            units = "pix",
            vertices = (
                ((-1*(scale/2)),(-1*(scale/2))),
                ((-1*(scale/2)), (scale/2)),
                ((scale/2), (scale/2)), 
                ((scale/2), (-1*(scale/2)))  
            ),
            pos = pos,
            lineColor = line,
        )
    

    def draw(self):
        if self.shape in [1, 2, 3, 4]:
            if self.shape == 1:
                self.triangle1.ori = 0
                self.triangle2.ori = 0
            elif self.shape == 2:
                self.triangle1.ori = 90
                self.triangle2.ori = 90
            elif self.shape == 3:
                self.triangle1.ori = 180
                self.triangle2.ori = 180
            elif self.shape == 4:
                self.triangle1.ori = 270
                self.triangle2.ori = 270
            self.triangle1.draw()
            self.triangle2.draw()    
        elif self.shape == 5:
            self.square.fillColor = "red"
            self.square.draw()
        elif self.shape == 6:
            self.square.fillColor = "white"
            self.square.draw()

    
    def __repr__(self):
        return f"KohBlock({self.win}, {self.scale}, {self.line}, {self.pos}, {self.shape})"


class KohGrid:
    
    def __init__(self, position: tuple, scale: int,  win, block_type = "", pat = None, line_color = "black", num_blocks = 3):#spread: int, 
        self.h_center = position[0]#h_center
        self.v_center = position[1]#v_center
        self.pos_number = position[2]
        self.num_blocks = num_blocks
        self.scale = scale
        self.block_type = block_type # specifies if blocks are random or fixed
        self.win = win
        self.line_color = line_color
        self.__rotation = 0
        
        self.positions = self.position_grid()
        self.original_positions = self.positions # save the original just in case

        if pat is None:
            self.pattern = self.block_design()
        else:
            self.pattern = pat
        self.original_pattern = self.pattern # save original pattern


    def x_positions(self):
        # returns a list of x coordinate modifiers for individual block placement.
        # with 0,0 being the center of the grid, it's defines the center of each block in overall block units
        # a 3x3 grid would be [-1,0,1]
        # a 4x4 grid would be [-1.5, -0.5, 0.5, 1.5]
        if self.num_blocks % 2 != 0:
            return list(map(lambda x: x, range(-int((self.num_blocks-1)/2), int((self.num_blocks-1)/2+1), 1)))
        elif self.num_blocks % 2 == 0:
           return list(map(lambda x: x + 0.5, range(-int(self.num_blocks/2), int(self.num_blocks/2), 1)))
        
    
    def y_positions(self):
        # returns list of y coordintate modifiers in the same manner as the x_positions() method
        # list starts with positive values (top of grid) instead of negative as in x_positions() (left of grid)
        if self.num_blocks % 2 != 0:
            return list(map(lambda x: x, range(int((self.num_blocks-1)/2), -int((self.num_blocks-1)/2+1), -1)))
        elif self.num_blocks % 2 == 0:
            return list(map(lambda x: x - 0.5, range(int(self.num_blocks/2), -int(self.num_blocks/2), -1)))


    def position_grid(self):
        return [[(self.h_center + x * self.scale, self.v_center + y * self.scale) for x in self.x_positions()] for y in self.y_positions()]


    def spread_blocks(self, distance):
        spreader = [[(x * distance, y * distance) for x in self.x_positions()] for y in self.y_positions()]
        self.positions = np.add(self.positions, spreader)    
        self.__spread = False if distance == 0 else True # for data logging purposes
        

    def block_design(self):
        if self.block_type == "random":
            temp = [random.randint(1,6) for _ in range((self.num_blocks * self.num_blocks))]
            design = []
            for i in range(0, len(temp), self.num_blocks):
                design.append(temp[i: i + self.num_blocks])
        elif self.block_type == "fixed":
            # for testing only
            design = [[5,5,5],[2,2,2],[6,6,6]] if self.num_blocks == 3 else [[5,5,5,5],[2,2,2,2],[6,6,6,6]]
            # a fixed pattern is specified during initialiation by passing a matrix into the pat var
        return design

    
    def display_grid(self): 
        shape_matrix = []
        for row1, row2 in zip(self.positions, self.pattern):
            row_list = []
    
            for var, x in zip(row1, row2): 
                block = KohBlock(
                    win = self.win,
                    line = self.line_color,
                    scale = self.scale,
                    pos = (var[0], var[1]),
                    shape = x
                )       
                row_list.append(block)
            shape_matrix.append(row_list)

        for row in shape_matrix:
            for stim in row:
                stim.draw()


    def rotate_grid(self, n: int):
        for i in range(n):
            rotated = [list(reversed(col)) for col in zip(*self.pattern)]
            updated_blocks = []
            for row in rotated:
                temp = []
                for i in row:
                    if i in [1, 2, 3]:
                        temp.append(i+1)
                    elif i == 4:
                        temp.append(1)
                    else:
                        temp.append(i)
                updated_blocks.append(temp)
        
            self.pattern = updated_blocks
        self.__rotation = n
    

    def reset_pattern(self):
        self.pattern = self.original_pattern

    
    def reset_positions(self):
        self.positions = self.original_positions
    

    def reset_grid(self):
        self.pattern = self.original_pattern
        self.positions = self.original_positions


    def log_design(self):
        return self.pattern
    

    def log_position(self):
        return self.pos_number
        

    def log_rotation(self):
        rotations = [0, 90, 180, 270]
        return rotations[self.__rotation]
        
    
    def log_spread(self):
        return self.__spread
    

    def log_outline(self):
        return True if self.line_color else False
    

class KohStimuli():
    
    def __init__(self, condition: str, grid_size = 3):
        self.condition = condition
        self.grid_size = grid_size
        self._stimuli = {
            "test": None,
            "target": None,
            "distractor_1": None,
            "distractor_2": None
        }


    # method to convert a int id for locations into a tuple of x, y coordinates
    def __set_positions(self, location: int, scale_param: int):
        if False:
            if location == 0: # the test location at 0, 0
                return 0, self.set_visual_angle(2.0), 0 # (0, 150)
            if location == 1:
                return -self.set_visual_angle(4.0), -self.set_visual_angle(2.0), 1 # (-300, -150)
            if location == 2:
                return 0, -self.set_visual_angle(2.0), 2 # (0, -150)
            if location == 3:
                return self.set_visual_angle(4.0), -self.set_visual_angle(2.0), 3 #(300, -150)
        else:
            # calculate relative positions:
            # scale 2.0 is scale * 1.34 -- try scale * nblocks/2 * 1.125
            # scale 4.0 is scale * 2.67
            if location == 0: # the test location at 0, 0
                return 0, (scale_param * (self.grid_size/2)* 1.5), 0 # (0, 150)
            if location == 1:
                return -(scale_param * (self.grid_size/2)* 3), -(scale_param * (self.grid_size/2)* 1.5), 1 # (-300, -150)
            if location == 2:
                return 0, -(scale_param * (self.grid_size/2)* 1.5), 2 # (0, -150)
            if location == 3:
                return (scale_param * (self.grid_size/2)* 3), -(scale_param * (self.grid_size/2)* 1.5), 3 #(300, -150)


    def add_stimulus(self, name: str, location: int, scale: int,  win, block_type, line_color):
        # method returns a tuple with x, y coords for the koh grid based on a number for each location
        position = self.__set_positions(location, scale)
        # target reads the test pattern from the stimulus list
        # TODO define stimulus list for test pattern 
        if name == "test":
            pattern = None # temporary
        # target replicates and possibly rotates the test pattern
        # trial type != catch is limits the pattern duplication to "target" trials
        elif name == "target" and self.trial_type != "catch":
            try:
                # reads pattern from the test stimulus and set's it to match
                pattern = self._stimuli["test"].log_design()
            except:
                raise ValueError("error defining target stimulus")
        # setting "pattern" to none for random block pattern designation
        else:
            pattern = None
        # calls the KohGrid class to create a Koh pattern
        stimulus = KohGrid(position, scale, win, block_type, pattern, line_color, num_blocks = self.grid_size)
        # before adding the distractor to the overall display, first check to ensure it is different
        if "distractor" in name:
            while True:
                if stimulus.pattern not in [self._stimuli["test"].pattern, self._stimuli["target"].pattern]:
                    break 
                else:
                    stimulus = KohGrid(position, scale, win, block_type, pattern, line_color, num_blocks = self.grid_size)
        # add the stimulus to the dict holding the 4 on-screen stimuli
        self._stimuli[name] = stimulus

    
    # method to load a trial condition to set overall screen parameters.
    def load_stimulus_conditions(self, stimuli: list, window: visual.Window):        
        for stim in stimuli:
            # checks for trial type as attached to the target stimulus
            # sets a "target" vs. "catch" trial
            if stim["name"] == "target":
                self.trial_type = stim["validity"]
            
            self.add_stimulus(
                stim["name"], 
                stim["position"], 
                stim["size"],
                window,
                stim["design"],
                stim["line_color"]
                )
            
    def set_visual_angle(self, deg: int):
        if self.condition == "test":
            screen_pix = [1920, 1080]
            screen_mm = [529, 297]
            distance = 1000
        elif self.condition == "far":
            screen_pix = [3840, 2160]
            screen_mm = [1805, 1015]
            distance = 5385 
        elif self.condition == "near":
            screen_pix = [3840, 2160]
            screen_mm = [597, 335] 
            distance = 400
        # assumes that pixels are square
        pix_mm = (screen_pix[0]/screen_mm[0])
        pix = (2 * distance) * math.tan((deg * (math.pi/180))/2) * pix_mm
        return round(pix)
    
    
    def __iter__(self):
        return iter(self._stimuli.keys())
    
    
    def __getitem__(self, key):
        return self._stimuli[key]
    
    
    def __setitem__(self, key, value):
        self._stimuli[key] = value

    
    def keys(self):
        return self._stimuli.keys()
    
    
    def values(self):
        return self._stimuli.values()
    
    
    def items(self):
        return self._stimuli.items()
    

    def record_stimulus(self):
        return {key: value.log_design() for key, value in self._stimuli.items()}
    

    def log_trial_type(self):
        return self.trial_type
    
    
class KohExperiment():
    
    def __init__(self, deg: int, condition: str, window: visual.Window, trial_type: str, grid_size = 3):
        self.__condition = condition
        self.__window = window
        self.__trial_type = trial_type
        self.__grid_size = grid_size
        self.__deg = deg
        self.__set_scale()
        self.__add_koh_trials()


    def generate_trial_list(self):
        style = ["solid", "spread"]
        outline = ["black", None]
        position = [1, 2, 3]
        condition_list = []

        if self.__trial_type == "experiment":
            for s in style:
                for o in outline:
                    for p in position * 2:
                        condition_list.append((s,o,p, "target"))
                    condition_list.append((s,o,p, "catch"))
        elif self.__trial_type == "practice":
            for s in style:
                for o in outline:
                    condition_list.append((s,o,random.choice(position), "target"))
            condition_list.append(("solid", "black", 1, "catch"))
        else:
            raise ValueError(f"trial type: {self.__trial_type} invalid.  Must be 'experiment' or 'practice'")

        trial_list = []

        for trial in condition_list:
            test_pattern = {
                "name": "test", 
                "position": 0, 
                "size":  self.__scale,
                "design": "random",
                "line_color": trial[1],
                "style": trial[0]
            }
            target_pattern = {
                "name": "target", 
                "position": trial[2], 
                "size":  self.__scale,
                "design": "random",
                "line_color": trial[1],
                "style": trial[0],
                "validity": trial[3] # logs target validity. 
                # when stim conditions are loaded, this is checked to set the trials validity
                # validity determines if the target pattern will match the test pattern and what 
                # the correct response will be.  Catch trials do not match, correct response is 0
            }
            positions = [1, 2, 3]
            positions.remove(trial[2])
            distractor_1 = {
                "name": "distractor_1", 
                "position": positions.pop(), 
                "size":  self.__scale,
                "design": "random",
                "line_color": trial[1],
                "style": trial[0]
            }
            distractor_2 = {
                "name": "distractor_2", 
                "position": positions.pop(), 
                "size":  self.__scale,
                "design": "random",
                "line_color": trial[1],
                "style": trial[0]
            }
            trial_list.append([test_pattern, target_pattern, distractor_1, distractor_2])

        if self.__trial_type == "experiment":
            random.shuffle(trial_list) 
        
        return trial_list
    

    def __add_koh_trials(self):
        self.__trials = {}
        index = 0
        for trial in self.generate_trial_list():
            index += 1
            screen = KohStimuli(self.__condition, self.__grid_size)
            screen.load_stimulus_conditions(trial, self.__window)

            if trial[0]["style"] == "spread":
                spread_value = 10
            else:
                spread_value = 0
            
            # add 0 to the list to include targets that are not rotated
            rotation_value = random.choice([1, 2, 3])

            for key, value in screen.items():
                if key in ["target", "distractor_1", "distractor_2"]:
                    value.spread_blocks(spread_value)
                    if key == "target" and rotation_value != 0:
                        value.rotate_grid(rotation_value)

            self.__trials[f"{self.__condition}: {index}"] = screen


    def __set_scale(self):
        if self.__condition == "test":
            screen_pix = [1920, 1080]
            screen_mm = [529, 297]
            distance = 610
        elif self.__condition == "far":
            screen_pix = [3840, 2160]
            screen_mm = [1805, 1015]
            distance = 5385
        elif self.__condition == "near":
            screen_pix = [3840, 2160]
            screen_mm = [597, 335] 
            distance = 400  
        # assumes pixels are squaare
        pix_mm = (screen_pix[0]/screen_mm[0])
        pix = (2 * distance) * math.tan((self.__deg * (math.pi/180))/2) * pix_mm
        # returns the number of pixels producing an object of the entered visual angle
        self.__scale = round(pix)

    
    def __iter__(self):
        return iter(self.__trials.keys())
    
    
    def __getitem__(self, key):
        return self.__trials[key]
    
    
    def __setitem__(self, key, value):
        self.__trials[key] = value

    
    def keys(self):
        return self.__trials.keys()
    
    
    def values(self):
        return self.__trials.values()
    
    
    def items(self):
        return self.__trials.items()
    

class KohPatternLogs:

    def __init__(self):
        self.__patterns = {}
        self.load_pattern_data()

    def add_pattern_to_log(self, pattern: KohGrid):
        if pattern.log_design() not in self.__patterns.values():
            self.__patterns[len(self.__patterns) + 1] = pattern.log_design()

        # return the key for data logging
        for key, value in self.__patterns.items():
            if value == pattern.log_design():
                return key


    def save_pattern_data(self):
        with open("koh_experiment_patterns.csv", 'w', newline='') as datafile:
            writer = csv.writer(datafile)
            for key, value in self.__patterns.items():
                writer.writerow([key, value])        
        datafile.close()


    def load_pattern_data(self):
        if os.path.exists("koh_experiment_patterns.csv"):
            temp = open("koh_experiment_patterns.csv", "r")
            reader = csv.reader(temp)
            for row in reader:
                self.__patterns[row[0]] = row[1]
            temp.close()


    def __iter__(self):
        return iter(self.__patterns.keys())
    

    def __getitem__(self, key):
        return self.__patterns[key]
    

    def __setitem__(self, key, value):
        self.__patterns[key] = value


    def keys(self):
        return self.__patterns.keys()
    

    def values(self):
        return self.__patterns.values()
    

    def items(self):
        return self.__patterns.items()
        

class ExperimentData:

    def __init__(self, filename: str):
        self.__exp_data = []
        self.__filename = filename
        #self.check_for_existing_data()


    def load_data_header(self, *variables):
        # does not check for existing file because the datafile
        # is rewritten each time the exp is run
        self.__exp_data.append([var for var in variables])


    def add_trial_data(self, *variables):
        if len(variables) == len(self.__exp_data[0]):
            self.__exp_data.append([var for var in variables])
        else:
            raise IndexError(f"trial data ({len(variables)} vars) does not match header  ({len(self.__exp_data[0])} vars)")


    def check_for_existing_data(self):
        if os.path.exists(self.__filename):
            temp = open(self.__filename, "r")
            reader = csv.reader(temp)
            next(reader)
            for row in reader:
                self.__exp_data.append(row)
            temp.close()

    
    def save_data(self):
        with open(self.__filename, 'w', newline='') as datafile:
            writer = csv.writer(datafile)
            for row in self.__exp_data:
                writer.writerow(row)
        datafile.close()


    def __iter__(self):
        self.n = 0
        return self
    

    def __next__(self):
        if self.n < len(self.__exp_data):
            trial_data = self.__exp_data[self.n]
            self.n += 1
            return trial_data
        else:
            raise StopIteration


class MouseResponse:
    def __init__(self, stim_size: int, condition: str, window: visual.Window, grid_size):
        self.__stim_size = stim_size
        self.__condition = condition
        self.__set_scale()
        self.__grid_size = grid_size
        self.win = window
        

    def __set_scale(self):
        if self.__condition == "test":
            screen_pix = [1920, 1080]
            screen_mm = [529, 297]
            distance = 610
        elif self.__condition == "far":
            screen_pix = [3840, 2160]
            screen_mm = [1805, 1015]
            distance = 5385
        elif self.__condition == "near":
            screen_pix = [3840, 2160]
            screen_mm = [597, 335] 
            distance = 400  
        # assumes pixels are squaare
        pix_mm = (screen_pix[0]/screen_mm[0])
        pix = (2 * distance) * math.tan((self.__stim_size * (math.pi/180))/2) * pix_mm
        # returns the number of pixels producing an object of the entered visual angle
        self.__scale = round(pix)


    def create_response_boxes(self):
        self.response_box_1 = visual.Rect(
            win = self.win,
            units = "pix",
            size = (self.__scale * (self.__grid_size/2)* 2.25),
            fillColor = [1] * 3,
            opacity = 0.0,
            pos = (-(self.__scale * (self.__grid_size/2)* 3), -(self.__scale * (self.__grid_size/2)* 1.5))
        )

        self.response_box_2 = visual.Rect(
            win = self.win,
            units = "pix",
            size = (self.__scale * (self.__grid_size/2)* 2.25),
            fillColor = [1] * 3,
            opacity = 0.0,
            pos = (0, -(self.__scale * (self.__grid_size/2)* 1.5))
        )

        self.response_box_3 = visual.Rect(
            win = self.win,
            units = "pix",
            size = (self.__scale * (self.__grid_size/2)* 2.25),
            fillColor = [1] * 3,
            opacity = 0.0,
            pos = ((self.__scale * (self.__grid_size/2)* 3), -(self.__scale * (self.__grid_size/2)* 1.5))
        )

        self.response_box_0 = visual.Rect(
            win = self.win,
            units = "pix",
            size = (self.__scale * (self.__grid_size/2)* 2.25),
            fillColor = [1] * 3,
            opacity = 0.0,
            pos = (0, (self.__scale * (self.__grid_size/2)* 1.5))
        )

        self.response_boxes = [self.response_box_0, self.response_box_1, self.response_box_2, self.response_box_3]

        self.mouse = event.Mouse(
            win = self.win,
            visible = True,   
        )
        self.mouse.clickableStim = self.response_boxes


    def collect_mouse_response(self):
        self.create_response_boxes()
        for box in self.response_boxes:
            box.draw()
        self.win.flip()
        clicked = False
        start_time = clock.getTime()
        while not clicked:
            # check the list of shapes
            for n, box in enumerate(self.response_boxes):
                if self.mouse.isPressedIn(box):
                    clicked = True
                    response = n 
                    end_time = clock.getTime()
                    break # exit this loop
                else: # this runs once at the completion of the for loop
                # breathe for 1 ms
                    time.sleep(0.001)
        rt = round((end_time - start_time) * 1000)
        return (response, rt)
    

if __name__ in "__main__":
    from psychopy import event
    
    win = visual.Window(
        monitor="hp_home_main", #"hp_home_main", #"surface", #"testMonitor",  # "BlackLaptop",,
        fullscr=True,
        size=[1920, 1080],  # [1920, 1080],# [1280, 1024], #[2736, 1824], #[1600, 900],
        screen=0,
        color=[.5] * 3,
        units="pix"
    )

    condition = "test"
    subj_id = "0001"

    #test = KohExperiment(1.5, condition, win)

    #for key, value in test.items():
        #for x, y in value.items():
            #y.display_grid()
        

        #event.waitKeys()
    
    """test = KohGrid((0,0, 1),50, win, block_type="random", num_blocks=4)
    test.spread_blocks(25)
    test.display_grid()
    win.flip()
    event.waitKeys()"""

    """n = 4
    x_pos = list(map(lambda x: x + 0.5, range(-int(n/2), int(n/2), 1)))
    y_pos = list(map(lambda x: x - 0.5, range(int(n/2), -int(n/2), -1)))
    test = [[(x, y) for x in x_pos] for y in y_pos]
    print(test)"""

    """n = 1
    x_pos = list(map(lambda x: x, range(-int((n-1)/2), int((n-1)/2+1), 1)))
    y_pos = list(map(lambda x: x, range(int((n-1)/2), -int((n-1)/2+1), -1)))

    positions = [[(x, y) for x in x_pos] for y in y_pos]
    print(positions)"""

    practice_trials = KohExperiment(1.5, condition, win, "practice", 3)
    responses = MouseResponse(1.5, condition, win, 3)
    for key, value in practice_trials.items():
        for practice_n, trial_n in value.items():
            trial_n.display_grid()

        print(responses.collect_mouse_response())

