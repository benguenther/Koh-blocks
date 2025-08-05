#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual
import random, math
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
    
    def __init__(self, position: tuple, scale: int,  win, block_type = "", pat = None, line_color = "black"):#spread: int, 
        self.h_center = position[0]#h_center
        self.v_center = position[1]#v_center
        self.scale = scale
        self.block_type = block_type # specifies if blocks are random or fixed
        self.win = win
        self.line_color = line_color
        
        self.positions = self.position_grid()
        self.original_positions = self.positions # save the original just in case

        if pat is None:
            self.pattern = self.block_design()
        else:
            self.pattern = pat
        self.original_pattern = self.pattern # save original pattern


    def position_grid(self):
        self.positions = [
            [
                [(self.h_center - self.scale), (self.v_center + self.scale)], # cube 1
                [(self.h_center),(self.v_center + self.scale)], # cube 2
                [(self.h_center + self.scale),(self.v_center + self.scale)]
                ], # cube 3
            [
                [(self.h_center - self.scale),(self.v_center)], # cube 4
                [(self.h_center),(self.v_center)], # cube 5
                [(self.h_center + self.scale),(self.v_center)]
                ], # cube 6
            [
                [(self.h_center - self.scale),(self.v_center - self.scale)], # cube 7
                [(self.h_center),(self.v_center - self.scale)], # cube 8
                [(self.h_center + self.scale),(self.v_center - self.scale)] # cube 9
                ]
        ]
        return self.positions
    
    def move_position_grid(self, new_h, new_v):
        self.positions = [
            [
                [(new_h - self.scale), (new_v + self.scale)], # cube 1
                [(new_h),(new_v + self.scale)], # cube 2
                [(new_h + self.scale),(new_v + self.scale)]
                ], # cube 3
            [
                [(new_h - self.scale),(new_v)], # cube 4
                [(new_h),(new_v)], # cube 5
                [(new_h + self.scale),(new_v)]
                ], # cube 6
            [
                [(new_h - self.scale),(new_v - self.scale)], # cube 7
                [(new_h),(new_v - self.scale)], # cube 8
                [(new_h + self.scale),(new_v - self.scale)] # cube 9
                ]
        ]


    def spread_blocks(self, distance):
        spreader = [
            [
                [(-distance), (distance)], # cube 1
                [(0), (distance)], # cube 2
                [(distance), (distance)]
                ], # cube 3
            [
                [(-distance), (0)], # cube 4
                [(0), (0)], # cube 5
                [(distance), (0)]
            ], # cube 6
            [
                [(-distance), (-distance)], # cube 7
                [(-0), (-distance)], # cube 8
                [(distance), (-distance)]
            ], # cube 9
        ]   
        self.positions = np.add(self.positions, spreader)


    def block_design(self):
        if self.block_type == "random":
            temp = [random.randint(1,6) for _ in range(9)]
            design = []
            for i in range(0, len(temp), 3):
                design.append(temp[i: i + 3])
        elif self.block_type == "fixed":
            design = [[5,5,5],[2,2,2],[6,6,6]] # used for testing
            # pattern is manually specified during initialiation by passing a matrix into the pat var
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
    

    def reset_pattern(self):
        self.pattern = self.original_pattern

    
    def reset_positions(self):
        self.positions = self.original_positions
    

    def reset_grid(self):
        self.pattern = self.original_pattern
        self.positions = self.original_positions


    def log_design(self):
        return self.pattern
    

class KohStimuli():
    
    def __init__(self):
        self._stimuli = {
            "test": None,
            "target": None,
            "distractor_1": None,
            "distractor_2": None
        }

    # method to convert a int id for locations into a tuple of x, y coordinates
    def __set_positions(self, location: int):
        if location == 0: # the test location at 0, 0
            return 0, 150
        if location == 1:
            return -300, -150
        if location == 2:
            return 0, -150
        if location == 3:
            return 300, -150

    def add_stimulus(self, name: str, location: int, scale: int,  win, block_type, line_color):
        # method returns a tuple with x, y coords for the koh grid based on a number for each location
        position = self.__set_positions(location)
        # target reads the test pattern from the stimulus list
        # TODO define stimulus list for test pattern 
        if name == "test":
            pattern = None # temporary
        # target replicates and possibly rotates the test pattern
        elif name == "target":
            try:
                # reads pattern from the test stimulus and set's it to match
                pattern = self._stimuli["test"].log_design()
            except:
                raise ValueError("error defining target stimulus")
        # setting "pattern" to none for random block pattern designation
        else:
            pattern = None
        # calls the KohGrid class to create a Koh pattern
        stimulus = KohGrid(position, scale, win, block_type, pattern, line_color)
        # before adding the distractor to the overall display, first check to ensure it is different
        if "distractor" in name:
            while True:
                if stimulus.pattern not in [self._stimuli["test"].pattern, self._stimuli["target"].pattern]:
                    break 
                else:
                    stimulus = KohGrid(position, scale, win, block_type, pattern, line_color)
        # add the stimulus to the dict holding the 4 on-screen stimuli
        self._stimuli[name] = stimulus

    
    def load_stimulus_conditions(self, stimuli: list, window: visual.Window):        
        for stim in stimuli:
            self.add_stimulus(
                stim["name"], 
                stim["position"], 
                stim["size"],
                window,
                stim["design"],
                stim["line_color"]
                )


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


class KohExperiment():
    
    def __init__(self, deg: int, condition: str, window: visual.Window):
        self.__condition = condition
        self.__window = window
        self.__deg = deg
        self.__set_scale()
        self.__add_koh_trials()
        

    def generate_trial_list(self):
        style = ["solid", "spread"]
        outline = ["black", None]
        position = [1, 2, 3]
        condition_list = []

        for s in style:
            for o in outline:
                for p in position * 2:
                    condition_list.append((s,o,p))

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
                "style": trial[0]
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

        random.shuffle(trial_list) 
        return trial_list
    

    def __add_koh_trials(self):
        self.__trials = {}
        index = 0
        for trial in self.generate_trial_list():
            index += 1
            screen = KohStimuli()
            screen.load_stimulus_conditions(trial, self.__window)

            if trial[0]["style"] == "spread":
                spread_value = 10
            else:
                spread_value = 0
            
            rotation_value = random.choice([0, 1, 2, 3])

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


    def condition_logging(self):
        pass


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
    
    test = KohExperiment(1.5, "test")
    for key, value in test.items():
        for x, y in value.items():
            y.display_grid()
        print(f"{key}: {value.record_stimulus()}")
        win.flip()
        event.waitKeys()



    