from copy import deepcopy
import time

class Node:

	def __init__(self, x, y, value):
		self.x = x
		self.y = y
		self.value = value

	def getColumn(self, board):
		column = []
		for i in range(9):
			column.append(board[i][self.x])
		return(column)

	def getRow(self, board):
		return(board[self.y])

	def setValue(self, newValue):
		self.value = newValue

	def __repr__(self):
		return(str(self.value))

	def __str__(self):
		return(str(self.value))

##region BoardFunctions
def printBoard(chart):
	print('\n')

	board = deepcopy(chart)

	for i in range(9):
		for j in range(9):
			board[i][j] = str(board[i][j])
	for i in range(9):
		printline = '  '.join([' '.join(board[i][0:3]), ' '.join(board[i][3:6]), ' '.join(board[i][6:9])])
		printline = printline.replace('0', ' ')
		print(printline)

		if ((i + 1) % 3 == 0):
			print('')

def getBox(board, num):
	num *= 3
	box = []
	x = (num // 9) * 3

	for i in range(3):
		box.append(board[x+i][num % 9:num % 9 + 3])
	return(box)

def listIncludes(line, num):
	for i in line:
		if (i.value == num):
			return(True)
	return(False)

def countNode(container, num):
	counter = 0
	for item in container:
		if (item.value == num):
			counter += 1

	return(counter)

def boardFull(board):
	for i in range(9):
		for item in board[i]:
			if (item.value == 0):
				return(False)
	return(True)

def checkErrors(board):
	for i in range(9):
		for j in range(1, 10):
			if (countNode(board[i], j) > 1):
				return(True)

		for j in range(1, 10):
			if (countNode(board[0][i].getColumn(board), j) > 1):
				return(True)

	return(False)

def checkBoard(board):
	errors = checkErrors(board)
	if (not errors):
		for i in range(9):
			for j in range(9):
				if (board[i][j].value == 0):
					return(False)
		return(True)
	else:
		return(False)

def countZero(board):
	totalCount = 0

	for i in range(9):
		totalCount += countNode(board[i], 0)

	return(totalCount)

##endregion

##region SolveTechniques
def fill(board):
	code = 1

	for i in range(1, 10):
		for j in range(9):
			impossible = False
			possibles = []
			box = getBox(board, j)
			for a in range(3):
				for b in range(3):
					if (box[a][b].value == 0):
						if (not listIncludes(box[a][b].getColumn(board), i)):
							if (not listIncludes(box[a][b].getRow(board), i)):
								possibles.append(box[a][b])
					elif (box[a][b].value == i):
						impossible = True

			if (not impossible):
				if ((len(possibles) > 1)):
					pass
				elif ((len(possibles) == 0)):
					code = 2
				else:
					possibles[0].setValue(i)
					code = 0
	return (board, code)

def lineComplete(board):
	code = 1

	for i in range(9):
		zeroCount = 0
		for item in board[i]:
			if (item.value == 0):
				zeroCount += 1

		if (zeroCount == 1):
			possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
			for j in range(len(board[i])):
				if (board[i][j].value != 0):
					possibles.remove(board[i][j].value)
				else:
					zeroSet = j

			board[i][zeroSet].setValue(possibles[0])
			NO_CHANGE = False

	for i in range(9):
		column = board[0][i].getColumn(board)
		zeroCount = 0
		for item in column:
			if (item.value == 0):
				zeroCount += 1

		if (zeroCount == 1):
			possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
			for j in range(len(column)):
				if (column[j].value != 0):
					possibles.remove(column[j].value)
				else:
					zeroSet = j

			board[zeroSet][i].setValue(possibles[0])
			code = 0

	return (board, code)

##endregion

##region SuperFill
def superFill(board):

	NO_CHANGE = True
	for i in range(1, 10):
		allPossibles = []

		for j in range(9):
			impossible = False
			possibles = []
			box = getBox(board, j)
			for a in range(3):
				for b in range(3):
					if (box[a][b].value == 0):
						if (not listIncludes(box[a][b].getColumn(board), i)):
							if (not listIncludes(box[a][b].getRow(board), i)):
								possibles.append(box[a][b])
					elif (box[a][b].value == i):
						impossible = True
			if impossible:
				possibles = []

			allPossibles.append(possibles)

		for j in range(9):
			selfBox = allPossibles[j]

			rows = []
			for num in getRowBoxes(j):
				rows.append(allPossibles[num])

			cols = []
			for num in getColBoxes(j):
				cols.append(allPossibles[num])

			for rowBox in rows:
				if checkSingleRow(rowBox):
					newPossibles = []
					for selfPossible in selfBox:
						if selfPossible.y != rowBox[0].y:
							newPossibles.append(selfPossible)
					selfBox = newPossibles

			for colBox in cols:
				if checkSingleCol(colBox):
					newPossibles = []
					for selfPossible in selfBox:
						if selfPossible.x != colBox[0].x:
							newPossibles.append(selfPossible)
					selfBox = newPossibles

			if (len(selfBox) == 1):
				selfBox[0].setValue(i)
				NO_CHANGE = False
	return (board, NO_CHANGE)

def getRowBoxes(num):
	boxes = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
	for row in boxes:
		if num in row:
			row.remove(num)
			return(row)

def getColBoxes(num):
	boxes = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
	for col in boxes:
		if num in col:
			col.remove(num)
			return(col)

def checkSingleRow(possibles):
	if (len(possibles) > 0):
		yVal = possibles[0].y
		for possible in possibles:
			if (possible.y != yVal):
				return(False)
		return(True)
	else:
		return(False)

def checkSingleCol(possibles):
	if (len(possibles) > 0):
		xVal = possibles[0].x
		for possible in possibles:
			if (possible.x != xVal):
				return(False)
		return(True)
	else:
		return(False)
##endregion

##region RecursiveGuessing
def findChoice(board):
	emptySpots = []
	for i in range(9):
		counter = 0
		index = i
		box = getBox(board, i)
		for a in range(3):
			for b in range(3):
				if (box[a][b].value == 0):
					counter += 1
		if (counter == 0):
			counter = 10
		emptySpots.append(counter)

	i = emptySpots.index(min(emptySpots))

	box = getBox(board, i)
	possibilities = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	counter = 0
	for a in range(3):
		for b in range(3):
			if (box[a][b].value == 0):
				zeroNode = (box[a][b].y, box[a][b].x)
			else:
				possibilities.remove(box[a][b].value)

	return (zeroNode, possibilities)

def solve(board):
	while (not boardFull(board)):
		board, res = fill(board)
		if (res == 1):
			board, res = lineComplete(board)
			if (res == 1):
				board, res = superFill(board)
				if (res == 1):
					saveBoard = deepcopy(board)
					coord, opts = findChoice(saveBoard)

					isSolved = False
					for i in range(len(opts)):
						if (not isSolved):
							if (not listIncludes(saveBoard[coord[0]][coord[1]].getColumn(saveBoard), opts[i])):
								if (not listIncludes(saveBoard[coord[0]][coord[1]].getRow(saveBoard), opts[i])):
									saveBoard[coord[0]][coord[1]].setValue(opts[i])

									res = solve(deepcopy(saveBoard))

									if (type(res) == int):
										if (i + 1 == len(opts)):
											return(1)
										else:
											saveBoard[coord[0]][coord[1]].setValue(0)
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
##endregion

def main():
	boardToRun = input('Which board would you like to solve? (Must be corresponding to file name): ')

	start_time = time.time()

	with open('./boards/'+boardToRun+'.txt', 'r') as f:
		content = f.read()
		board = [[int(x) for x in list(row)] for row in content.split('\n')[:-1]]

	for i in range(9):
		for j in range(9):
			board[i][j] = Node(j, i, board[i][j])

	printBoard(board)

	board = solve(board)

	printBoard(board)

	print('BOARD SOLVED:', checkBoard(board))

	print('\n--- %s seconds ---' % (time.time() - start_time))

if __name__ == '__main__':
	main()
