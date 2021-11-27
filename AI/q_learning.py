
from player import Player
import random
from utility_functions import RewardFunction
import json
from ast import literal_eval


class QLearningAI(Player):
    def __init__(self, id, learning_rate, discount_factor, location_info=None,
                 the_random_move_probability=0, the_board=None):

        self.random_move_probability = the_random_move_probability
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.player_id = id
        self.board = the_board
        self.pre_previous_move_state = None
        self.post_previous_move_state = None
        if not location_info is None:
            self.file_transition_info_load(location_info)
        else:
            self.transitions = {}

    # sets the AI's random move probability
    def set_likelihood_random_move_(self, probability):
        self.random_move_probability = probability

    #sets the AI's learning rate
    def set_learning_rate(self, learning_rate):
        self.learning_rate = learning_rate

    # grabs a tuple array from the inputted board spots -each tuple represents characteristics to define the board state
    #Format of returned data:[(own_pieces, opp_pieces, own_kings, opp_kings, own_edges, own_vert_center_mass, opp_vert_center_mass), ..]
    def get_state_with_board_spots(self, boards_spots):
        piece_count = [[0, 0, 0, 0, 0, 0, 0] for j in range(len(boards_spots))]
        for k in range(len(boards_spots)):
            for j in range(len(boards_spots[k])):
                for i in range(len(boards_spots[k][j])):
                    if boards_spots[k][j][i] != 0:
                        piece_count[k][boards_spots[k][j][i] - 1] = piece_count[k][boards_spots[k][j][i] - 1] + 1
                        if (self.player_id and (boards_spots[k][j][i] == 1 or boards_spots[k][j][i] == 3)) or (
                                not self.player_id and (boards_spots[k][j][i] == 2 or boards_spots[k][j][i] == 4)):
                            if i == 0 and j % 2 == 0:
                                piece_count[k][4] = piece_count[k][4] + 1
                            elif i == 3 and j % 2 == 1:
                                piece_count[k][4] = piece_count[k][4] + 1

                            piece_count[k][5] = piece_count[k][5] + j
                        else:
                            piece_count[k][6] = piece_count[k][6] + j

            if piece_count[k][0] + piece_count[k][2] != 0:
                piece_count[k][5] = int(piece_count[k][5] / (piece_count[k][0] + piece_count[k][2]))
            else:
                piece_count[k][5] = 0
            if piece_count[k][1] + piece_count[k][3] != 0:
                piece_count[k][6] = int(piece_count[k][6] / (piece_count[k][1] + piece_count[k][3]))
            else:
                piece_count[k][6] = 0

        return [tuple(counter) for counter in piece_count]

    # grabs the desired transition for current board corrent board config - if none exist it creates one
    def get_best_state_transition(self, possible_state_array,
                                  initial_transition_value=10):
        cur_state = tuple(self.get_state_with_board_spots([self.board.spots])[0])
        done_transitions = {}
        for state in possible_state_array:
            if done_transitions.get((cur_state, tuple(state))) is None:
                if self.transitions.get((cur_state, tuple(state))) is None:
                    self.transitions.update({(cur_state, tuple(state)): initial_transition_value})
                done_transitions.update({(cur_state, tuple(state)): self.transitions.get((cur_state, tuple(state)))})

        if random != 0 and random.random() < self.random_move_probability:
            try:
                return list(done_transitions.keys())[random.randint(0, len(done_transitions) - 1)]
            except:
                return []

        try:
            reverse_dict = {j: i for i, j in done_transitions.items()}
            return reverse_dict.get(max(reverse_dict))
        except:
            return []

    # update self.transition with a finished game before board clear
    def game_completed(self):
        cur_state = self.get_state_with_board_spots([self.board.spots])[0]
        transition = (self.pre_previous_move_state, self.post_previous_move_state)

        self.transitions[transition] = self.transitions[transition] + self.learning_rate * RewardFunction(
            transition[0], cur_state)

        self.pre_previous_move_state = None
        self.post_previous_move_state = None

    # Get array of information about the dictionary self.transitions
    # in form num_transitions, num_start_of_transitions, avg_value, max_value, min_value]
    def get_transitions_info(self):
        begining_of_transitions = {}
        max_v = float("-inf")
        min_v = float("inf")
        cumulativeValue = 0
        for k, v in self.transitions.items():
            if begining_of_transitions.get(k[0]) is None:
                begining_of_transitions.update({k[0]: 0})
            if v > max_v:
                max_v = v
            if v < min_v:
                min_v = v
            cumulativeValue = cumulativeValue + v
        return [len(self.transitions), len(begining_of_transitions), float(cumulativeValue / len(self.transitions)), max_v,
                min_v]

    # Prints the output of get transition_information to console
    def print_transition_info(self, info):
        print("Total transitions: ".ljust(35), info[0])
        print("Total visited states: ".ljust(35), info[1])
        print("Average value of transition: ".ljust(35), info[2])
        print("Maximum value of transition: ".ljust(35), info[3])
        print("Minimum value of transition: ".ljust(35), info[4])

    # Save our current transition information to json file
    def save_transition_information(self, file="data.json"):
        with open(file, 'w') as fp:
            json.dump({str(k): v for k, v in self.transitions.items()}, fp)

    # Load transition info from inputted json file
    def file_transition_info_load(self, file):
        with open(file, 'r') as fp:
            self.transitions = {literal_eval(k): v for k, v in json.load(fp).items()}

    # Look forward a inputted number of moves then return the best values associated with a move of that depth
    def get_best_forward_looking_value(self, depth):
        solution = float("-inf")
        cur_state = self.get_state_with_board_spots([self.board.spots])[0]
        for k, v in self.transitions.items():
            if v > solution and k[0] == cur_state:
                solution = v
        if solution == float("-inf"):
            return None
        return solution

    # If the board exists and is legal then get the next move
    def get_next_move(self):
        if self.pre_previous_move_state is not None:
            cur_state = self.get_state_with_board_spots([self.board.spots])[0]
            transition = (self.pre_previous_move_state, self.post_previous_move_state)
            try:
                max_future_state = self.get_best_forward_looking_value(1)
                self.transitions[transition] = self.transitions[transition] + self.learning_rate * (
                        RewardFunction(transition[0], cur_state) + self.discount_factor * max_future_state -
                        self.transitions[transition])
            except:
                self.transitions[transition] = self.transitions[transition] + self.learning_rate * (
                    RewardFunction(transition[0], cur_state))
        self.pre_previous_move_state = self.get_state_with_board_spots([self.board.spots])[
            0]
        possible_next_moves = self.board.get_moves_available()
        possible_next_states = self.get_state_with_board_spots(
            self.board.get_new_game_states(possible_next_moves))
        self.post_previous_move_state = self.get_best_state_transition(possible_next_states)[1]
        considered_moves = []
        for j in range(len(possible_next_states)):
            if tuple(possible_next_states[j]) == self.post_previous_move_state:
                considered_moves.append(possible_next_moves[j])
        return considered_moves[random.randint(0, len(considered_moves) - 1)]