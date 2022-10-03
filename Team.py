import pygame
import display as disp
import core_gameplay as gp
import game as game
import os.path
import copy
import math

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
        # pass in a copy as currentPos?
        # expanding is done within minimax funciton recursively not here..
        # move = minimax(currentPos, depth, alpha, beta, maximizing)
        if move in moves:
            move_selected = True

    # return our optimal move
    return move


# def minimax(pos, depth, alpha, beta, maximizingPlayer)
# pos is represented by multiple args?
def minimax(moves, main_board, local_board_num, my_symbol, opponent_symbol, depth, alpha, beta, maximizing):
    
    # if depth == 0 or game over in pos
    # if 
    #   return static eval of pos (this is the only place we evaluate)
    #
    # if maximizing player
    #   maxEval = -infinity
    #   for each child of pos
    #       eval = minimax(child, depth-1, alpha, beta, false)
    #       maxEval = max(maxEval, eval)
    #       alpha = max(alpha, eval)
    #       if beta <= alpha:
    #           break
    #   return maxEval
    # else
    #   minEval = +inf
    #   for each child of pos
    #       eval = minimax(child, depth-1, alpha, beta, true) 
    #       minEval = min(minEval, eval)
    #       beta = min(beta, eval)
    #       if beta <= alpha:
    #           break
    #   return minEval

    return eval

    # MISC LOGIC FOR DETERMINING TERMINAL NODE    
    #board_state = game.game.main_board.copy()
    #board_state_check_win = gp.check_3x3_win(board_state)
    #if board_state_check_win != 0:
    #    return board_state_check_win    
    #minimax_scores = []

#execute_move(board_state , move)
def execute_move(board_state, move, marker, board_state_wins):
    new_board = board_state.copy()
    new_board_wins = board_state_wins.copy()
    gp.handle_mark_big_board(new_board, move, marker, new_board_wins)
    return new_board

#get_valid_moves(board_state)
# returns valid moves from curr position
# 

# Optional Rule Variables

        # True allows you to send opponents to won boards (Thad rules)
        # False means won boards are off limits (Classic rules)
        #self.can_move_in_won_board = False

        # True makes the game a draw when a player is sent to a full square (Thad rules)
        # False allows the player to play in any free space (Classic rules)
        #self.send_to_full_board_is_draw = False

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

#-----
    # possible_moves(current_board) -> pos_moves [0,1,2,3,4,5,6,7,8]
    #  for each move in pos_moves:
    #    move_set = [0]
    #    expand all possible for 0
    #    basecase: len(moveset) => 3
    #       move_sets.append(moveset)
 
    # if (terminal_node_reached and len(moveset >= 3):
    # 

def make_move(maximizing, move, main_board, local_board_num, my_symbol, opponent_symbol):
    my_move = -1
    my_move = int(move)

    #Check if the game has ended
    #if not file_exists('end_game.txt'):
        
    # move local pair
    move_lp = gp.global_to_local(my_move)
    local_sq = move_lp[0]

    if gp.handle_mark_big_board(main_board, my_move, my_symbol, self.main_board_wins) > -1:
        self.winner = gp.check_3x3_win(self.main_board_wins)

    print(self.main_board)

