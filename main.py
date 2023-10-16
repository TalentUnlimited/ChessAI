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
		return [0, evaluate(board)]

	moves = list(board.legal_moves)

	best_evaluation = -999
	best_move = 0

	for move in moves:
		board.push_san(str(move))
		
		score = -negamax(board, depth-1)[1]
		if score > best_evaluation:
			best_evaluation = score
			best_move = move
		
		board.pop()

	return [best_move, best_evaluation]

for x in range(50):
	move1 = negamax(board, 3)[0]
	board.push_san(str(move1))
	move2 = negamax(board, 3)[0]
	board.push_san(str(move2))

	print(f'{x+1}. {move1} {move2}')
