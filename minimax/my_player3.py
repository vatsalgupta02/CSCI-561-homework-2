import random
import numpy as np
from copy import deepcopy

from read import readInput
from write import writeOutput

def detect_neighbor(board, i, j):
    neighbors = []
    if i > 0:
        neighbors.append((i - 1, j))
    if i < len(board) - 1:
        neighbors.append((i + 1, j))
    if j > 0:
        neighbors.append((i, j - 1))
    if j < len(board) - 1:
        neighbors.append((i, j + 1))
    return neighbors


def detect_neighbor_ally(board, i, j):
    # Detect all the neighbors of a given stone
    neighbors = detect_neighbor(board, i, j)
    group_allies = []
    # Detect borders and add neighbor coordinates
    for p in neighbors:
        # print('p......', p)
        # print("i...j....", i, "   ", j)
        if board[p[0]][p[1]] == board[i][j]:
            group_allies.append(p)
    return group_allies


def ally_dfs(board, i, j):
    stack = [(i, j)]
    ally_members = []
    while stack:
        p = stack.pop()
        ally_members.append(p)
        neighbor_allies = detect_neighbor_ally(board, p[0], p[1])
        for al in neighbor_allies:
            if al not in stack and al not in ally_members:
                stack.append(al)
    return ally_members


def calc_liberty(board, i, j):
    count = 0
    ally_members = ally_dfs(board, i, j)
    for m in ally_members:
        neighbors = detect_neighbor(board, m[0], m[1])
        for p in neighbors:
            if board[p[0]][p[1]] == 0:
                count += 1
    return count


def find_dead_pieces(board, piece_type):
    dead_pieces = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == piece_type:
                if not calc_liberty(board, i, j) > 0:
                    dead_pieces.append((i, j))
    return dead_pieces


def remove_certain_pieces(board, dead_pieces):
    for p in dead_pieces:
        board[p[0]][p[1]] = 0
    return board


def remove_dead_pieces(b, piece_type):
    dead_pieces = find_dead_pieces(b, piece_type)
    if len(dead_pieces) != 0:
        b = remove_certain_pieces(b, dead_pieces)    
    return b


def valid_place_check(board, i, j, piece_type):
    # Row index out of range
    if not (0 <= i < 5):
        return False
    # Column index out of range
    if not (0 <= j < 5):
        return False
    # not an empty place
    if board[i][j] != 0:
        return False
    test_board = deepcopy(board)
    test_board[i][j] = piece_type
    if calc_liberty(test_board, i, j) > 0:
        return True
    test_board_dead_pieces = find_dead_pieces(test_board, 3 - piece_type)
    test_board_rdp = remove_dead_pieces(test_board, 3 - piece_type)
    if not calc_liberty(test_board_rdp, i, j) > 0:
        return False

    else:
        if test_board_dead_pieces and compare(test_board_rdp, board):
            return False
    return True


def compare(b1, b2):
    for i in range(5):
        for j in range(5):
            if b1[i][j] != b2[i][j]:
                return False
    return True


def valid_moves_list(b, piece_type):
    '''

    :param b: board list of lists
    :param piece_type:
    :return:
    '''
    # valid = []

    valid=set()
    for i in range(5):
        for j in range(5):
            if valid_place_check(b, i, j, piece_type):
                valid.add((i, j))
    return valid


def place_chess(board, i, j, piece_type):
    valid_place = valid_place_check(board, i, j, piece_type)
    if not valid_place:
        return None
    board[i][j] = piece_type
    return board


def move(curr, i, j, piece_type):
    temp = deepcopy(curr)
    temp_move = place_chess(temp, i, j, piece_type)
    if temp_move is None:
        return curr
    temp_rdp = remove_dead_pieces(temp_move, piece_type)
    return temp_rdp


# def evaluate(b, curr_player):
#     _min, _max, _eval_min, _eval_max, died_max, died_min = 0, 0, 0, 0, 0, 0
#     for i in range(5):
#         for j in range(5):
#             if b[i][j] == COLOR:
#                 _max += 1
#                 died_max += len(find_dead_pieces(b, curr_player))
#                 _eval_max += (_max + calc_liberty(b, i, j))
#             elif b[i][j] == 3 - COLOR:
#                 _min += 1
#                 died_min += len(find_dead_pieces(b, curr_player))
#                 _eval_min += (_min + calc_liberty(b, i, j))
#     heuristic = _eval_max - _eval_min
#     if COLOR == curr_player:
#         return heuristic
#     else:
#         return -heuristic

def evaluate(b, curr_player):
    black, white = -3, 3
    bDanger, wDanger = 0, 0
    for i in range(5):
        for j in range(5):
            if b[i][j] == 1:
                lib = calc_liberty(b, i, j)
                if lib < 2:
                    bDanger += 1
                black += 1
            elif b[i][j] == 2:
                lib = calc_liberty(b, i, j)
                if lib < 2:
                    wDanger += 1
                white += 1
    if curr_player == 1:
        heuristic = (10*black) - (10*white) + (2*wDanger) - (1.5*bDanger)
    elif curr_player == 2:
        heuristic = (10*white) - (10*black) + (2*bDanger) - (1.5*wDanger)
    
    return heuristic



def minimax(curr_board_copy, alpha, beta, maxDepth, piece_type):
    best = 0
    # curr_board_copy = deepcopy(curr_board)
    moves = []
    valid_moves = valid_moves_list(curr_board_copy, piece_type)

    for m in valid_moves:
        fut = move(curr_board_copy, m[0], m[1], piece_type)
        score = -1 * min_turn(fut, maxDepth, alpha, beta, 3 - piece_type)

        if score > best or len(moves) == 0:
            best = score
            alpha = best
            moves = [m]
        elif score == best:
            moves.append(m)
    return moves


def min_turn(curr_board, maxDepth, alpha, beta, player):
    # print('before evaluate......', curr_board)
    best_score = evaluate(curr_board, player)
    if maxDepth == 0:
        return best_score
    # curr_board_copy = deepcopy(curr_board)
    valid_moves = valid_moves_list(curr_board, player)
    for m in valid_moves:
        future_board = move(curr_board, m[0], m[1], player)
        score = -1 * max_turn(future_board, maxDepth - 1,
                              alpha, beta, 3 - player)
        if score > best_score:
            best_score = score
    player_score = -1 * best_score
    if alpha > player_score:
        return best_score
    if beta < best_score:
        beta = best_score
    return best_score


def max_turn(curr_board, maxDepth, alpha, beta, player):
    best_score = evaluate(curr_board, player)
    if maxDepth == 0:
        return best_score
    # curr_board_copy = deepcopy(curr_board)
    valid_moves = valid_moves_list(curr_board, player)
    for m in valid_moves:
        future_board = move(curr_board, m[0], m[1], player)
        score = -1 * min_turn(future_board, maxDepth - 1,
                              alpha, beta, 3 - player)
        if score > best_score:
            best_score = score
        opponent_score = -1 * best_score
        if beta > opponent_score:
            return best_score
        if alpha < best_score:
            alpha = best_score
    return best_score

def driver(curr_board, prev_board, piece_type, maxDepth):
    c, c_bool = 0, False
    for i in range(5):
        for j in range(5):
            if (curr_board[i][j] != 0 and i == 2 and j == 2):
                c_bool = True
                c += 1
    if (c == 0 and piece_type == 1) or (c == 1 and piece_type == 2 and not c_bool):
        action = [(2, 2)]
    else:
        action = minimax(curr_board, -np.Inf, np.Inf, maxDepth, piece_type)

    if len(action) == 0:
        return 'PASS'
    return random.choice(action)


COLOR, PREV_BOARD, CURR_BOARD = readInput(5)
max_depth = 2

action = driver(CURR_BOARD, PREV_BOARD, COLOR, max_depth)
writeOutput(action)
