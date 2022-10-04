import pygame
import display as disp
import core_gameplay as gp
import game as game
import os.path
import copy
import math
import random
import numpy as np

from os.path import exists as file_exists

from core_gameplay import DRAW, NO_MARKER, PLAYER0_MARKER, PLAYER1_MARKER, NO_LOCAL_BOARD, MARKERS, BAD_MOVE_I_WIN, BAD_MOVE_I_LOST, BAD_MOVE_DRAW, WIN_INDEXES 

# when our turn: root node is current board position (opponents last move)
# we need initial call to our minimax function from our starting pos
def team_player(moves, main_board, local_board_num, my_symbol, opponent_symbol):
    
    # initial states of player
    move_selected = False
    move = -1

    # default values for minimax
    maximizing = True # set to false if we are trying to minimize our hueristic
    depth = 3 # initial search depth
    alpha = -math.inf
    beta = math.inf

    # determine next move using minimax
    while not move_selected:
        # create copy of
        current_moves = copy.copy(moves)
        current_board = copy.copy(main_board)
        current_local_board_num = copy.copy(local_board_num)
        current_my_symbol = copy.copy(my_symbol)
        current_opponent_symbol = copy.copy(opponent_symbol)
        current_player = current_my_symbol
        #current_board_wins = copy.copy(game.Game.main_board_wins)

        # evaluate minimax fn for all possible moves from this point
        # compare the scores pick the best
        my_move = -1
        best_score = -math.inf
        for move in moves:
            new_board = apply_move(move, current_board, current_local_board_num, current_player)
            # switch current player after move is applied to board
            if current_player == 1:
                current_player = 2
            else:
                current_player = 1

            # decides new local board num for opponent
            new_local_board_num = global_to_local(move)
            # recursive call for each child board
            eval = minimax(new_board, new_local_board_num, current_player, depth-1, alpha, beta, True)
            if eval > best_score:
                best_score = eval
                my_move = move
        
        # if the move we chose was valid, send it!
        if my_move in moves:
            move_selected = True

    # return our optimal move
    return move

# def minimax(pos, depth, alpha, beta, maximizingPlayer)
def minimax(current_board, current_local_board_num, current_player, depth, alpha, beta, maximizing):
    
    # can_move_in_won_board is set to false
    # get all of the possible moves from current board 
    current_possible_moves = valid_moves(current_board, current_local_board_num, False)

    print("--------------------------------------------------------")
    print("possible moves: " + str(current_possible_moves) + " count: " + str(len(current_possible_moves)))
    print("--------------------------------------------------------")

    # check if current board is a terminal state (no possible moves from current board)
    # evaluate and return hueristic val only at terminal state
    if depth == 0 or len(current_possible_moves) < 1:
        out = random.randint(1,100)
        print(out)
        return out
            
    if maximizing:
        max_eval = -math.inf
        
        # create new board for each applied move
        for move in current_possible_moves:

            new_board = apply_move(move, current_board, current_local_board_num, current_player)
            
            # switch current player after move is applied to board
            if current_player == 1:
                current_player = 2
            else:
                current_player = 1

            # decides new local board num for opponent
            print("--------------------------------------------------------")
            print(new_board)
            print("applyied move: " + str(move))
            new_local_board_num = global_to_local(move)
            print("opponents new target local board: " + str(new_local_board_num))
            print("--------------------------------------------------------")

            # recursive call for each child board (need to specify current player)
            eval = minimax(new_board, new_local_board_num, current_player, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            if beta <= alpha:
                break
        return max_eval
    # if minimizing    
    else:
        min_eval = math.inf

        # create new board for each applied move
        for move in current_possible_moves:
            new_board = apply_move(move, current_board, current_local_board_num, current_player)

            # switch current player after move is applied to board
            if current_player == 1:
                current_player = 2
            else:
                current_player = 1

            # decides new local board num for opponent
            new_local_board_num = global_to_local(move)

            # recursive call for each child board
            eval = minimax(new_board, new_local_board_num, current_player, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            if beta <= alpha:
                break
        return min_eval

# create copy of current board and apply a give move
def apply_move(move, current_board, current_local_board_num, current_symbol):
    new_board = copy.copy(current_board)
    new_board[current_local_board_num][move % 9] = current_symbol
    return new_board

#execute_move(board_state , move)
def execute_move(current_board, move, marker, board_state_wins):
    new_board = current_board.copy()
    new_board_wins = board_state_wins.copy()
    handle_mark_big_board(new_board, move, marker, new_board_wins)
    return new_board

# FUNCTIONAL
# Converts a global square number (0-80) to a local
# pair containing [local_square_number, board_number]
def global_to_local(g):
    lb_num = int(np.floor(g / 9))
    l = g - lb_num * 9
    return lb_num

# FUNCTIONAL
# Converts a local pair containing [local_square_number, board_number]
# to a global location 0-80
def local_to_global(l):
    return l[0] + 9 * l[1]

# Returns the winner marker of the board
def check_3x3_win(board):
    for indexes in WIN_INDEXES:
        if board[indexes[0]] == board[indexes[1]] and \
                board[indexes[1]] == board[indexes[2]] and \
                board[indexes[0]] != NO_MARKER:
            return board[indexes[0]]

    # If no one has won but the board is full, is draw
    if NO_MARKER not in board:
        return DRAW
    return NO_MARKER

# Gets the valid moves based on the global board state and
# the currently active board
def valid_moves(big_board, current_local, can_move_in_won_board):
    moves = []
    if current_local == NO_LOCAL_BOARD:
        for i in range(0, 9):
            moves = moves + valid_moves_3x3_global(big_board[i], i, can_move_in_won_board)
    else:
        moves = valid_moves_3x3_global(big_board[current_local], current_local, can_move_in_won_board)
    return moves


# Returns the valid moves of a 3x3 board converted to global numbers
def valid_moves_3x3_global(board, board_number, can_move_in_won_board):
    l_moves = valid_moves_3x3(board, can_move_in_won_board)
    moves = []
    for move in l_moves:
        moves.append(local_to_global([move, board_number]))
    return moves


# Returns the playable moves on a basic 3x3 board
def valid_moves_3x3(board, can_move_in_won_board):
    moves = []

    # There are no valid moves on a won board
    if not can_move_in_won_board:
        if check_3x3_win(board):
            return moves

    for i in range(0, 9):
        val = board[i]
        if val == NO_MARKER:
            moves.append(i)
    return moves
