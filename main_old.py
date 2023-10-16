import chess
import random
from math import inf

board = chess.Board()

pawnValue = 100
knightValue = 300
bishopValue = 300
rookValue = 500
queenValue = 900

def evaluate(board):
	fen = board.fen().split(' ')[0]

	whiteEval = (fen.count('P')*pawnValue) + (fen.count('N')*knightValue) + (fen.count('B')*bishopValue) + (fen.count('R')*rookValue) + (fen.count('Q')*queenValue)
	blackEval = (fen.count('p')*pawnValue) + (fen.count('n')*knightValue) + (fen.count('b')*bishopValue) + (fen.count('r')*rookValue) + (fen.count('q')*queenValue)

	evaluation = whiteEval - blackEval

	perspective = 1 if board.turn == chess.WHITE else -1
	
	return evaluation * perspective

def minimax(board, depth):
	if depth == 0:
		return evaluate(board)

	moves = list(board.legal_moves)

	if len(moves) == 0:
		if board.is_check():
			return -inf
		return 0

	best_evaluation = -inf

	for move in moves:
		board.push_san(str(move))
		evaluation = -minimax(board, depth-1)
		best_evaluation = max(evaluation, best_evaluation)
		board.pop()
	
	return best_evaluation

while(True):
	move = input("Move: ")
		
	board.push_san(move)
	print(evaluate(board))
	
	print(board)

