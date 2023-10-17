import chess
import numpy

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

def negamax(board, depth):
	if depth == 0:
		return evaluate(board)

	moves = list(board.legal_moves)

	best_evaluation = -999
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
			return -999
		return 0

	if maximizingPlayer:
		maxEval = -999
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
		minEval = 999
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

	best_evaluation = -999
	best_move = None

	for move in moves:
		board.push_san(str(move))
		#print(move, '\n', board)
		evaluation = alphabeta(board, depth-1, -999, 999, board.turn)

		board.pop()

		if evaluation > best_evaluation:
			best_evaluation = evaluation
			best_move = move
	
	return best_move

def ordermoves(moves):
	pass

board = chess.Board(fen='rnbqkb1r/pppp1pp1/4pn1p/6B1/3PP3/8/PPP2PPP/RN1QKBNR w KQkq - 0 4')


print(alphabetaRoot(board, 5))
