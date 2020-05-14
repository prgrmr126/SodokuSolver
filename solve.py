import pulp
import time
import sys


def cell_name(i, j, k):
	return 'x_{%d,%d,%d}' % (i, j, k)


class Solver:
	def __init__(self):
		self.sudoku_model = pulp.LpProblem('Sudoku', pulp.LpMinimize)

		var_names = [cell_name(i, j, k)
					 for i in range(9)
					 for j in range(9)
					 for k in range(9)]

		# Creates all cells
		self.vars = pulp.LpVariable.dict('%s',
										 var_names,
										 lowBound=0,
										 upBound=1,
										 cat=pulp.LpInteger)

		# Ensures all rows contain all numbers
		for i in range(9):
			for k in range(9):
				self.sudoku_model += sum([self.vars[cell_name(i, j, k)]
										  for j in range(9)]) == 1

		# Ensures all columns contain all numbers
		for j in range(9):
			for k in range(9):
				self.sudoku_model += sum([self.vars[cell_name(i, j, k)]
										  for i in range(9)]) == 1

		# Ensures all boxes contain all numbers
		for i in range(3):
			for j in range(3):

				i_low = i * 3
				j_low = j * 3
				block_i_values = range(i_low, i_low + 3)
				block_j_values = range(j_low, j_low + 3)

				for k in range(9):
					self.sudoku_model += sum([self.vars[cell_name(i, j, k)]
											  for i in block_i_values
											  for j in block_j_values]) == 1

		# Ensures all cells are filled on the board
		for i in range(9):
			for j in range(9):
				self.sudoku_model += sum([self.vars[cell_name(i, j, k)]
										  for k in range(9)]) == 1

	# Reads the board from file and gives an initial print
	def initialize_board(self, content, output=True):
		# Takes care of trailing newline at end of file
		content = content[:-1] if content[-1:] is '' else content

		for i in range(9):
			for j in range(9):
				k = int(content[i][j])
				if k != 0:
					self.set_cell_value(i, j, k - 1)

				if output:
					v1 = str(k) if k is not 0 else ' '
					s1 = ' ' if j is not 8 else ''
					s2 = '|' if (j + 1) % 3 is 0 and j < 8 else ''
					print(f'{v1}{s1}{s2}', end='')

			if output:
				print()

				if (i + 1) % 3 is 0 and i < 8:
					print('-' * 19)

	# Sets a cell value to 1
	def set_cell_value(self, i, j, v):
		if self.sudoku_model.status != pulp.LpStatusNotSolved:
			raise RuntimeError('Puzzle has already been solved.')

		self.sudoku_model += self.vars[cell_name(i, j, v)] == 1

	# Gets the value of a cell
	def get_cell_value(self, i, j):
		for k in range(9):
			if self.vars[cell_name(i, j, k)].value() == 1:
				return k
		return None

	# Prints the board, this can only be done once the sudoku board is solved
	def print_board(self):
		for i in range(9):
			for j in range(9):
				k = self.get_cell_value(i, j)

				s1 = ' ' if j is not 8 else ''
				s2 = '|' if (j + 1) % 3 is 0 and j < 8 else ''
				print(f'{str(k + 1)}{s1}{s2}', end='')
			print()

			if (i + 1) % 3 is 0 and i < 8:
				print('-' * 19)

	def get_txt(self):
		content = ''
		for i in range(9):
			for j in range(9):
				k = self.get_cell_value(i, j)
				v = '0' if not k and k != 0 else str(k + 1)
				content += v
			content += '\n'

		return content

	# Solves the board
	def solve(self):
		status = self.sudoku_model.solve()

		return status == pulp.LpStatusOptimal


if __name__ == '__main__':
	board = Solver()

	board_name = input('Board name: ')

	with open(f'boards/{board_name}.txt', 'r') as f:
		content = f.read().split('\n')

	board.initialize_board(content)

	print('\nSolving board...\n')

	start_time = time.time()
	if not board.solve():
		print('Sudoku puzzle is not valid.')

	board.print_board()

	print('\n--- %s seconds ---' % (time.time() - start_time))
