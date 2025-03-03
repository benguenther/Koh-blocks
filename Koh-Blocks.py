#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Psychopy version: 2024.2.1post4
# Python version: 3.10.11

from psychopy import visual, event
import math




win = visual.Window(
    monitor="hp_home_main", #"surface", #"testMonitor",  # "BlackLaptop",,
    fullscr=True,
    size=[1920, 1080],  # [1920, 1080],# [1280, 1024], #[2736, 1824], #[1600, 900],
    screen=0,
    color=[+1] * 3,
    units="pix"
)




"""def visual_angle(distance, size):
    theta = 2 * math.atan((size / (2 * distance)))
    print(theta)
    return theta * (180/math.pi)
    #return round(theta * (180/math.pi),1)

va = visual_angle(70, 40)
print(va)

print((2 * 70) * math.tan(((va * (math.pi/180))/2)))

va_rad = va * (math.pi/180)
size_cm = (2*70) * math.tan(va_rad/2)
print(size_cm)"""



def va_to_pix(width, # stimulus width in degrees VA
              height, # stiulus height in degrees VA
              screen, # string for the monitor name
              distance # viewing distance in mm
              ): # function returns a list (width x height) of the stimulus in pix
    if screen == "test":
        screen_pix = [1920, 1080]
        screen_mm = [529, 297]
        
    pix_mm = [(screen_pix[0]/screen_mm[0]), (screen_pix[1]/screen_mm[1])]

    w_pix = (2 * distance) * math.tan((width * (math.pi/180))/2) * pix_mm[0]
    h_pix = (2 * distance) * math.tan((height * (math.pi/180))/2) * pix_mm[1]

    return [round(w_pix), round(h_pix)]

size = va_to_pix(2, 2, "test", 610)

# Monitor Dimensions
# width = 1920
# height = 1080
# 529 mm
# 297 mm



block_positions = [[(-1*size[0]), size[1]], [0, size[1]], [size[0], size[1]],
             [(-1*size[0]), 0], [0, 0], [size[0], 0],
             [(-1*size[0]), (-1*size[1])], [0, (-1*size[1])], [size[0], (-1*size[1])]
             ]
    
block_colors = [
    ("black"), ("red"), ("black"),
    ("red"), ("black"), ("red"),
    ("black"), ("red"), ("black")
]

shape_matrix = []

for row in range(1):
    row_list = []
    for col, pos, color in zip(range(9), block_positions, block_colors):
        block = visual.Rect(
        win = win,
        units = "pix",
        lineColor = "black",
        color = color,
        size = (size[0], size[1]),
        pos = (pos[0], pos[1])
        )       
        row_list.append(block)
    shape_matrix.append(row_list)

"""for row in shape_matrix:
    for stim in row:
        stim.draw()

win.flip()
event.waitKeys()"""

adj_vert = [
    ((-1*(size[1]/2)), (-1*(size[0]/2))),
    ((size[1]/2), (-1*(size[0]/2))),
    ((-1*(size[1]/2)), (size[0]/2)),
    ((size[1]/2), (size[0]/2)),
    ((-1*(size[1]/2)), (size[0]/2)),
    ((size[1]/2), (-1*(size[0]/2)))
]

vert_a = []
for a, b in adj_vert:
    if b < 0:
        vert_a.append((a, (b + 2*b)))
    else:
        vert_a.append((a, (b - 2*b)))

print(adj_vert)
print(vert_a)

t1 = visual.ShapeStim(
    win = win,
    vertices = (adj_vert[0], adj_vert[1], adj_vert[2]),#((0,0),(size[1],0),(0,size[0])),
    fillColor = "red",
    lineColor = "black",
    units = "pix",
)

t2 = visual.ShapeStim(
    win = win,
    vertices = (adj_vert[3], adj_vert[4], adj_vert[5]),
    fillColor = "white",
    lineColor = "black",
    units = "pix"
)


t3 = visual.ShapeStim(
    win = win,
    vertices = (vert_a[0], vert_a[1], vert_a[2]),#((0,0),(size[1],0),(0,size[0])),
    fillColor = "red",
    lineColor = "black",
    units = "pix",
)

t4 = visual.ShapeStim(
    win = win,
    vertices = (vert_a[3], vert_a[4], vert_a[5]),
    fillColor = "white",
    lineColor = "black",
    units = "pix"
)

vert_pair = [((0,0),(size[1],0),(0,size[0])), 
             ((size[1],size[0]),(size[1],0),(0,size[0]))
             ]


t1.draw()
t2.draw()
t3.draw()
t4.draw()
win.flip()
event.waitKeys()


class SplitKohBlock:
    def __init__(self, win, scale, line, pos, ori=0):
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
            ori = ori
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
            ori = ori
        )
    
    def draw(self):
        self.triangle1.draw()
        self.triangle2.draw()


block1 = SplitKohBlock(win, size[0], line = "black", pos = (0,0), ori = 90)
block2 = SplitKohBlock(win, size[0], line = None, pos = ((-1*size[0]), size[1]), ori = 180)
block1.draw()
block2.draw()
win.flip()
event.waitKeys()



shape_matrix = []

for row in range(1):
    row_list = []
    for col, pos, color in zip(range(9), block_positions, block_colors):
        block = visual.Rect(
        win = win,
        units = "pix",
        lineColor = "black",
        color = color,
        size = (size[0], size[1]),
        pos = (pos[0], pos[1])
        )       
        row_list.append(block)
    shape_matrix.append(row_list)

class KohBlockPattern:
    def __init__(self, size, center_vert, center_horiz, color, outline = False):
        #self.center_vert = center_vert
        #self.center_horiz = center_horiz
        self.size = size
        self.color = color
        self.outline = outline

        print((center_vert + size))
        self.positions = [
            [(center_vert + size), (center_horiz - size)], # cube 1
            [(center_vert + size),(center_horiz)], # cube 2
            [(center_vert + size),(center_horiz + size)], # cube 3
            [(center_vert),(center_horiz - size)], # cube 4
            [(center_vert),(center_horiz)], # cube 5
            [(center_vert),(center_horiz + size)], # cube 6
            [(center_vert - size),(center_horiz - size)], # cube 7
            [(center_vert - size),(center_horiz)], # cube 8
            [(center_vert - size),(center_horiz + size)] # cube 9
        ]
        print(self.positions)

    #def shape_matrix(self):
        shape_matrix = []
        for row in range(1):
            row_list = []
            for col, pos, color in zip(range(9), self.positions, self.color):
                print(pos[0], pos[1])
                block = visual.Rect(
                    win = win,
                    units = "pix",
                    lineColor = "black",
                    color = color,
                    size = size,
                    pos = (pos[0], pos[1])
                )       
                row_list.append(block)
            shape_matrix.append(row_list)
        #return shape_matrix

    for row in shape_matrix:
        for stim in row:
            stim.draw()

KohBlockPattern(size= size[0], center_vert = 0, center_horiz=200, color = block_colors)
KohBlockPattern(size= size[0], center_vert = 0, center_horiz=-200, color = block_colors)

win.flip()
event.waitKeys()