import pygame
import display as disp
import core_gameplay as gp
import game as game
import os.path
import copy
import math
import random

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
        current_board = copy.copy(main_board)
        current_local_board_num = copy.copy(local_board_num)
        my_symbol_ = copy.copy(my_symbol)
        opponent_symbol_ = copy.copy(opponent_symbol)
        # pass current/root board into minimax.
        move = minimax(current_board, current_local_board_num, my_symbol_, opponent_symbol_, depth, alpha, beta, maximizing)
        if move in moves:
            move_selected = True

    # return our optimal move
    return move


# def minimax(pos, depth, alpha, beta, maximizingPlayer)
# pos is represented by multiple args?
def minimax(current_board, current_local_board_num, board_state_wins, my_symbol_, opponent_symbol_, depth, alpha, beta, maximizing):
    
    # check if current board is a terminal state (if 0 game continues)
    print("-----------")
    print(current_board)
    print("-----------")
    is_terminal_board = check_3x3_win(current_board)

    # evaluate and return hueristic val only at terminal state
    if depth == 0 or is_terminal_board != 0:
        if is_terminal_board == PLAYER0_MARKER and my_symbol_ == PLAYER0_MARKER:
            return 101

        elif is_terminal_board == PLAYER1_MARKER and my_symbol_ == PLAYER1_MARKER:
            return 101
        
        elif is_terminal_board == DRAW:
            return -1
        
        else:
            return randint(1,100)

    if maximizing:
        max_eval = -math.inf
        # can_move_in_won_board is set to false
        # get all of the possible moves from current board 
        possible_moves = valid_moves(current_board, current_local_board_num, False)
        
        # create new board for each applied move
        for move in possible_moves:
            new_board = execute_move(new_board, move, my_symbol_, board_state_wins)
            # recursive call for each child board
            # Todo : pass in new local board number
            eval = minimax(new_board, current_local_board_num, my_symbol_, opponent_symbol_, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            if beta <= alpha:
                break
        return max_eval
    
    else:
        min_eval = math.inf
        # can_move_in_won_board is set to false
        # get all of the possible moves from current board 
        possible_moves = valid_moves(current_board, current_local_board_num, False)

         # create new board for each applied move
        for move in possible_moves:
            new_board = execute_move(new_board, move, my_symbol_, board_state_wins)
            # recursive call for each child board
            # Todo : pass in new local board number
            eval = minimax(new_board, current_local_board_num, my_symbol_, opponent_symbol_, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            if beta <= alpha:
                break
        return min_eval


#execute_move(board_state , move)
def execute_move(current_board, move, marker, board_state_wins):
    new_board = current_board.copy()
    new_board_wins = board_state_wins.copy()
    handle_mark_big_board(new_board, move, marker, new_board_wins)
    return new_board

# The local board numbers are
# 0 1 2
# 3 4 5
# 6 7 8
#
# The global numbers are of the form
# 0 1 2 | 09 10 11 |
# 3 4 5 | 12 13 14 |
# 6 7 8 | 15 16 17 |

# moves = [43]
# move_set = [max for you, min for opp, max for you after opp move]
# move_set = [12,7,23]
# move_set = [3,5,21]
# moves = [09, 11, 13, 15, 16, 17]

# FUNCTIONAL
# Converts a global square number (0-80) to a local
# pair containing [local_square_number, board_number]
def global_to_local(g):
    lb_num = int(np.floor(g / 9))
    l = g - lb_num * 9
    return [l, lb_num]


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


# Mutates big_board
# Marks a big board at the global location given
def mark_big_board(big_board, g_sq, marker):
    local = global_to_local(g_sq)
    big_board[local[1], local[0]] = marker


# Mutates big_board, main_board_wins
# Marks a big board at the global location given
# Returns the number of the local board that was won if one was won, -1 otherwise
def handle_mark_big_board(big_board, g_sq, marker, main_board_wins):
    mark_big_board(big_board, g_sq, marker)
    local_board_number = global_to_local(g_sq)[1]
    local_winner = check_3x3_win(big_board[local_board_number])
    if local_winner != NO_MARKER:
        # If there was a local victory, see then if that ended the game
        main_board_wins[local_board_number] = local_winner
        return local_board_number
    return -1

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
