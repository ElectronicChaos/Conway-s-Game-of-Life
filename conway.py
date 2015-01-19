'''
Pygame implementation of Conway's Game of Life
Coded by Daniel Hill(daniel.mitchell.hill@gmail.com)

Copyright (C) 2015 Daniel Hill

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Controls:
Escape key closes program
Space key pauses/un-pauses
R key randomizes board
C key clears board
Clicking on a cell toggles its state

'''

import pygame, random, sys, time

#SIZE is the number of rows and columns
#Each cell will be CELL_SIZE * CELL_SIZE pixels
SIZE = 50
CELL_SIZE = 20
#Draw a border around cells. Setting this to true may cause performance issues in less powerful machines
border = True

#Colors for filled cells and background
filled = 219,211,151
background = 115,115,115

#ticks_per_second is the number of times per second the game updates
ticks_per_second = 4
next_time = int(round(time.time() * 1000L))
skip_ticks = 1000 / ticks_per_second

screen = pygame.display.set_mode([SIZE * CELL_SIZE, SIZE * CELL_SIZE])
pygame.display.set_caption("Conway's Game of Life")

is_running = True
is_paused = True

class Cell:
	def __init__(self, alive, position):
		#alive is whether or not the cell is alive. Shouldn't be modified directly unless by the update() method
		self.alive = alive
		#next_alive is whether or not the cell will be alive in the next iteration. Modify this instead of alive
		self.next_alive = False
		
		self.x = position % SIZE
		self.y = position / SIZE
		self.rect = pygame.Rect([self.x * CELL_SIZE, self.y * CELL_SIZE], [CELL_SIZE, CELL_SIZE])
		self.blank_rect = pygame.Rect([self.x * CELL_SIZE + 1, self.y * CELL_SIZE +1], [CELL_SIZE - 1, CELL_SIZE - 1])
	
	#Creates a list of neighbors to the cell
	def neighbors(self):
		self.neighbors = []
		x_coords = [n for n in range(self.x - 1, self.x + 2) if n >= 0 and n < SIZE]
		y_coords = [m for m in range(self.y - 1, self.y + 2) if m >= 0 and m < SIZE]
		
		for n in x_coords:
			for m in y_coords:
				#Exclude this cell
				if n == self.x and m == self.y:
					continue
				position = (m * SIZE) + n
				self.neighbors.append(board[position])

#Create the board, set each cell to false, and generate the neighbors lists				
board = []
for x in range(SIZE * SIZE):
	board.append(Cell(False, x))
for c in board:
	c.neighbors()

def change_ticks(tps):
	global ticks_per_second
	global skip_ticks
	if ticks_per_second > 1 or tps > 0:
		ticks_per_second += tps
		skip_ticks = 1000 / ticks_per_second

#Ticks the board one iteration forward
def tick():
	for cell in board:
		count = len([c for c in cell.neighbors if c.alive])
		
		if cell.alive and (count == 2 or count == 3):
			cell.next_alive = True
		elif not cell.alive and count == 3:
			cell.next_alive = True
		else:
			cell.next_alive = False
	update()

#Sets the board to a randomized state. 25% chance for a cell to be true
def randomize():
	for cell in board:
		cell.next_alive = random.choice([True, False, False, False])
	update()

#Clears the board. 
def clear():
	for cell in board:
		cell.next_alive = False
	update()
	
#Update the board. Should be called after modifying Cell.next_alive
def update():
	for cell in board:
		if cell.next_alive:
			cell.alive = True
		else:
			cell.alive = False

#Render cells. If border is true, render each cell 'filled', and then render dead cells 1 pixel smaller in 'background'
def render():
	for cell in board:
		if border:
			screen.fill(filled, cell.rect)
			if not cell.alive:
				screen.fill(background, cell.blank_rect)
		elif cell.alive:
			screen.fill(filled, cell.rect)
			

def on_click(position):
	#Convert x & y of the screen to x & y of the board
	x_pos = (position[0] / CELL_SIZE) % SIZE
	y_pos = (position[1] / CELL_SIZE) % SIZE
	cell_pos = (y_pos * SIZE) + x_pos
	
	#Toggle the clicked cell
	board[cell_pos].next_alive = not board[cell_pos].alive
	update()
			
print ""
print "Conway's Game of Life"
print "Controls: "
print "Escape key closes program"
print "Space key pauses/un-pauses"
print "R key randomizes board"
print "C key clears board"
print "B toggles borders"
print "Clicking on a cell toggles its state"
print "Numkey + and - increase and decrease speed"

#Main game loop
while is_running:
	for event in pygame.event.get():
		if event.type==pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			is_running=False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				is_paused = not is_paused
			elif event.key == pygame.K_r:
				randomize()
			elif event.key == pygame.K_c:
				clear()
			elif event.key == pygame.K_b:
				border = not border
			elif event.key == pygame.K_KP_PLUS:
				change_ticks(1)
			elif event.key == pygame.K_KP_MINUS:
				change_ticks(-1)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			on_click(pygame.mouse.get_pos())
		
			

	while int(round(time.time() * 1000L)) > next_time:
		screen.fill(background)
		render()
		if not is_paused:
			tick()
		pygame.display.flip()
		next_time += skip_ticks

pygame.quit()
sys.exit()