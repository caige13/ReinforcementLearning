
import math
import copy
from functools import reduce


class Board:
    BLANK_SQUARE = 0
    PLAYER1 = 1
    PLAYER2 = 2
    PLAYER1_K = 3
    PLAYER2_K = 4
    REVERSE_PLAYER = PLAYER2
    H = 8
    W = 4

    # Creates a new Board class instance, in the starting configuration
    def __init__(self, old_spots=None, player_turn=True):
        self.player_turn = player_turn
        if old_spots is None:
            self.spots = [[j, j, j, j] for j in
                          [self.PLAYER1, self.PLAYER1, self.PLAYER1, self.BLANK_SQUARE, self.BLANK_SQUARE, self.PLAYER2, self.PLAYER2, self.PLAYER2]]
        else:
            self.spots = old_spots

    # Takes all of the current game positions and clears them back to starting position
    def game_reset(self):
        self.spots = Board().spots

    # Completely clears the board, leaving only empty spaces
    def board_clear(self):
        self.spots = [[j, j, j, j] for j in
                      [self.BLANK_SQUARE] * self.H]

    # Returns true if the game is over, false if it's still being played
    def check_game_finished(self):
        if not self.get_moves_available():
            return True
        return False

    # Returns if the spot at the inputted coordinates is a spot on the board
    def is_invalid_square(self, location):
        if len(location) == 0 or location[0] < 0 or location[0] > self.H - 1 or location[1] < 0 or location[1] > self.W - 1:
            return True
        return False

    # Retreives the information on the inputted location spot
    def get_info(self, loc):
        return self.spots[loc[0]][loc[1]]

    # Gets possible moves diagonally forward or back 'n' number of times with no directional change midway
    def n_possible_moves(self, beg_location, n, reverse=False):
        if n % 2 == 0:
            t1 = 0
            t2 = 0
        elif beg_location[0] % 2 == 0:
            t1 = 0
            t2 = 1
        else:
            t1 = 1
            t2 = 0

        solution = [[beg_location[0], beg_location[1] + math.floor(n / 2) + t1],
                  [beg_location[0], beg_location[1] - math.floor(n / 2) - t2]]

        if reverse:
            solution[0][0] = solution[0][0] - n
            solution[1][0] = solution[1][0] - n
        else:
            solution[0][0] = solution[0][0] + n
            solution[1][0] = solution[1][0] + n

        if self.is_invalid_square(solution[0]):
            solution[0] = []
        if self.is_invalid_square(solution[1]):
            solution[1] = []

        return solution

    # Gets all the moves that can be made that don't require capturing an enemy piece
    def basic_moves(self, beg_location):
        if self.spots[beg_location[0]][beg_location[1]] > 2:
            nex_loc = self.n_possible_moves(beg_location, 1)
            nex_loc.extend(self.n_possible_moves(beg_location, 1, True))
        elif self.spots[beg_location[0]][beg_location[1]] == self.REVERSE_PLAYER:
            nex_loc = self.n_possible_moves(beg_location, 1, True)  # Switched the true from the statement below
        else:
            nex_loc = self.n_possible_moves(beg_location, 1)

        pos_nex_loc = []

        for location in nex_loc:
            if len(location) != 0:
                if self.spots[location[0]][location[1]] == self.BLANK_SQUARE:
                    pos_nex_loc.append(location)

        return [[beg_location, end_spot] for end_spot in pos_nex_loc]

    # Use recursion to grab all of the potential moves that involve taking an enemy piece
    def jump_moves(self, beg_location, starting_moves=None):
        if starting_moves is None:
            starting_moves = [beg_location]

        solution = []
        if self.spots[beg_location[0]][beg_location[1]] > 2:
            n1 = self.n_possible_moves(beg_location, 1)
            n2 = self.n_possible_moves(beg_location, 2)
            n1.extend(self.n_possible_moves(beg_location, 1, True))
            n2.extend(self.n_possible_moves(beg_location, 2, True))
        elif self.spots[beg_location[0]][beg_location[1]] == self.REVERSE_PLAYER:
            n1 = self.n_possible_moves(beg_location, 1, True)
            n2 = self.n_possible_moves(beg_location, 2, True)
        else:
            n1 = self.n_possible_moves(beg_location, 1)
            n2 = self.n_possible_moves(beg_location, 2)

        for j in range(len(n1)):
            if (not self.is_invalid_square(n2[j])) and (not self.is_invalid_square(n1[j])):  # if both spots are there
                if self.get_info(n1[j]) != self.BLANK_SQUARE and self.get_info(
                        n1[j]) % 2 != self.get_info(beg_location) % 2:  # is the next spot enemy
                    if self.get_info(n2[j]) == self.BLANK_SQUARE:  # is the next spot a blank square
                        tm_1 = copy.deepcopy(starting_moves)
                        tm_1.append(n2[j])
                        answer_length = len(solution)
                        if self.get_info(beg_location) != self.PLAYER1 or n2[j][0] != self.H - 1:
                            if self.get_info(beg_location) != self.PLAYER2 or n2[j][0] != 0:
                                tm_2 = [beg_location, n2[j]]
                                t_board = Board(copy.deepcopy(self.spots), self.player_turn)
                                t_board.execute_move(tm_2, False)
                                solution.extend(t_board.jump_moves(tm_2[1], tm_1))
                        if len(solution) == answer_length:
                            solution.append(tm_1)
        return solution

    # Get all the moves that can be made from the current state of the board
    def get_moves_available(self):
        position_of_pieces = []
        for j in range(self.H):
            for i in range(self.W):
                if (self.player_turn == True and (self.spots[j][i] == self.PLAYER1 or self.spots[j][i] == self.PLAYER1_K)) or (
                        self.player_turn == False and (self.spots[j][i] == self.PLAYER2 or self.spots[j][i] == self.PLAYER2_K)):
                    position_of_pieces.append([j, i])

        try:  # potentially unnecessary
            jump_moves = list(reduce(lambda a, b: a + b, list(
                map(self.jump_moves, position_of_pieces))))

            if len(jump_moves) != 0:
                return jump_moves

            return list(reduce(lambda a, b: a + b,
                               list(map(self.basic_moves, position_of_pieces))))
        except TypeError:
            return []

    # executes the inputted move and changes the state of the board to reflect it - switches to other player's turn
    def execute_move(self, move, swap_player=True):
        if abs(move[0][0] - move[1][0]) == 2:
            for j in range(len(move) - 1):
                if move[j][0] % 2 == 1:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j][1]
                    else:
                        middle_y = move[j + 1][1]
                else:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j + 1][1]
                    else:
                        middle_y = move[j][1]

                self.spots[int((move[j][0] + move[j + 1][0]) / 2)][middle_y] = self.BLANK_SQUARE

        self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.spots[move[0][0]][move[0][1]]
        if move[len(move) - 1][0] == self.H - 1 and self.spots[move[len(move) - 1][0]][
            move[len(move) - 1][1]] == self.PLAYER1:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.PLAYER1_K
        elif move[len(move) - 1][0] == 0 and self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] == self.PLAYER2:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.PLAYER2_K
        else:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.spots[move[0][0]][move[0][1]]
        self.spots[move[0][0]][move[0][1]] = self.BLANK_SQUARE

        if swap_player:
            self.player_turn = not self.player_turn

    # Get's the new board states given the moves inputted
    def get_new_game_states(self, moves):
        if moves is None:
            return self.spots
        solution = []
        for move in moves:
            original_spots = copy.deepcopy(self.spots)
            self.execute_move(move, swap_player=False)
            solution.append(self.spots)
            self.spots = original_spots
        return solution

    # Places pieces onto the board
    def insert_pieces(self, pieces_info):
        for piece_info in pieces_info:
            self.spots[piece_info[0]][piece_info[1]] = piece_info[2]

    # get's the symbol for the location inputted
    def get_symbol(self, loc):
        if self.spots[loc[0]][loc[1]] == self.BLANK_SQUARE:
            return " "
        elif self.spots[loc[0]][loc[1]] == self.PLAYER1:
            return "o"
        elif self.spots[loc[0]][loc[1]] == self.PLAYER2:
            return "x"
        elif self.spots[loc[0]][loc[1]] == self.PLAYER1_K:
            return "O"
        else:
            return "X"

    # A visual representation of the board
    def print_board(self):
        normal_row = "|---|---|---|---|---|---|---|---|"
        print(normal_row)
        for j in range(self.H):
            if j % 2 == 1:
                t_line = "|///|"
            else:
                t_line = "|"
            for i in range(self.W):
                t_line = t_line + " " + self.get_symbol([j, i]) + " |"
                if i != 3 or j % 2 != 1:  # should figure out if this 3 should be changed to self.WIDTH-1
                    t_line = t_line + "///|"
            print(t_line)
            print(normal_row)