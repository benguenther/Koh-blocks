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
            design = [[5,5,5],[2,2,2],[6,6,6]] # need to specify where it will be coming from  [[1,2,3],[4,5,6],[6,6,6]]
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