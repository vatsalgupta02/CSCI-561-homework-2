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

    def evaluate(self, b):
        _min, _max, _eval_min, _eval_max = 0, 0, 0, 0
        for i in range(5):
            for j in range(5):
                if b[i][j] == self.piece_type:
                    _max += 1
                    _eval_max += (_max + b.find_liberty(i, j))
                elif b[i][j] == 3-self.piece_type:
                    _min += 1
                    _eval_min += (_min + b.find_liberty(i, j))
        heuristic = _eval_max - _eval_min
        # if self.piece_type == player:
        #     heuristic = _eval_max - _eval_min
        # else:
        #     heuristic = _eval_min - _eval_max
        return heuristic

    def minimax(self, board, depth, isMax):
        score = self.evaluate(board)
        pass

    def move(self, go):
        '''
        Get one input.

        :param go: Go instance.
        :return: (row, column) coordinate of input.
        '''        
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, self.piece_type, test_check = True):
                    possible_placements.append((i,j))

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
    action = player.move(go)
    writeOutput(action)