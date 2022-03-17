import copy
import random
import sys

import numpy as np

from read import readInput
from write import writeOutput
from copy import deepcopy

from host import GO


class MiniMax:
    def __init__(self, piece_type):
        self.piece_type = piece_type
        self.type = 'random'

    def isMovesLeft(self, board):
        # game has not ended, moves may still be present
        if not board.game_end(self.piece_type):
            return True

    def move(self, board, i, j, curr_player):
        temp = board.copy_board()
        x = temp.place_chess(i, j, curr_player)
        y = temp.remove_died_pieces(3-curr_player)
        return temp

    def valid_moves_list(self, curr, curr_player):
        # curr: GO class instance
        # player: current player/piece_type
        valid = []
        for i in range(5):
            for j in range(5):
                if curr.valid_place_check(i, j, curr_player):
                    valid.append((i, j))
        return valid

    def cal_liberty(self, b_obj, i, j):
        # piece_type = self.piece_type
        b_board = b_obj.board
        count = {
            b_board[i][j]: 0,
        }
        ally_members = b_obj.ally_dfs(i, j)
        for member in ally_members:
            neighbors = b_obj.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if b_board[piece[0]][piece[1]] == 0:
                    count[b_board[i][j]] += 1
        return count[b_board[i][j]]

    def evaluate(self, b, curr_player):
        _min, _max, _eval_min, _eval_max, died_max, died_min = 0, 0, 0, 0, 0, 0
        b_board = b.board
        for i in range(5):
            for j in range(5):
                if b_board[i][j] == self.piece_type:
                    _max += 1
                    died_max += len(b.remove_died_pieces(self.piece_type))
                    _eval_max += (_max + self.cal_liberty(b, i, j))
                elif b_board[i][j] == 3 - self.piece_type:
                    _min += 1
                    died_min += len(b.remove_died_pieces(3-self.piece_type))
                    _eval_min += (_min + self.cal_liberty(b, i, j))
        heuristic = _eval_max - _eval_min
        if self.piece_type == curr_player:
            return heuristic
        else:
            return -heuristic

    def minimax(self, curr, prev, alpha, beta, maxDepth):
        best = 0
        curr_board_copy = copy.deepcopy(curr)
        moves = []
        valid_moves = self.valid_moves_list(curr_board_copy, self.piece_type)
        # TODO: if len(valid) == 0: then pass

        for m in valid_moves:
            fut = self.move(curr, m[0], m[1], self.piece_type)
            score = -1 * self.min_turn(fut, curr_board_copy, maxDepth, alpha, beta, 3-self.piece_type)

            if score > best or len(moves) == 0:
                best = score
                alpha = best
                moves = [m]

            elif score == best:
                moves.append(m)

        return moves

    def min_turn(self, curr_board, prev_board, maxDepth, alpha, beta, player):
        best_score = self.evaluate(curr_board, player)
        if maxDepth == 0:
            return best_score

        curr_board_copy = copy.deepcopy(curr_board)
        valid_moves = self.valid_moves_list(curr_board_copy, player)
        for m in valid_moves:
            future_board = self.move(curr_board_copy, m[0], m[1], player)
            score = -1 * self.max_turn(future_board, curr_board, maxDepth-1,
                                       alpha, beta, 3-player)

            if score > best_score:
                best_score = score

            player_score = -1 * best_score

            if alpha > player_score:
                return best_score
            if beta < best_score:
                beta = best_score

        return best_score

    def max_turn(self, curr_board, prev_board, maxDepth, alpha, beta, player):
        best_score = self.evaluate(curr_board, player)
        if maxDepth == 0:
            return best_score
        curr_board_copy = copy.deepcopy(curr_board)
        valid_moves = self.valid_moves_list(curr_board_copy, player)
        for m in valid_moves:
            future_board = self.move(curr_board_copy, m[0], m[1], player)
            score = -1 * self.max_turn(future_board, curr_board, maxDepth-1,
                                       alpha, beta, 3-player)

            if score > best_score:
                best_score = score

            opponent_score = -1 * best_score

            if beta > opponent_score:
                return best_score
            if alpha < best_score:
                alpha = best_score

        return best_score

    def driver(self, go):
        '''
        Get one input.

        :param go: Go instance.
        :return: (row, column) coordinate of input.
        '''
        # possible_placements = []
        # for i in range(go.size):
        #     for j in range(go.size):
        #         if go.valid_place_check(i, j, self.piece_type, test_check=True):
        #             possible_placements.append((i, j))
        #
        # if not possible_placements:
        #     return "PASS"
        # else:
        #     return random.choice(possible_placements)
        curr = go.board
        prev = go.previous_board

        action = self.minimax(go, prev, -np.Inf, -np.Inf, 2)
        if len(action) == 0:
            return 'PASS'
        else:
            return random.choice(action)


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = MiniMax(piece_type)
    action = player.driver(go)
    writeOutput(action)
