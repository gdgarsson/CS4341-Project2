import pygame
import display as disp
import core_gameplay as gp
import game as game
import os.path
import copy

from os.path import exists as file_exists

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

#get_valid_moves(board_state) 



#execute_move(board_state , move)
#   return board_state (the new one)
def execute_move(board_state, move, marker, board_state_wins):
    new_board = board_state.copy()
    new_board_wins = board_state_wins.copy()
    gp.handle_mark_big_board(new_board, move, marker, new_board_wins)
    return new_board

def minimax(maximizing, moves, main_board, local_board_num, my_symbol, opponent_symbol):
    # maximizing : bool representing if current player is maximizing or not
    
    # how many moves ahead we want to search
    depth = 3

    

    # possible_moves(current_board) -> pos_moves [0,1,2,3,4,5,6,7,8]
    #  for each move in pos_moves:
    #    move_set = [0]
    #    expand all possible for 0
    #    basecase: len(moveset) => 3
    #       move_sets.append(moveset)

    # if (terminal_node_reached and len(moveset >= 3):
    # 

    

    board_state = game.game.main_board.copy()
    board_state_check_win = gp.check_3x3_win(board_state)
    if board_state_check_win != 0:
        return board_state_check_win    
    
    minimax_scores = []
    
    #for a_move in moves:

    # returns our optimal move
    return move

def make_move(maximizing, move, main_board, local_board_num, my_symbol, opponent_symbol):
    my_move = -1
    my_move = int(move)

    #Check if the game has ended
    if not file_exists('end_game.txt'):
        



    # move local pair
    move_lp = gp.global_to_local(my_move)
    local_sq = move_lp[0]

    if gp.handle_mark_big_board(main_board, my_move, my_symbol, self.main_board_wins) > -1:
        self.winner = gp.check_3x3_win(self.main_board_wins)

    print(self.main_board)

