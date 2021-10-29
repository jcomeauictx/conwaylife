#!/usr/bin/python
'''Conway's Game of Life

   placed in the public domain by jc@unternet.net 2011-06-11
'''
import sys, os, Tkinter, random, time, Image, ImageTk
WIDTH, HEIGHT = 50, 50  # of game board
CELLSIZE = 10  # width and height of a single cell
CHANCE = .09  # chance of random cell being alive at start
TICKTIME = 200  # time in milliseconds between ticks (plus processing time)
IMAGE = Image.new('RGBA', (CELLSIZE, CELLSIZE), (255, 255, 255, 0))
GLIDER = [[1, 1, 1], [1, 0, 0], [0, 1, 0]]  # simple glider
class Cell(Tkinter.Label, object):
 'a cell is the basic unit of Life'
 def __init__(self, master, image, alive = 'random'):
  'cell constructor'
  super(Cell, self).__init__(master, image = image)
  self.alive, self.board = alive, master
  if alive == 'random':
   self.alive = [False, True][(random.random() < CHANCE)]
  elif alive == 'glider':
   self.alive = False
  self.tick[1](self)
 def phase_1(self):
  "set this cell's state; don't update its representation until phase 2"
  surrounded_by = self.live_neighbors()
  if surrounded_by < 2 or surrounded_by > 3:  # rules 1 and 3
   self.alive = False
  elif surrounded_by == 3:  # rule 4; rule 2 is covered by default
   self.alive = True
 def phase_2(self):
  "based on the decisions made in phase 1, update this cell's state"
  self.config({'background': ['white', 'green'][self.alive]})
 def live_neighbors(self):
  'determine living neighbors based on their color'
  grid_info = self.grid_info()
  row, column, living = int(grid_info['row']), int(grid_info['column']), 0
  for r in (row - 1) % HEIGHT, row, (row + 1) % HEIGHT:
   for c in (column - 1) % WIDTH, column, (column + 1) % WIDTH:
    cell = self.master.grid_slaves(row = r, column = c)[0]
    living += cell.cget('background') == 'green'
  living -= (self.cget('background') == 'green')  # don't count myself
  return living
 def set(self, alive = True):
  self.alive = alive
  self.phase_2()
 def reset(self):
  self.set(False)
 tick = [phase_1, phase_2]
class Board(Tkinter.Tk, object):
 "the 'game board' of Life"
 def __init__(self, alive = 'random'):
  'set up the game board'
  super(Board, self).__init__(None)
  self.title("Conway's Game of Life")
  self.IMAGE = ImageTk.PhotoImage(IMAGE)
  # now create the cells
  for row in range(HEIGHT):
   for column in range(WIDTH):
    Cell(self, self.IMAGE, alive).grid(row = row, column = column)
  if alive == 'glider':
   start = WIDTH / 2, WIDTH / 2
   for row in range(len(GLIDER)):
    for column in range(len(GLIDER[0])):
     cell = self.grid_slaves(row = start[0] + row,
      column = start[1] + column)[0]
     cell.set(GLIDER[row][column])
  self.after(TICKTIME, self.tick)
 def tick(self):
  'run one "generation", or "tick"'
  for cell in self.children.values():
   cell.tick[0](cell)
  for cell in self.children.values():
   cell.tick[1](cell)
  self.after(TICKTIME, self.tick)
if __name__ == '__main__':  # run program, not import or pydoc
 life = Board(*sys.argv[1:])
 life.mainloop()
