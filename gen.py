import random

# 1 - 5 difficulties
DIFFICULTY = 1

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

def checkBoard(board):
	for i in range(len(board)):
		for j in range(9):
			if (countNode(board[i], j+1) != 1):
				return(False)

		for j in range(9):
			if (countNode(board[0][i].getColumn(board), j+1) != 1):
				return(False)

	return(True)

def countNode(container, num):
	counter = 0
	for item in container:
		if (item.value == num):
			counter += 1

	return(counter)

def shuffle(board):
	global DIFFICULTY
	i = 0
	while i < (DIFFICULTY * 20):
		a = random.randint(0, 8)
		b = random.randint(0, 8)
		if (board[a][b].value != 0):
			board[a][b].setValue(0)
			i += 1
	return(board)

def boardRestart(board):
	for i in range(9):
		for j in range(9):
			board[i][j] = Node(j, i, 0)

	return(board)

def boardPrint(board):
	print('\n\n\n')
	for i in range(len(board)):
		print(board[i])

def listIncludes(line, num):
	for i in line:
		if (i.value == num):
			return(True)
	return(False)

def getBox(board, num):
	num *= 3
	box = []
	x = (num // 9) * 3

	for i in range(3):
		box.append(board[x+i][num % 9:num % 9 + 3])
	return(box)

board = []

for i in range(9):
	row = []
	for j in range(9):
		row.append(0)
	board.append(row)

for i in range(9):
	for j in range(9):
		board[i][j] = Node(j, i, 0)

i = 1
while i < 10:
	j = 0
	while j < 9:
		possibles = []
		box = getBox(board, j)
		#print(box)
		for a in range(3):
			for b in range(3):
				if (box[a][b].value == 0):
					if (not listIncludes(box[a][b].getColumn(board), i)):
						if (not listIncludes(box[a][b].getRow(board), i)):
							possibles.append(box[a][b])
		if (len(possibles) == 0):
			boardRestart(board)
			i = 1
			j = 0
		else:
			chosen = random.choice(possibles)
			chosen.setValue(i)

			j += 1

	i += 1

boardPrint(board)
print(checkBoard(board))

board = shuffle(board)

board = [[str(x) for x in row] for row in board]

content = '\n'.join([''.join(row) for row in board])+'\n'

with open('./boards/gen.txt', 'w') as f:
	f.write(content)
