from player import Player
from utility_functions import GetPieces
from board import Board


# This class is a AI learning to play checkers using Alpha-Beta pruning
class AlphaBeta(Player):

    def __init__(self, id, depth, board=None):
        self.board = board
        self.depth = depth
        self.player_id = id

# A class that implements the pruning algorithm to make move decisions based on the current state
    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if board.check_game_finished():
            if GetPieces(board.spots, board.player_turn) == [0, 0]:
                if maximizing_player:
                    # Using integers instead of float("inf") so it's less than float("inf") not equal to
                    return -10000000, None
                else:
                    return 10000000, None
            elif GetPieces(board.spots, not board.player_turn) == [0, 0]:
                if maximizing_player:
                    return 1000000, None
                else:
                    return -1000000, None
            else:
                return 0, None

        if depth == 0:
            info_players = GetPieces(board.spots)
            if board.player_turn != maximizing_player:
                return info_players[1] + 2 * info_players[3] - (info_players[0] + 2 * info_players[2]), None
            return info_players[0] + 2 * info_players[2] - (info_players[1] + 2 * info_players[3]), None
        possible_moves = board.get_moves_available()

        potential_spots = board.get_new_game_states(possible_moves)
        best_move_index = None
        if maximizing_player:
            v = float('-inf')
            for j in range(len(potential_spots)):
                cur_board = Board(potential_spots[j], not board.player_turn)
                alpha_beta_results = self.alpha_beta(cur_board, depth - 1, alpha, beta, False)
                if v < alpha_beta_results[0]:
                    v = alpha_beta_results[0]
                    alpha = max(alpha, v)
                    best_move_index = j
                if beta <= alpha:
                    break
            if best_move_index is None:
                return v, None
            return v, possible_moves[best_move_index]
        else:
            v = float('inf')
            for j in range(len(potential_spots)):
                cur_board = Board(potential_spots[j], not board.player_turn)
                alpha_beta_results = self.alpha_beta(cur_board, depth - 1, alpha, beta, True)
                if v > alpha_beta_results[0]:
                    v = alpha_beta_results[0]
                    best_move_index = j
                    beta = min(beta, v)
                if beta <= alpha:
                    break
            if best_move_index is None:
                return v, None
            return v, possible_moves[best_move_index]

    def get_next_move(self):
        return self.alpha_beta(self.board, self.depth, float('-inf'), float('inf'), self.player_id)[1]