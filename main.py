import chess
import numpy

board = chess.Board()

pawnValue = 100
knightValue = 300
bishopValue = 300
rookValue = 500
queenValue = 900

piece_square_tables = {
	'pawn': [
		[0,  0,  0,  0,  0,  0,  0,  0],
		[50, 50, 50, 50, 50, 50, 50, 50],
		[10, 10, 20, 30, 30, 20, 10, 10],
		[5,  5, 10, 25, 25, 10,  5,  5],
		[0,  0,  0, 20, 20,  0,  0,  0],
		[5, -5,-10,  0,  0,-10, -5,  5],
		[5, 10, 10,-20,-20, 10, 10,  5],
		[0,  0,  0,  0,  0,  0,  0,  0]
	],
	'knight': [
		[-50,-40,-30,-30,-30,-30,-40,-50],
		[-40,-20,  0,  0,  0,  0,-20,-40],
		[-30,  0, 10, 15, 15, 10,  0,-30],
		[-30,  5, 15, 20, 20, 15,  5,-30],
		[-30,  0, 15, 20, 20, 15,  0,-30],
		[-30,  5, 10, 15, 15, 10,  5,-30],
		[-40,-20,  0,  5,  5,  0,-20,-40],
		[-50,-40,-30,-30,-30,-30,-40,-50]
	],
	'bishop': [
		[-20,-10,-10,-10,-10,-10,-10,-20],
		[-10,  0,  0,  0,  0,  0,  0,-10],
		[-10,  0,  5, 10, 10,  5,  0,-10],
		[-10,  5,  5, 10, 10,  5,  5,-10],
		[-10,  0, 10, 10, 10, 10,  0,-10],
		[-10, 10, 10, 10, 10, 10, 10,-10],
		[-10,  5,  0,  0,  0,  0,  5,-10],
		[-20,-10,-10,-10,-10,-10,-10,-20]
	],
	'rook': [
		[0,  0,  0,  0,  0,  0,  0,  0],
		[5, 10, 10, 10, 10, 10, 10,  5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[0,  0,  0,  5,  5,  0,  0,  0]
	],
	'queen': [
		[-20,-10,-10, -5, -5,-10,-10,-20],
		[-10,  0,  0,  0,  0,  0,  0,-10],
		[-10,  0,  5,  5,  5,  5,  0,-10],
		[-5,  0,  5,  5,  5,  5,  0, -5],
		[0,  0,  5,  5,  5,  5,  0, -5],
		[-10,  5,  5,  5,  5,  5,  0,-10],
		[-10,  0,  5,  0,  0,  0,  0,-10],
		[-20,-10,-10, -5, -5,-10,-10,-20]
	],
	'king': [
		[-30,-40,-40,-50,-50,-40,-40,-30],
		[-30,-40,-40,-50,-50,-40,-40,-30],
		[-30,-40,-40,-50,-50,-40,-40,-30],
		[-30,-40,-40,-50,-50,-40,-40,-30],
		[-20,-30,-30,-40,-40,-30,-30,-20],
		[-10,-20,-20,-20,-20,-20,-20,-10],
		[20, 20,  0,  0,  0,  0, 20, 20],
		[20, 30, 10,  0,  0, 10, 30, 20]
	],
	'king_endgame': [
		[-50,-40,-30,-20,-20,-30,-40,-50],
		[-30,-20,-10,  0,  0,-10,-20,-30],
		[-30,-10, 20, 30, 30, 20,-10,-30],
		[-30,-10, 30, 40, 40, 30,-10,-30],
		[-30,-10, 30, 40, 40, 30,-10,-30],
		[-30,-10, 20, 30, 30, 20,-10,-30],
		[-30,-30,  0,  0,  0,  0,-30,-30],
		[-50,-30,-30,-30,-30,-30,-30,-50]
	]
}

def evaluate(board):
	fen = board.fen().split(' ')[0]

	whiteEval = (fen.count('P')*pawnValue) + (fen.count('N')*knightValue) + (fen.count('B')*bishopValue) + (fen.count('R')*rookValue) + (fen.count('Q')*queenValue)
	blackEval = (fen.count('p')*pawnValue) + (fen.count('n')*knightValue) + (fen.count('b')*bishopValue) + (fen.count('r')*rookValue) + (fen.count('q')*queenValue)

	evaluation = whiteEval - blackEval

	perspective = 1 if board.turn == chess.WHITE else -1
	
	return evaluation * perspective

def negamax(board, depth):
	if depth == 0:
		return evaluate(board)

	moves = list(board.legal_moves)

	best_evaluation = -infinity
	best_move = 0

	for move in moves:
		board.push_san(str(move))
		
		score = -negamax(board, depth-1)
		if score > best_evaluation:
			best_evaluation = score
			best_move = move
		
		board.pop()

	return best_evaluation

def alphabeta(board, depth, alpha, beta, maximizingPlayer):
	if depth == 0:
		return evaluate(board)
	
	if len(list(board.legal_moves)) == 0:
		if board.is_check:
			return -infinity
		return 0

	if maximizingPlayer:
		maxEval = -infinity
		moves = list(board.legal_moves)

		for move in moves:
			board.push_san(str(move))
			evaluation = alphabeta(board, depth-1, alpha, beta, False)
			maxEval = max(maxEval, evaluation)
			alpha = max(alpha, evaluation)
			board.pop()
			if beta <= alpha:
				break
		
		return maxEval
	else:
		minEval = infinity
		moves = list(board.legal_moves)

		for move in moves:
			board.push_san(str(move))
			evaluation = alphabeta(board, depth-1, alpha, beta, True)
			minEval = min(minEval, evaluation)
			beta = min(beta, evaluation)
			board.pop()
			if beta <= alpha:
				break
		
		return minEval

def alphabetaRoot(board, depth):
	moves = list(board.legal_moves)

	best_evaluation = -infinity
	best_move = None

	for move in moves:
		board.push_san(str(move))
		#print(move, '\n', board)
		evaluation = alphabeta(board, depth-1, -infinity, infinity, board.turn)

		board.pop()

		if evaluation > best_evaluation:
			best_evaluation = evaluation
			best_move = move
	
	return best_move

def ordermoves(moves):
	pass

board = chess.Board(fen='rnbqkb1r/pppp1pp1/4pn1p/6B1/3PP3/8/PPP2PPP/RN1QKBNR w KQkq - 0 4')


print(alphabetaRoot(board, 5))
