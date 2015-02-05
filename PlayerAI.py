#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI

from Displayer import Displayer
from Grid import Grid

import math
import time
import sys
import copy

class PlayerAI(BaseAI):

	# Heuristic weighting coefficient
	smoothness_weight = 0.1
	monotonicity_weight = 1.0
	max_tile_value_weight = 1.0
	empty_cell_weight = 2.7

	# Search time limit = 1 sec
	search_time_limit = 1
	start_time = None

	# Initial search depth = 0
	# Current best move = None
	search_depth = 0
	current_best = None

	def getMove(self, grid):

		# Start timer, set initial serach depth to 0
		self.start_time = time.time()
		self.search_depth = 0

		# Perform iterative deepening search
		return self.iterative_deep_alpha_beta_search(grid)		

	# This function return true if available time < 0.1 sec
	def time_alarm(self):
		if time.time() - self.start_time > self.search_time_limit - 0.1:
			return True
		else:
			return False

	def iterative_deep_alpha_beta_search(self, grid):

		best_move = None

		while True:

			# Store result for search with specific depth
			result = self.alpha_beta_search(grid, self.search_depth)
			
			# If time is not enough to complete search at this depth, result = None
			# Else, result is the best move, write it into best_move
			if result == None:
		 		# print "search depth:" , self.search_depth - 2
				return best_move
			else:
				best_move = result

			# Increase search depth	
			self.search_depth += 2

		return best_move
	
	def alpha_beta_search(self, grid, depth):

		v = self.max_value(grid, - sys.maxint - 1, sys.maxint, depth)
		# While searching, the max_value function will write the best move to 
		# class variable current_best, thus we need to only return current_best
		return self.current_best

	# The max_value function for alpha-beta search
	def max_value(self, grid, alpha, beta, depth):

		# v = minus infinity
		v = - sys.maxint - 1

		# Since we can not alter the original grid, copy a new one
		# Get available moves and store it in moves
		new_grid = copy.deepcopy(grid)
		moves = new_grid.getAvailableMoves()


		# Reach the bottom depth of search
		if depth == 0:

			# If the total search depth is 0 (the first loop in iterative search)
			# we need to perform greedy search
			if self.search_depth == 0:

				# score = minus infinity
				score = - sys.maxint - 1

				# For each move in moves
				for move in moves:

					# use temp to store the score for each move
					temp = self.player(copy.deepcopy(grid), move)

					# If temp is greater than current score
					# rewrite current score and best move
					if self.evaluation(temp) >= score:
						self.current_best = move
						score = self.evaluation(temp)

			# If reach the bottom depth, then return the evaluation score
			return self.evaluation(grid)


		# If the depth is not 0 (not reach the bottom)
		# For each move in moves		
		for move in moves:

			# Time check, if True, then return None
			if self.time_alarm():
				self.current_best = None
				return None
			
			temp = self.min_value(self.player(new_grid, move), alpha, beta, depth - 1)

			# If catching None from lower level, meaning time is no enough
			# Also return None in this level
			if temp == None:
				self.current_best = None
				return None

			# Below codes perform alpha-beta pruning
			if temp >= v:
				# If this level is the top level, write the best move
				if depth == self.search_depth:
					self.current_best = move
				v = temp
			if v >= beta:
				return v
			alpha = max(alpha, v)

		return v

	def min_value(self, grid, alpha, beta, depth):

		# v = infinity
		v = sys.maxint

		# Create new grid and get available cell position
		new_grid = copy.deepcopy(grid)
		cells = new_grid.getAvailableCells()

		moves = []

		# Now we can insert tiles with number 2 or 4
		# move = (2 or 4, cell position)
		for cell in cells:
			moves.append((2,cell))
			moves.append((4,cell))

		# For each move in moves			
		for move in moves:

			# Time check, if True, return None
			if self.time_alarm():
				return None

			# Perform alpha-beta pruning
			v = min(v, self.max_value(self.computer(new_grid, move), alpha, beta, depth - 1))
			if v == None:
				return None
			if  v <= alpha:
				return v
		beta = min(beta, v) 

		return v

	# Evaluation function 	
	def evaluation (self, grid):

		empty_cell = len(grid.getAvailableCells())
		return self.smoothness_weight * self.smoothness(grid) + self.monotonicity_weight * self.monotonicity(grid) + self.max_tile_value_weight * self.max_tile_value(grid) + self.empty_cell_weight * empty_cell		

	# Transition model for player
	def player(self, grid, move):
		new_grid = copy.deepcopy(grid)
		# make a move, and then change the grid
		new_grid.move(move)
		return new_grid
	
	# Transition model for computer
	def computer(self, grid, move):
		new_grid = copy.deepcopy(grid)
		# value = tile number
		# position = where to put the tile
		(value, position) = move
		new_grid.insertTile(position, value)
		return new_grid


	# Function to measure the monotonicity of a grid
	def monotonicity (self, grid):

		[mono_up, mono_down, mono_left, mono_right] = [0, 0, 0, 0]
		new_grid = copy.deepcopy(grid)

		for row in range(4):
			for col in range(4):
				cell_value = new_grid.map[row][col]
				if cell_value != 0:
					new_grid.setCellValue((row,col), math.log(cell_value,2))

		for col in range(4):
			for row in range(3):
				upper = new_grid.map[row][col]
				lower = new_grid.map[row + 1][col]

				if upper > lower:
					mono_up -= upper - lower
				else:
					mono_down -= lower - upper

		for row in range(4):
			for col in range(3):
				lefter = new_grid.map[row][col]
				righter = new_grid.map[row][col + 1]

				if lefter > righter:
					mono_left -= lefter - righter
				else:
					mono_right -= righter - lefter
		score = max(mono_left, mono_right) + max(mono_up, mono_down)
		
		return score

	# Function to measure the smoothness of a grid
	def smoothness(self, grid):

		score = 0

		new_grid = copy.deepcopy(grid)

		for row in range(4):
			for col in range(4):
				cell_value = new_grid.map[row][col]
				if cell_value != 0:
					new_grid.setCellValue((row,col), math.log(cell_value,2))

		for row in range(4):
			for col in range(4):
				if new_grid.map[row][col] != 0:
					for i in range(row + 1, 4):
						if new_grid.map[i][col] != 0:
							score -= abs(new_grid.map[row][col] - new_grid.map[i][col])
							break
					for j in range(col + 1, 4):
						if new_grid.map[row][j] != 0:
							score -= abs(new_grid.map[row][col] - new_grid.map[row][j])
							break

		return score

	# Function to return the max tile value of a grid
	def max_tile_value(self, grid):

		max_tile = 0
		for row in range(4):
			for col in range(4):
				if grid.map[row][col] > max_tile:
					max_tile = grid.map[row][col]

		return math.log(max_tile,2)




