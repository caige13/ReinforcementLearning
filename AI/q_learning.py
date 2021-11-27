from player import Player
import random
from utility_functions import reward_function
import json
from ast import literal_eval

class Q_Learning_AI(Player):
    """
    TO-DO:
    1) add ability to not train when wanted in a more efficient way
        A) when not training also don't look for/add currently unknown states
        B) do this by having an instance variable saying if it's testing or training
        C) and let a function set that parameter
    2) handle the rewards function which is coded as if the function were already defined
    """

    def __init__(self, the_player_id, the_learning_rate, the_discount_factor, info_location=None,
                 the_random_move_probability=0, the_board=None):
        """
        Initialize the instance variables to be stored by the AI.
        """
        self.random_move_probability = the_random_move_probability
        self.learning_rate = the_learning_rate
        self.discount_factor = the_discount_factor
        self.player_id = the_player_id
        self.board = the_board
        self.pre_last_move_state = None
        self.post_last_move_state = None
        if not info_location is None:
            self.load_transition_information(info_location)
        else:
            self.transitions = {}

    def set_random_move_probability(self, probability):
        """
        Sets the random move probability for the AI.
        """
        self.random_move_probability = probability

    def set_learning_rate(self, the_learning_rate):
        """
        Sets the learning rate for the AI.
        """
        self.learning_rate = the_learning_rate

    def get_states_from_boards_spots(self, boards_spots):
        """
        Gets an array of tuples from the given set of board spots,
        each tuple representing the characteristics which define the
        state the board is in.

        Format of returned data:
        [(own_pieces, opp_pieces, own_kings, opp_kings, own_edges, own_vert_center_mass, opp_vert_center_mass), ...]
        """
        piece_counters = [[0, 0, 0, 0, 0, 0, 0] for j in range(len(boards_spots))]
        for k in range(len(boards_spots)):
            for j in range(len(boards_spots[k])):
                for i in range(len(boards_spots[k][j])):
                    if boards_spots[k][j][i] != 0:
                        piece_counters[k][boards_spots[k][j][i] - 1] = piece_counters[k][boards_spots[k][j][i] - 1] + 1
                        if (self.player_id and (boards_spots[k][j][i] == 1 or boards_spots[k][j][i] == 3)) or (
                                not self.player_id and (boards_spots[k][j][i] == 2 or boards_spots[k][j][i] == 4)):
                            if i == 0 and j % 2 == 0:
                                piece_counters[k][4] = piece_counters[k][4] + 1
                            elif i == 3 and j % 2 == 1:
                                piece_counters[k][4] = piece_counters[k][4] + 1

                            piece_counters[k][5] = piece_counters[k][5] + j
                        else:
                            piece_counters[k][6] = piece_counters[k][6] + j

            if piece_counters[k][0] + piece_counters[k][2] != 0:
                piece_counters[k][5] = int(piece_counters[k][5] / (piece_counters[k][0] + piece_counters[k][2]))
            else:
                piece_counters[k][5] = 0
            if piece_counters[k][1] + piece_counters[k][3] != 0:
                piece_counters[k][6] = int(piece_counters[k][6] / (piece_counters[k][1] + piece_counters[k][3]))
            else:
                piece_counters[k][6] = 0

        return [tuple(counter) for counter in piece_counters]

    def get_desired_transition_between_states(self, possible_state_array,
                                              initial_transition_value=10):  # %%%%%%%%%%%%%%%%%% FOR (1)
        """
        Gets the desired transition to taken for the current board configuration.
        If any possible transition does not exist, it will create it.
        """
        cur_state = tuple(self.get_states_from_boards_spots([self.board.slots])[0])
        done_transitions = {}
        for state in possible_state_array:  # %%%%%%%%%%%%%%%%%%%%%% FOR (1)
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

    def game_completed(self):
        """
        Update self.transitions with a completed game before the board
        is cleared.
        """
        cur_state = self.get_states_from_boards_spots([self.board.slots])[0]
        transition = (self.pre_last_move_state, self.post_last_move_state)

        self.transitions[transition] = self.transitions[transition] + self.learning_rate * reward_function(
            transition[0], cur_state)

        self.pre_last_move_state = None
        self.post_last_move_state = None

    def get_transitions_information(self):
        """
        Get an array of of information about the dictionary self.transitions .
        It returns the information in the form:
        [num_transitions, num_start_of_transitions, avg_value, max_value, min_value]

        NOTES:
        1) Should use a dictionary here so this runs much faster
        """
        start_of_transitions = {}
        max_value = float("-inf")
        min_value = float("inf")
        total_value = 0
        for k, v in self.transitions.items():
            if start_of_transitions.get(k[0]) is None:
                start_of_transitions.update({k[0]: 0})
            # if k[0] not in start_of_transitions:
            # start_of_transitions.append(k[0])
            if v > max_value:
                max_value = v
            if v < min_value:
                min_value = v
            total_value = total_value + v

        return [len(self.transitions), len(start_of_transitions), float(total_value / len(self.transitions)), max_value,
                min_value]

    def print_transition_information(self, info):
        """
        Prints the output of get_transitions_information in a easy to understand format.
        """
        print("Total number of transitions: ".ljust(35), info[0])
        print("Total number of visited states: ".ljust(35), info[1])
        print("Average value for transition: ".ljust(35), info[2])
        print("Maximum value for transition: ".ljust(35), info[3])
        print("Minimum value for transition: ".ljust(35), info[4])

    def save_transition_information(self, file_name="data.json"):
        """
        Saves the current transitions information to a specified
        json file.
        """
        with open(file_name, 'w') as fp:
            json.dump({str(k): v for k, v in self.transitions.items()}, fp)

    def load_transition_information(self, file_name):
        """
        Loads transitions information from a desired json file.
        """
        with open(file_name, 'r') as fp:
            self.transitions = {literal_eval(k): v for k, v in json.load(fp).items()}

    def get_optimal_potential_value(self, depth):
        """
        Look ahead a given number of moves and return the maximal value associated
        with a move of that depth.

        STRATEGY:
        1) Look forward in (actual) own transition states.
        2) Look at board as self being the opponent and look forward in that situations transition states
        3) If not at depth go back to step (1)

        TODO:
        1) Approach this with algorithm similar to how minimax works
            a) look for set of transitions from (I think) current state of length depth by doing minimax
            b) Might also use alpha-beta pruning

        NOTES:
        1) depth is not actually looking ahead in possible moves, but actually simulating something similar (hopefully similar)
        2) ONLY WORKS FOR DEPTH OF 1 RIGHT NOW
        """
        answer = float("-inf")
        cur_state = self.get_states_from_boards_spots([self.board.slots])[0]
        for k, v in self.transitions.items():
            if v > answer and k[0] == cur_state:
                answer = v

        if answer == float("-inf"):
            return None
        return answer

    def get_next_move(self):  # , new_board):
        """
        NOTES:
        If the variable names are confusing, think about them being named when you just call the method.

        PRECONDITIONS:
        1)  The board exists and is legal
        """
        if self.pre_last_move_state is not None:  # %%%%%%%%%%%%%%%%%%%%%%% FOR (1)
            cur_state = self.get_states_from_boards_spots([self.board.slots])[0]

            transition = (self.pre_last_move_state, self.post_last_move_state)
            try:  # self.transitions.get(transition) is not None:#%%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
                max_future_state = self.get_optimal_potential_value(1)
                self.transitions[transition] = self.transitions[transition] + self.learning_rate * (
                            reward_function(transition[0], cur_state) + self.discount_factor * max_future_state -
                            self.transitions[transition])
            except:  # %%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)
                self.transitions[transition] = self.transitions[transition] + self.learning_rate * (
                    reward_function(transition[0], cur_state))

        self.pre_last_move_state = self.get_states_from_boards_spots([self.board.slots])[
            0]  # %%%%%%%%%%%%%%%%%%%%%%%%%%%% FOR (1)

        possible_next_moves = self.board.get_moves_available()
        possible_next_states = self.get_states_from_boards_spots(
            self.board.get_new_game_states(possible_next_moves))

        self.post_last_move_state = self.get_desired_transition_between_states(possible_next_states)[1]

        considered_moves = []
        for j in range(len(possible_next_states)):
            if tuple(possible_next_states[j]) == self.post_last_move_state:
                considered_moves.append(possible_next_moves[j])

        # I believe with the updated board.is_game_over() I don't need to use this try statement
        #         try:
        #             return considered_moves[random.randint(0,len(considered_moves)-1)]
        #         except ValueError:
        #             return []

        return considered_moves[random.randint(0, len(considered_moves) - 1)]