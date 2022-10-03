import pygame
import display as disp
import core_gameplay as gp
import game as game
import os.path
import copy
import math
import random

from os.path import exists as file_exists

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
def minimax(current_board, current_local_board_num, my_symbol_, opponent_symbol_, depth, alpha, beta, maximizing):
    
    # check if current board is a terminal state (if 0 game continues)
    print("-----------")
    print(current_board)
    print("-----------")
    is_terminal_board = gp.check_3x3_win(current_board)

    # evaluate and return hueristic val only at terminal state
    if depth == 0 or is_terminal_board != 0:
        return randint(1,100)

    if maximizing:
        max_eval = -math.inf
        # can_move_in_won_board is set to false
        # get all of the possible moves from current board 
        possible_moves = gp.valid_moves(current_board, current_local_board_num, False)
        
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
        possible_moves = gp.valid_moves(current_board, current_local_board_num, False)

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
    gp.handle_mark_big_board(new_board, move, marker, new_board_wins)
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