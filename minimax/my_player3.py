import random
import sys
from read import readInput
from write import writeOutput

from host import GO


class MiniMax():
    def __init__(self, piece_type):
        self.piece_type = piece_type
        self.type = 'random'

    def isMovesLeft(self, board):
        # game has not ended, moves may still be present
        if not board.game_end(self.piece_type):
            return True

    def move(self, board, i, j, curr_player):
        x = board.place_chess(i, j, curr_player)
        y = board.remove_died_pieces(3-curr_player)

    def valid_moves_list(self, curr, curr_player):
        # curr: GO class instance
        # player: current player/piece_type
        valid = []
        for i in range(5):
            for j in range(5):
                if curr.valid_place_check(i, j, curr_player):
                    valid.append((i, j))
        return valid

    def evaluate(self, b, curr_player):
        _min, _max, _eval_min, _eval_max = 0, 0, 0, 0
        died_max, died_min = 0, 0
        for i in range(5):
            for j in range(5):
                if b[i][j] == self.piece_type:
                    _max += 1
                    died_max += b.remove_died_pieces(self.piece_type)
                    _eval_max += (_max + b.find_liberty(i, j))
                elif b[i][j] == 3 - self.piece_type:
                    _min += 1
                    died_min += b.remove_died_pieces(3-self.piece_type)
                    _eval_min += (_min + b.find_liberty(i, j))
        heuristic = _eval_max - _eval_min
        if self.piece_type == curr_player:
            return heuristic + died_min
        else:
            return -heuristic + died_max

    def minimax(self, ):
        score = self.evaluate(board)

        pass

    def driver(self, go):
        '''
        Get one input.

        :param go: Go instance.
        :return: (row, column) coordinate of input.
        '''
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, self.piece_type, test_check=True):
                    possible_placements.append((i, j))

        if not possible_placements:
            return "PASS"
        else:
            return random.choice(possible_placements)


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = MiniMax(piece_type)
    action = player.driver(go)
    writeOutput(action)
