import chess
import chess.polyglot
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
	chess.PAWN: [
		[0,  0,  0,  0,  0,  0,  0,  0],
		[50, 50, 50, 50, 50, 50, 50, 50],
		[10, 10, 20, 30, 30, 20, 10, 10],
		[5,  5, 10, 25, 25, 10,  5,  5],
		[0,  0,  0, 20, 20,  0,  0,  0],
		[5, -5,-10,  0,  0,-10, -5,  5],
		[5, 10, 10,-20,-20, 10, 10,  5],
		[0,  0,  0,  0,  0,  0,  0,  0]
	],
	chess.KNIGHT: [
		[-50,-40,-30,-30,-30,-30,-40,-50],
		[-40,-20,  0,  0,  0,  0,-20,-40],
		[-30,  0, 10, 15, 15, 10,  0,-30],
		[-30,  5, 15, 20, 20, 15,  5,-30],
		[-30,  0, 15, 20, 20, 15,  0,-30],
		[-30,  5, 10, 15, 15, 10,  5,-30],
		[-40,-20,  0,  5,  5,  0,-20,-40],
		[-50,-40,-30,-30,-30,-30,-40,-50]
	],
	chess.BISHOP: [
		[-20,-10,-10,-10,-10,-10,-10,-20],
		[-10,  0,  0,  0,  0,  0,  0,-10],
		[-10,  0,  5, 10, 10,  5,  0,-10],
		[-10,  5,  5, 10, 10,  5,  5,-10],
		[-10,  0, 10, 10, 10, 10,  0,-10],
		[-10, 10, 10, 10, 10, 10, 10,-10],
		[-10,  5,  0,  0,  0,  0,  5,-10],
		[-20,-10,-10,-10,-10,-10,-10,-20]
	],
	chess.ROOK: [
		[0,  0,  0,  0,  0,  0,  0,  0],
		[5, 10, 10, 10, 10, 10, 10,  5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[-5,  0,  0,  0,  0,  0,  0, -5],
		[0,  0,  0,  5,  5,  0,  0,  0]
	],
	chess.QUEEN: [
		[-20,-10,-10, -5, -5,-10,-10,-20],
		[-10,  0,  0,  0,  0,  0,  0,-10],
		[-10,  0,  5,  5,  5,  5,  0,-10],
		[-5,  0,  5,  5,  5,  5,  0, -5],
		[0,  0,  5,  5,  5,  5,  0, -5],
		[-10,  5,  5,  5,  5,  5,  0,-10],
		[-10,  0,  5,  0,  0,  0,  0,-10],
		[-20,-10,-10, -5, -5,-10,-10,-20]
	],
	chess.KING: [
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

def alphabeta(board, depth, alpha, beta, maximizingPlayer, transpositions):
	if depth == 0:
		return evaluate(board)
	
	if len(list(board.legal_moves)) == 0:
		if board.is_check:
			return -infinity
		return 0

	if maximizingPlayer:
		maxEval = -infinity
		moves = list(board.legal_moves)
		moves = ordermoves(moves)

		for move in moves:
			board.push_san(str(move))

			zobrist_hash = chess.polyglot.zobrist_hash(board)
			if zobrist_hash in transpositions:
				evaluation = transpositions[zobrist_hash]
			else:
				evaluation = alphabeta(board, depth-1, alpha, beta, False, transpositions)
				transpositions[zobrist_hash] = evaluation
			maxEval = max(maxEval, evaluation)
			alpha = max(alpha, evaluation)
			board.pop()
			if beta <= alpha:
				break
		
		return maxEval
	else:
		minEval = infinity
		moves = list(board.legal_moves)
		moves = ordermoves(moves)

		for move in moves:
			board.push_san(str(move))
			
			zobrist_hash = chess.polyglot.zobrist_hash(board)
			if zobrist_hash in transpositions:
				evaluation = transpositions[zobrist_hash]
			else:
				evaluation = alphabeta(board, depth-1, alpha, beta, False, transpositions)
				transpositions[zobrist_hash] = evaluation
			minEval = min(minEval, evaluation)
			beta = min(beta, evaluation)
			board.pop()
			if beta <= alpha:
				break
		
		return minEval

def alphabetaRoot(board, depth):
	moves = list(board.legal_moves)
	moves = ordermoves(moves)

	best_evaluation = -infinity
	best_move = None

	transpositions = {}

	for move in moves:
		board.push_san(str(move))
		#print(move, '\n', board)
		evaluation = alphabeta(board, depth-1, -infinity, infinity, board.turn, transpositions)

		board.pop()

		if evaluation > best_evaluation:
			best_evaluation = evaluation
			best_move = move
	
	return best_move

def ordermoves(moves):
	moveScores = []

	for move in moves:
		moveScoreGuess = 0
		movingPiece = board.piece_at(move.from_square)
		capturingPiece = board.piece_at(move.to_square)

		if capturingPiece != None:
			moveScoreGuess = 10 * piece_values[capturingPiece.piece_type] - piece_values[movingPiece.piece_type]

		if move.promotion != None:
			moveScoreGuess += piece_values[move.promotion]
		
		moveScores.append(moveScoreGuess)

	moveScoresDict = dict(zip(moves, moveScores)) 
	
	return list(dict(sorted(moveScoresDict.items(), key=lambda item: item[1], reverse=True)).keys())

#board = chess.Board(fen='rnbqkb1r/pppp1pp1/4pn1p/6B1/3PP3/8/PPP2PPP/RN1QKBNR w KQkq - 0 4')


# for x in range(50):
# 	move1 = alphabetaRoot(board, 3)
# 	board.push_san(str(move1))
# 	move2 = alphabetaRoot(board, 3)
# 	board.push_san(str(move2))

# 	print(f'{x+1}. {move1} {move2}')
