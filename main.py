import chess
import numpy
import math

board = chess.Board()

piece_values = {
	chess.PAWN: 100,
	chess.KNIGHT: 300,
	chess.BISHOP: 300,
	chess.ROOK: 500,
	chess.QUEEN: 900,
	chess.KING: 20000
}

infinity = math.inf

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
	#master_board_value_matrix = numpy.array([[0]*8]*8)
	colorwise_value_matrix = [numpy.array([[0]*8]*8), numpy.array([[0]*8]*8)]

	for color in [chess.WHITE, chess.BLACK]:
		for piece in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
			piece_map = numpy.flipud(numpy.array(board.pieces(piece_type=piece, color=color).tolist()).reshape(8,8))
			piece_square_table_map = piece_map * (piece_square_tables[piece] if color == chess.WHITE else numpy.flip(piece_square_tables[piece]))
			piece_value_map = piece_map * piece_values[piece]

			#master_board_value_matrix += (piece_square_table_map + piece_value_map)
			colorwise_value_matrix[0 if color == chess.WHITE else 1] += (piece_square_table_map + piece_value_map)

	# print(master_board_value_matrix)
	# print(colorwise_value_matrix[0])
	# print(colorwise_value_matrix[1])

	whiteEval = colorwise_value_matrix[0].sum()
	blackEval = colorwise_value_matrix[1].sum()

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
