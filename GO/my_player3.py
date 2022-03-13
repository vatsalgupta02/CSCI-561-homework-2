import random
import sys
from read import readInput
from write import writeOutput
import numpy as np

from host import GO

WIN_REWARD = 1.0
DRAW_REWARD = 0.5
LOSS_REWARD = 0.0


def encode_state(self):
    """ Encode the current state of the board as a string
    """
    return ''.join([str(self.board[i][j]) for i in range(self.size) for j in range(self.size)])

def cal_score(self, piece_type):
    if piece_type == 2:
        # add komi
        return self.komi + self.score(2)
    else:
        return self.score(1)

GO.cal_score = cal_score
GO.encode_state = encode_state


class QLearner:
    GAME_NUM = 100000

    def __init__(self, alpha=.7, gamma=.9, initial_value=0.5):
        if not (0 < gamma <= 1):
            raise ValueError("An MDP must have 0 < gamma <= 1")

        # self.side = side
        self.type = 'q_agent'
        self.alpha = alpha
        self.gamma = gamma
        self.q_values = {}
        self.history_states = []
        self.piece_type = None
        self.initial_value = initial_value
        # self.state = ?

    def flatten_q(self):
        '''
        flatten q_values to include a q_value for action -> pass
        length of the return list-> 25 possible actions + 1 for pass
        '''
        pass

    def revert_q(self):
        '''
        revert the q_values to 2D list from flattened list
        '''
        pass

    def rotate(self):
        '''
        rotate the states to decrease the number of q_value computations
        '''
        pass

    def Q(self, state):
        if state not in self.q_values:
            q_val = np.zeros((3, 3))
            q_val.fill(self.initial_value)
            self.q_values[state] = q_val
        return self.q_values[state]

    def _select_best_move(self, board):
        state = board.encode_state()
        q_values = self.Q(state)
        row, col = 0, 0
        curr_max = -np.inf
        while True:

            i, j, _pass = self._find_max(q_values)

            if board.is_valid_move(i, j):
                return i, j
            else:
                q_values[i][j] = -1.0

    def _find_max(self, q_values):
        curr_max = -np.inf
        row, col = 0, 0
        _pass = None
        if np.all(q_values == -1):
            _pass = True
            return row, col, _pass

        for i in range(0, 5):
            for j in range(0, 5):
                if q_values[i][j] > curr_max:
                    curr_max = q_values[i][j]
                    row, col = i, j
        return row, col, _pass

    def move_train(self, go, piece_type):
        pass

    def move(self, board):
        """ make a move
        """
        if board.game_over():
            return
        row, col = self._select_best_move(board)
        self.history_states.append((board.encode_state(), (row, col)))
        return board.move(row, col, self.side)

    def learn(self, board):
        """
        when games ended,
        this method will be
        called to update the q_values
        """
        reward = go.cal_score(self.piece_type) - go.cal_score(3-self.piece_type)
        self.history_states.reverse()
        max_q_value = -1.0
        for hist in self.history_states:
            state, move = hist
            q = self.Q(state)
            if max_q_value < 0:
                q[move[0]][move[1]] = reward
            else:
                q[move[0]][move[1]] = q[move[0]][move[1]] * (1 - self.alpha) + self.alpha * self.gamma * max_q_value
            max_q_value = np.max(q)
        self.history_states = []


class RandomPlayer():
    def __init__(self):
        self.type = 'random'

    def get_input(self, go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''        
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check = True):
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
    player = RandomPlayer()
    action = player.get_input(go, piece_type)
    writeOutput(action)