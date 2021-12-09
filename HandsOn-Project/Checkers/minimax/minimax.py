from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE = (255,255,255)
MAXX = 100000
MINN = -100000

def minimax(position, depth, maxPlayer, game):
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    if maxPlayer:
        max_val = MINN
        max_move = None
        all_moves = getAllMoves(position, WHITE, game)
        for move in all_moves:
            curr_val, dummy = minimax(move, depth - 1, False, game)
            if curr_val > max_val:
                max_val = curr_val
                max_move = move
        return max_val, max_move
    else:
        min_val = MAXX
        min_move = None
        all_moves = getAllMoves(position, RED, game)
        for move in all_moves:
            curr_val, dummy = minimax(move, depth - 1, True, game)
            if curr_val < min_val:
                min_val = curr_val
                min_move = move
        return min_val, min_move

def simulateMove(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board

def getAllMoves(board, color, game):
    moves = []
    pieces = board.getAllPieces(color)
    for piece in pieces:
        all_moves = board.getValidMoves(piece)
        for curr_move, skip in all_moves.items():
            new_board = deepcopy(board)
            new_piece = new_board.getPiece(piece.row, piece.col)
            moves.append(simulateMove(new_piece, curr_move, new_board, game, skip))
    return moves

