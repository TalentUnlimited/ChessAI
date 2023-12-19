import pygame
import math
from main import *

pygame.init()

running = True

WIDTH, HEIGHT = 500, 500
GAP = 10

SQUARE_WIDTH, SQUARE_HEIGHT = WIDTH/8, HEIGHT/8

win = pygame.Surface((WIDTH,HEIGHT))
mainWin = pygame.display.set_mode(((2*WIDTH) + (3*GAP), HEIGHT + (2*GAP)))

background = pygame.image.load("StartMenuImages/background.jpg")
logo = pygame.image.load("StartMenuImages/logo_transparent.png")
challenge = pygame.image.load("StartMenuImages/challenge_resized.png")
learn = pygame.image.load("StartMenuImages/learn_resized.png")


pygame.display.set_caption('Chess AI')

font = pygame.font.SysFont(None, int(WIDTH/20))

LEFT, RIGHT  = 1, 3

move = ""
highlighted = []

skins = {
	'default': [(234, 233, 210), (75, 115, 153)],
	'brown': [(238, 214, 176), (184, 134, 97)],
}

skin = skins['brown']

game_state = 'start_menu'

while running:
	area = pygame.Rect(GAP, GAP, WIDTH, HEIGHT)

	challenge_button_area = pygame.Rect(20, 250, challenge.get_width(), challenge.get_height())
	learn_button_area = pygame.Rect(20, 370, challenge.get_width(), challenge.get_height())


	if game_state == 'start_menu':
		mainWin.blit(background, (0,-100))
		mainWin.blit(logo, (20, 20))
		mainWin.blit(challenge, (20, 250))
		mainWin.blit(learn, (20, 370))


		pygame.display.update()	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEBUTTONUP and game_state == "start_menu":
			if event.button == LEFT:
				if challenge_button_area.collidepoint(event.pos):
					game_state = "play01"
				elif learn_button_area.collidepoint(event.pos):
					game_state = "play02"
		elif event.type == pygame.MOUSEBUTTONUP and game_state.startswith("play"):
			if event.button == LEFT and area.collidepoint(event.pos):
				file, rank = math.floor((pygame.mouse.get_pos()[0] - GAP)/(SQUARE_WIDTH)), math.floor((pygame.mouse.get_pos()[1] - GAP)/(SQUARE_HEIGHT))
				
				square = f"{chr(97+file)}{chr(49+(7-rank))}"

				if len(move) == 0:
					move += square
					updateHighlighted(square)
				elif len(move) == 2:
					if square == move:
						move = ""
						highlighted = []
						continue
					pseudo_move = move + square
					
					chess_pseudo_move = chess.Move.from_uci(pseudo_move)
					if board.piece_at(chess_pseudo_move.from_square) != None:
						if (chess.square_rank(chess_pseudo_move.to_square) == 7 and board.piece_at(chess_pseudo_move.from_square).piece_type == chess.PAWN):
							pseudo_move += "q"
					if chess.Move.from_uci(pseudo_move) in board.legal_moves:
						makeMove(pseudo_move)
						move = ""
						highlighted = []
						renderBoard()
						if len(list(board.legal_moves)) != 0:
							makeComputerMove(4)
					else:
						chess_pseudo_move = chess.Move.from_uci(pseudo_move)
						movingsquare = board.piece_at(chess_pseudo_move.from_square)
						goingsquare = board.piece_at(chess_pseudo_move.to_square)
						if (movingsquare != None and goingsquare != None) and movingsquare.color == goingsquare.color:
							move = square
							highlighted = []
							updateHighlighted(square)
						else:
							move = ""
							highlighted = []
							print(f"invalid move - {pseudo_move} is not possible")	

	def updateHighlighted(square):
		for legal_move in board.legal_moves:
			if legal_move.from_square == chess.parse_square(square):
				highlighted.append(legal_move.to_square)

	def makeMove(move):
		board.push_san(move)
		renderBoard()

	def makeComputerMove(depth):	
		#move, _ = alphabeta(board, depth, -infinity, infinity, {})
		move = best_move(board, depth)
		board.push_san(str(move))
		renderBoard()

	def renderBoard():
		win.fill((255,255,255))
		for y in range(8):
			for x in range(8):
				square = pygame.Rect(x*(SQUARE_WIDTH),y*(SQUARE_HEIGHT),SQUARE_WIDTH,SQUARE_HEIGHT)
				if (x+y) % 2 == 0:
					pygame.draw.rect(win,skin[0],square)
				else:
					pygame.draw.rect(win,skin[1],square)

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
		
		if board.is_check():
			king_square = board.king(chess.WHITE if board.turn == 1 else chess.BLACK)
			if king_square not in highlighted:
				highlighted.append(king_square)
			
		for y in range(8):
			for x in range(8):
				
				if chess.parse_square(f"{chr(97+x)}{8-y}") in highlighted:
					pygame.draw.rect(win,(153, 153, 255),pygame.Rect(x*(SQUARE_WIDTH),y*(SQUARE_HEIGHT),SQUARE_WIDTH,SQUARE_HEIGHT))
				if board_matrix[y][x] != ' ':
					i = pygame.transform.scale(pygame.image.load(f"Chess Pieces/{board_matrix[y][x]}.png"),(int(SQUARE_WIDTH), int(SQUARE_HEIGHT)))
					win.blit(i, (x*(SQUARE_WIDTH),y*(SQUARE_HEIGHT)))

		[win.blit(font.render(chr(97+x), True, skin[0] if x % 2 == 0 else skin[1]), (x*(SQUARE_WIDTH) + WIDTH/10 , HEIGHT - HEIGHT/25)) for x in range(8)]
		[win.blit(font.render(str(8-y), True, skin[1] if y % 2 == 0 else skin[0]), (2, y*(SQUARE_HEIGHT))) for y in range(8)]	
		
		mainWin.blit(background, (0,-100))
		mainWin.blit(win, (GAP,GAP))

		mainWin.blit(win, (WIDTH+(2*GAP), GAP)) if game_state == "play02" else None

		pygame.display.update()

	if game_state.startswith("play"):
		renderBoard()