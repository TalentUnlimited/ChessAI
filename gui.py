import pygame
import math
from main import *

pygame.init()

running = True

WIDTH = 500
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))

LEFT = 1
RIGHT = 3

move = ""

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == LEFT:
				file, rank = math.floor(pygame.mouse.get_pos()[0]/(WIDTH/8)), math.floor(pygame.mouse.get_pos()[1]/(HEIGHT/8))
				
				square = f"{chr(97+file)}{chr(49+(7-rank))}"

				if len(move) == 0:
					move += square
				elif len(move) == 2:
					pseudo_move = move + square
					if (square != move) and chess.Move.from_uci(pseudo_move) in board.legal_moves:
						move += square
						makeMove(move)
						if len(list(board.legal_moves)) != 0:
							makeComputerMove(4)
						move = ""
					else:
						print(f"invalid move - {pseudo_move} is not possible")
						move = ""

	def makeMove(move):
		board.push_san(move)
		renderBoard()

	def makeComputerMove(depth):	
		move, _ = alphabeta(board, depth, -infinity, infinity)
		board.push_san(str(move))
		renderBoard()

	def renderBoard():
		win.fill((255,255,255))
		for y in range(9):
			for x in range(9):
				if (x+y) % 2 == 0:
					pygame.draw.rect(win,(234, 233, 210),pygame.Rect(x*(WIDTH/8),y*(HEIGHT/8),WIDTH/8,HEIGHT/8))
				else:
					pygame.draw.rect(win,(75, 115, 153),pygame.Rect(x*(WIDTH/8),y*(HEIGHT/8),WIDTH/8,HEIGHT/8))

		board_matrix = []
		for rank in board.fen().split('/'):
			row = []
			for character in rank:
				if len(row) >= 8:
					continue
				if character.isdigit():
					for x in range(int(character)):
						row.append(' ')
				else:
					if character.isupper():
						row.append(f"{character.lower()}_")
					else:
						row.append(character)
			
			board_matrix.append(row)
		
			
		for y in range(8):
			for x in range(8):
				if board_matrix[y][x] != ' ':
					i = pygame.transform.scale(pygame.image.load(f"D:/ChessAI/Chess Pieces/{board_matrix[y][x]}.png"),(int(WIDTH/8), int(HEIGHT/8)))
					win.blit(i, (x*(WIDTH/8),y*(HEIGHT/8)))
		
		pygame.display.update()

	renderBoard()