from random import randint
from BaseAI import BaseAI

from Displayer import Displayer
from Grid import Grid
import math

def main():
	grid = Grid()
'''
def monotonicity (self, grid):
		[mono_up, mono_down, mono_left, mono_right] = [0, 0, 0, 0]

		new_grid = copy.deepcopy(grid)


		# First reset all value of the grid to log base 2
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
				mono_up += upper - lower
			else:
				mono_down += lower - upper

		for row in range(4):
			for col in range(3):
				lefter = new_grid.map[row][col]
				righter = new_grid.map[row][col + 1]

			if lefter > righter:
				mono_left += lefter - righter
			else:
				mono_right += righter - lefter

		score = max(mono_left, mono_right) + max(mono_up, mono_down)

		return score
'''

if __name__ == "__main__":
	main()