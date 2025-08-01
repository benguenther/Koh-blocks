#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual
import random
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
    
    def __init__(self, h_center: int, v_center: int, scale: int,  win, block_type = "", pat = None):#spread: int, 
        self.h_center = h_center
        self.v_center = v_center
        self.scale = scale
        self.block_type = block_type # specifies if blocks are random or fixed
        self.win = win
        
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
                    line = "black",
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
    
    """
    def __repr__(self):
        return f"KohGrid({self.pattern})"
    """

class KohStimuli(KohGrid):
    
    def __init__(self):
        self._stimuli = {
            "test": None,
            "target": None,
            "distractor_1": None,
            "distractor_2": None
        }

    
    # needs to read infomation from somewhere and then create KohGrid objects
    def add_stimulus(self, name: str, h_center: int, v_center: int, scale: int,  win, block_type):
        if name == "target":
            try:
                pattern = self._stimuli["test"].log_design()
            except:
                raise ValueError("error defining target stimulus")
        else:
            pattern = None
        
        stimulus = KohGrid(h_center,v_center, scale, win, block_type, pattern)
        self._stimuli[name] = stimulus
        

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
        

class KohTest:
    pass
# consider a class for a full stimulus screen and then a trial class


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
    
    screen = KohStimuli()
    screen.add_stimulus("test", 0,0, 58, win, "random")
    screen.add_stimulus("target", 300,0, 58, win, "")
    screen.add_stimulus("distractor_1", 300,300, 58, win, "random")
    screen.add_stimulus("distractor_2", 300,-300, 58, win, "random")
    print(screen.record_stimulus())

    for key, value in screen.items():
        if key in ["target", "distractor_1", "distractor_2"]:
            value.spread_blocks(20)
            if key == "target":
                value.rotate_grid(1)

        value.display_grid()


    win.flip()
    event.waitKeys()

