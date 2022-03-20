import random
import numpy as np
from copy import deepcopy


def writeOutput(result, path="output.txt"):
    res = ""
    if result[0] == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)


def readInput(n, path="input.txt"):
    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n + 1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n + 1: 2 * n + 1]]

        return piece_type, previous_board, board


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
        if board[p[0]][p[1]] == board[i][j]:
            group_allies.append(p)
    return group_allies


def ally_dfs(board, i, j):
    q = [(i, j)]
    ally_members = []
    while q:
        p = q.pop(0)
        ally_members.append(p)
        neighbor_allies = detect_neighbor_ally(board, p[0], p[1])
        for al in neighbor_allies:
            if al not in q and al not in ally_members:
                q.append(al)
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
                if not (calc_liberty(board, i, j) > 0) and (i, j) not in dead_pieces:
                    dead_pieces.append((i, j))
    return dead_pieces


def remove_certain_pieces(board, dead_pieces):
    for p in dead_pieces:
        board[p[0]][p[1]] = 0
    return board


def remove_dead_pieces(b, piece_type):
    dead_pieces = find_dead_pieces(b, piece_type)
    if not dead_pieces:
        return b
    b_rcp = remove_certain_pieces(b, dead_pieces)
    return b_rcp


def valid_place_check(board, prev, i, j, piece_type):
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
    # print(test_board)
    test_board[i][j] = piece_type
    test_board_dead_pieces = find_dead_pieces(test_board, 3 - piece_type)
    test_board_rdp = remove_dead_pieces(test_board, 3 - piece_type)
    if calc_liberty(test_board_rdp, i, j) >= 1:
        if not ((compare(prev, test_board_rdp) is True) and test_board_dead_pieces):
            return True
    return False

def compare(b1, b2):
    for i in range(5):
        for j in range(5):
            if b1[i][j] != b2[i][j]:
                return False
    return True


def valid_moves_list(b, prev, piece_type):
    valid = []
    for i in range(5):
        for j in range(5):
            if valid_place_check(b, prev, i, j, piece_type):
                # print('valid_moves_list...valid..in..loop....', valid)
                valid.append((i, j))
    return valid


def place_chess(board, prev_board, i, j, piece_type):
    valid_place = valid_place_check(board, prev_board, i, j, piece_type)
    if not valid_place:
        return None
    board[i][j] = piece_type
    return board


def move(curr, prev_board, i, j, piece_type):
    temp = deepcopy(curr)
    temp[i][j] = piece_type
    temp = remove_dead_pieces(temp, 3-piece_type)
    return temp


def evaluate(b, curr_player):
    _min, _max, _eval_min, _eval_max, died_max, died_min = 0, 0, 0, 0, 0, 0
    for i in range(5):
        for j in range(5):
            if b[i][j] == COLOR:
                _max += 1
                died_max += len(find_dead_pieces(b, curr_player))
                _eval_max += (_max + calc_liberty(b, i, j))
            elif b[i][j] == 3 - COLOR:
                _min += 1
                died_min += len(find_dead_pieces(b, curr_player))
                _eval_min += (_min + calc_liberty(b, i, j))
    heuristic = _eval_max - _eval_min
    if COLOR == curr_player:
        return heuristic
    else:
        return -heuristic


def minimax(curr_board, prev_board, alpha, beta, maxDepth, piece_type):
    best = 0
    moves = []
    curr_board_copy = deepcopy(curr_board)
    valid_moves = valid_moves_list(curr_board, prev_board, piece_type)
    # print('MiniMax...valid....', valid_moves)
    for m in valid_moves:
        fut = move(curr_board, prev_board, m[0], m[1], piece_type)
        score = -1 * min_turn(fut, curr_board_copy, maxDepth, alpha, beta, 3 - piece_type)

        if score > best or len(moves) == 0:
            best = score
            alpha = best
            moves = [m]
        elif score == best:
            moves.append(m)
    # print('MiniMax...', moves)
    return moves


def min_turn(curr_board, prev_board, maxDepth, alpha, beta, player):
    best_score = evaluate(curr_board, player)
    if not maxDepth:
        return best_score
    curr_board_copy = deepcopy(curr_board)
    valid_moves = valid_moves_list(curr_board, prev_board, player)
    for m in valid_moves:
        future_board = move(curr_board, prev_board, m[0], m[1], player)
        score = -1 * max_turn(future_board, curr_board_copy, maxDepth - 1,
                              alpha, beta, 3 - player)
        if score > best_score:
            best_score = score
        player_score = -1 * best_score
        if alpha > player_score:
            return best_score
        if beta < best_score:
            beta = best_score
    return best_score


def max_turn(curr_board, prev_board, maxDepth, alpha, beta, player):
    best_score = evaluate(curr_board, player)
    if maxDepth == 0:
        return best_score
    curr_board_copy = deepcopy(curr_board)
    valid_moves = valid_moves_list(curr_board, prev_board, player)
    for m in valid_moves:
        future_board = move(curr_board, prev_board, m[0], m[1], player)
        score = -1 * min_turn(future_board, curr_board_copy, maxDepth - 1,
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
    action = minimax(curr_board, prev_board, -np.inf, np.inf, maxDepth, piece_type)
    # print('action...', action)
    if not action:
        return ['PASS']
    return random.choice(action)


# MAIN

COLOR, PREV_BOARD, CURR_BOARD = readInput(5)
max_depth = 3

c, c_bool = 0, False
for i in range(5):
    for j in range(5):
        if CURR_BOARD[i][j] != 0:
            if i == 2 and j == 2:
                c_bool = True
            c += 1
if (c == 0 and COLOR == 1) or (c == 1 and COLOR == 2 and not c_bool):
    action = (2, 2)
else:
    action = driver(CURR_BOARD, PREV_BOARD, COLOR, max_depth)
print(action)
writeOutput(action)
