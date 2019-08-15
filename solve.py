from copy import deepcopy
import time

def listIncludes(line, searchInteger, giveCount=False):
	if (str(searchInteger) in [str(x) for x in line]):
		if (giveCount):
			return(True, [str(x) for x in line].count(str(searchInteger)))
		else:
			return(True)
	else:
		if (giveCount):
			return(False, 0)
		else:
			return(False)

def getAdjacentBoxes(num, dir):
	if (dir == 'horizontal'):
		boxes = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
	elif (dir == 'vertical'):
		boxes = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
	for row in boxes:
		if num in row:
			row.remove(num)
			return(row)

def checkSingle(possibles, dir):
	if (len(possibles) > 0):
		if (dir == 'horizontal'): val = possibles[0].i
		elif (dir == 'vertical'): val = possibles[0].j
		for possible in possibles:
			if (dir == 'horizontal' and possible.i != val):
				return(False)
			elif (dir == 'vertical' and possible.j != val):
				return(False)
		return(True)
	else:
		return(False)

class Board:
	def __init__(self, dataSet):
		self.board = dataSet

	def getBox(self, boxNum):
		boxNum *= 3
		box = []
		x = (boxNum // 9) * 3

		for i in range(3):
			box.append(self.board[x+i][boxNum % 9:boxNum % 9 + 3])
		return(box)

	def getColumn(self, columnNumber):
		column = []
		for i in range(9):
			column.append(self.board[i][columnNumber])
		return(column)

	def getRow(self, rowNumber):
		return(self.board[rowNumber])

	def checkFull(self):
		for i in range(9):
			if (listIncludes(self.board[i], 0) > 0): return(False)
		return(True)

	def checkBoard(self):
		for i in range(9):
			if (listIncludes(self.board[i], 0, True)[1] > 0):
				return(False)

			for j in range(1, 10):
				if (listIncludes(self.board[i], j, True)[1] > 1):
					return(False)

			for j in range(1, 10):
				if (listIncludes(self.getColumn(i), j, True)[1] > 1):
					return(False)

		return(True)

	def fill(self):
		code = 1

		for i in range(1, 10):
			for j in range(9):
				impossible = False
				possibles = []
				box = self.getBox(j)
				for a in range(3):
					for b in range(3):
						if (box[a][b].value == 0):
							if ((not listIncludes(self.getColumn(box[a][b].j), i)) and (not listIncludes(self.getRow(box[a][b].i), i))):
								possibles.append(box[a][b])
						elif (box[a][b].value == i): impossible = True

				if (not impossible):
					if ((len(possibles) > 1)):
						pass
					elif ((len(possibles) == 0)):
						code = 2
						return(code)
					else:
						possibles[0].setValue(i)
						code = 0
		return(code)

	def completeLines(self):
		code = 1

		for i in range(9):
			absentColumn = []
			columnIndex = 0

			absentRow = []
			rowIndex = 0
			for j in range(1, 10):
				if j not in [str(x) for x in self.getColumn(i)]:
					absentColumn.append(j)

				if (self.getColumn(i)[j - 1].value == 0):
					columnIndex = j - 1

				if j not in [str(x) for x in self.getRow(i)]:
					absentRow.append(j)

				if (self.getRow(i)[j - 1].value == 0):
					rowIndex = j - 1

			if (len(absentColumn) == 1):
				self.getRow(i)[columnIndex].setValue(absentColumn[0])

			if (len(absentRow) == 1):
				self.getRow(i)[rowIndex].setValue(absentRow[0])

		return(code)

	def superFill(self):

		code = 1

		for i in range(1, 10):
			allPossibles = []

			for j in range(9):
				impossible = False
				possibles = []
				box = self.getBox(j)
				for a in range(3):
					for b in range(3):
						if (box[a][b].value == 0):
							if (not listIncludes(self.getColumn(box[a][b].j), i)):
								if (not listIncludes(self.getRow(box[a][b].i), i)):
									possibles.append(box[a][b])
						elif (box[a][b].value == i):
							impossible = True
				if impossible:
					possibles = []

				allPossibles.append(possibles)

			for j in range(9):
				selfBox = allPossibles[j]

				rows = []
				for num in getAdjacentBoxes(j, 'horizontal'):
					rows.append(allPossibles[num])

				cols = []
				for num in getAdjacentBoxes(j, 'vertical'):
					cols.append(allPossibles[num])

				for rowBox in rows:
					if checkSingle(rowBox, 'horizontal'):
						newPossibles = []
						for selfPossible in selfBox:
							if selfPossible.i != rowBox[0].i:
								newPossibles.append(selfPossible)
						selfBox = newPossibles

				for colBox in cols:
					if checkSingle(colBox, 'vertical'):
						newPossibles = []
						for selfPossible in selfBox:
							if selfPossible.j != colBox[0].j:
								newPossibles.append(selfPossible)
						selfBox = newPossibles

				if (len(selfBox) == 1):
					selfBox[0].setValue(i)
					code = 0
		return(code)

	def print(self):
		print('\n')

		for i in range(9):
			printline = '  '.join([' '.join([str(x) for x in self.board[i][0:3]]), ' '.join([str(x) for x in self.board[i][3:6]]), ' '.join([str(x) for x in self.board[i][6:9]])])
			printline = printline.replace('0', ' ')
			print(printline)

			if ((i + 1) % 3 == 0):
				print('')

class Node:
	def __init__(self, i, j, value):
		self.i = i
		self.j = j
		self.value = value

	def setValue(self, newValue):
		self.value = newValue

	def __repr__(self):
		return(str(self.value))

	def __str__(self):
		return(str(self.value))

def findChoice(grid):
	emptySpots = []
	for i in range(9):
		counter = 0
		index = i
		box = grid.getBox(i)
		for a in range(3):
			for b in range(3):
				if (box[a][b].value == 0):
					counter += 1
		if (counter == 0):
			counter = 10
		emptySpots.append(counter)

	i = emptySpots.index(min(emptySpots))

	box = grid.getBox(i)
	possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	counter = 0
	for a in range(3):
		for b in range(3):
			if (box[a][b].value == 0):
				zeroNode = (box[a][b].i, box[a][b].j)
			else:
				possibilities.remove(box[a][b].value)

	return (zeroNode, possibilities)

def solve(board):
	while (not board.checkFull()):
		res = board.fill()
		if (res == 1):
			res = board.completeLines()
			if (res == 1):
				res = board.superFill()
				if (res == 1):
					saveBoard = deepcopy(board)
					coord, opts = findChoice(saveBoard)

					isSolved = False

					for i in range(len(opts)):
						if (not isSolved):
							if (not listIncludes(saveBoard.getColumn(coord[1]), opts[i])):
								if (not listIncludes(saveBoard.getRow(coord[0]), opts[i])):
									saveBoard.board[coord[0]][coord[1]].setValue(opts[i])

									res = solve(deepcopy(saveBoard))

									if (type(res) == int):
										if (i + 1 == len(opts)):
											return(1)
										else:
											saveBoard = deepcopy(board)
									else:
										board = deepcopy(res)
										isSolved = True
								else:
									pass
							else:
								pass
							if (i + 1 == len(opts)): return(1)
				elif (res == 2):
					return(1)
			elif (res == 2):
				return(1)
		elif (res == 2):
			return(1)

	return(board)

def main():
	boardToRun = input('Which board would you like to solve? (Must be corresponding to file name): ')

	start_time = time.time()

	with open('./boards/'+boardToRun+'.txt', 'r') as f:
		content = f.read()
		grid = [[int(x) for x in list(row)] for row in content.split('\n')[:-1]]

	for i in range(9):
		for j in range(9):
			grid[i][j] = Node(i, j, grid[i][j])

	board = Board(grid)

	board.print()

	board = solve(board)

	if (board == 2):
		print('IMPOSSIBLE')
	else:
		board.print()

		print('BOARD SOLVED:', board.checkBoard())

		print('\n--- %s seconds ---' % (time.time() - start_time))

if __name__ == '__main__':
	main()
