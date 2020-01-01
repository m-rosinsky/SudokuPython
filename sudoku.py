import pygame
import time
from color_sheet import *

class Board:
	def __init__(self, box_size=70, margin_size=3, selected=(10,10), font_size=40, wait_time=5):
		self.grid_array = []
		self.perm_array = []
		self.box_size = box_size
		self.margin_size = margin_size
		self.selected = selected
		self.font_size = font_size
		self.wait_time = wait_time

	def init_grid(self):
		self.grid_array = [[4,1,5,0,7,8,2,0,9],
						   [0,6,0,0,2,9,5,0,0],
						   [0,0,0,0,0,1,4,7,0],
						   [3,0,0,0,4,5,0,0,2],
						   [0,0,0,1,0,0,0,5,0],
						   [0,0,7,0,3,0,0,9,0],
						   [6,7,0,9,0,0,1,3,0],
						   [0,4,9,0,1,3,0,2,0],
						   [0,3,1,2,5,0,0,0,6]]

		self.perm_array = [[0,0,0,0,0,0,0,0,0],
						   [0,0,0,0,0,0,0,0,0],
						   [0,0,0,0,0,0,0,0,0],
						   [0,0,0,0,0,0,0,0,0],
						   [0,0,0,0,0,0,0,0,0],
						   [0,0,0,0,0,0,0,0,0],
						   [0,0,0,0,0,0,0,0,0],
						   [0,0,0,0,0,0,0,0,0],
						   [0,0,0,0,0,0,0,0,0]]

		for row in range(9):
			for column in range(9):
				if self.grid_array[row][column] != 0:
					self.perm_array[row][column] = 1
				else:
					self.perm_array[row][column] = 0

	def draw_grid(self):
		fnt = pygame.font.SysFont("courier", self.font_size)
		for row in range(9):
			for column in range(9):
				color = white
				if row == self.selected[0] and column == self.selected[1]:
					if self.perm_array[row][column] == 0:
						color = light_gray
					else:
						color = red
				pygame.draw.rect(screen, color,[(self.margin_size + self.box_size) * column + self.margin_size, (self.margin_size + self.box_size) * row + self.margin_size, (self.box_size),(self.box_size)])
				if self.grid_array[row][column] != 0:
					color = black
					if self.perm_array[row][column] == 0:
						color = cyan
					text = fnt.render(str(self.grid_array[row][column]), 1, color)
					screen.blit(text, (self.box_size*column + self.margin_size*(column-1) + self.box_size/2, self.box_size*row + self.margin_size*(row-1) + self.box_size/2))
		pygame.draw.line(screen, black, (self.box_size*3 + self.margin_size*3,0),(self.box_size*3 + self.margin_size*3,window_height),self.margin_size+1)
		pygame.draw.line(screen, black, (self.box_size*6 + self.margin_size*6,0),(self.box_size*6 + self.margin_size*6,window_height),self.margin_size+1)
		pygame.draw.line(screen, black, (0,self.box_size*3 + self.margin_size*3),(window_width,self.box_size*3 + self.margin_size*3),self.margin_size+1)
		pygame.draw.line(screen, black, (0,self.box_size*6 + self.margin_size*6),(window_width,self.box_size*6 + self.margin_size*6),self.margin_size+1)

	def find_unfilled_box(self,l):
		for row in range(9):
			for column in range(9):
				if self.grid_array[row][column] == 0:
					l[0] = row
					l[1] = column
					return True
		return False

	def check_row(self,row,val):
		for i in range(9):
			if self.grid_array[row][i] == val:
				return True
		return False

	def check_column(self,column,val):
		for i in range(9):
			if self.grid_array[i][column] == val:
				return True
		return False

	def check_box(self,row,column,val):
		for i in range(3):
			for j in range(3):
				if self.grid_array[i+row][j+column] == val:
					return True
		return False

	def check_safe(self,row,column,val):
		return not self.check_row(row,val) and not self.check_column(column,val) and not self.check_box(row-row%3,column-column%3,val)

	def solve(self):
		l = [0,0]
		if not self.find_unfilled_box(l):
			self.selected = (10,10)
			self.draw_grid()
			return True

		row=l[0]
		column = l[1]

		self.selected = (row,column)

		for val in range(1,10):
			if self.check_safe(row,column,val):
				self.grid_array[row][column]=val
				if animate:
					pygame.event.poll()
					pygame.time.wait(self.wait_time)
					self.draw_grid()
					pygame.display.update()
				if self.solve():
					return True
				self.grid_array[row][column] = 0

		return False

pygame.font.init()

board = Board()
board.init_grid()

window_height = (board.box_size * 9) + (board.margin_size * 9) + board.margin_size
window_width = (board.box_size * 9) + (board.margin_size * 9) + board.margin_size
screen = pygame.display.set_mode((window_width,window_height))
screen.fill(gray)

pygame.init()
pygame.display.set_caption("Sudoku by Mike Rosinsky")
clock = pygame.time.Clock()

board_drawn = 0

game_running = True
animate = True

while game_running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			game_running = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			column = pos[0] // (board.box_size + board.margin_size)
			row = pos[1] // (board.box_size + board.margin_size)

			if pygame.mouse.get_pressed()[0]:
				board.selected = (row,column)
			else:
				board.selected = (10,10)
			board.draw_grid()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				if board.solve():
					print("Solved")
				else:
					print("No Solution Possible")
				board.draw_grid()
			elif event.key == pygame.K_SPACE:
				board.init_grid()
				board.selected = (10,10)
				board.draw_grid()
			if board.selected != (10,10):
				if event.key == pygame.K_1:
					board.grid_array[board.selected[0]][board.selected[1]] = 1
				elif event.key == pygame.K_2:
					board.grid_array[board.selected[0]][board.selected[1]] = 2
				elif event.key == pygame.K_3:
					board.grid_array[board.selected[0]][board.selected[1]] = 3
				elif event.key == pygame.K_4:
					board.grid_array[board.selected[0]][board.selected[1]] = 4
				elif event.key == pygame.K_5:
					board.grid_array[board.selected[0]][board.selected[1]] = 5
				elif event.key == pygame.K_6:
					board.grid_array[board.selected[0]][board.selected[1]] = 6
				elif event.key == pygame.K_7:
					board.grid_array[board.selected[0]][board.selected[1]] = 7
				elif event.key == pygame.K_8:
					board.grid_array[board.selected[0]][board.selected[1]] = 8
				elif event.key == pygame.K_9:
					board.grid_array[board.selected[0]][board.selected[1]] = 9
				elif event.key == pygame.K_BACKSPACE:
					board.grid_array[board.selected[0]][board.selected[1]] = 0
				board.draw_grid()


	if board_drawn == 0:
		board.draw_grid()
		board_drawn = 1

	clock.tick(80)
	pygame.display.flip()

pygame.quit()