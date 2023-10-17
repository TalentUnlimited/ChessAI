import chess

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

def minimax(board, depth, alpha, beta, maximizingPlayer):
	if depth == 0:
		return evaluate(board)
	
	if maximizingPlayer:
		maxEval = -999
		moves = list(board.legal_moves)

		for move in moves:
			board.push_san(str(move))
			evaluation = minimax(board, depth-1, alpha, beta, False)
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
			evaluation = minimax(board, depth-1, alpha, beta, True)
			minEval = min(minEval, evaluation)
			beta = min(beta, evaluation)
			board.pop()
			if beta <= alpha:
				break
		
		return minEval


print(minimax(chess.Board(fen='3r1rk1/ppp2pp1/3pb2p/6q1/3RP3/P4P2/1PPQB1PP/2K4R w - - 5 16'), 4, -999, 999, True))
print(negamax(chess.Board(fen='3r1rk1/ppp2pp1/3pb2p/6q1/3RP3/P4P2/1PPQB1PP/2K4R w - - 5 16'), 4))
