from solve import Solver
import pulp
import numpy as np

# 1 - 3 difficulties
DIFFICULTY = 3

REMOVE = DIFFICULTY * 20

class Generator:
	def __init__(self):
		self.board = np.zeros((9, 9), dtype=int)

	def generate(self):
		self.seed()

		content = self.get_txt().split('\n')

		solver = Solver()
		solver.initialize_board(content, False)
		res = solver.solve()

		if not res:
			return

		self.set_board(solver.get_txt())
		self.de_solve()
		self.print_board()

		# Sets the board to a given content string
	def set_board(self, content):
		i = 0
		content = content.split('\n')

		for line in content:
			j = 0
			int_line = [int(x) for x in line]

			for x in int_line:
				self.board[i, j] = x
				j += 1

			i += 1

	# Removes certain items on the board to get an incompleted board
	def de_solve(self):
		for i in range(REMOVE):
			original = self.board.copy()

			pos = (np.random.randint(0, 9), np.random.randint(0, 9))

			while self.board[pos[0], pos[1]] == 0:
				pos = (np.random.randint(0, 9), np.random.randint(0, 9))

			self.board[pos[0], pos[1]] = 0

	# Creates a "seed" for the board
	def seed(self):
		options = list(range(1, 10))
		np.random.shuffle(options)

		for i, option in enumerate(options):
			box_i = (i // 3) * 3
			box_j = (i % 3) * 3

			p_i = np.random.randint(box_i, box_i + 3)
			p_j = np.random.randint(box_j, box_j + 3)

			self.board[p_i, p_j] = option

		# Total possibles different seeds:
		# 9! (different orders of options) * 9 (possible spots in a box) =
		# 3,265,920 seeds

	def print_board(self):
		for i in range(9):
			for j in range(9):
				k = self.board[i, j]

				v = ' ' if not k else str(k)
				s1 = ' ' if j is not 8 else ''
				s2 = '|' if (j + 1) % 3 is 0 and j < 8 else ''
				print(f'{v}{s1}{s2}', end='')
			print()

			if (i + 1) % 3 is 0 and i < 8:
				print('-' * 19)

	def get_txt(self):
		content = ''
		for i in range(9):
			for j in range(9):
				k = self.board[i, j]
				v = '0' if not k else str(k)
				content += v
			content += '\n'

		return content

if __name__ == "__main__":

	DIFFICULTY = int(input('Difficulty level (1-5): '))
	REMOVE = DIFFICULTY * 15

	gen = Generator()

	gen.generate()

	with open('./boards/gen.txt', 'w') as f:
		f.write(gen.get_txt())
