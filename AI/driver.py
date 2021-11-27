from alpha_beta import AlphaBeta
from q_learning import Q_Learning_AI
from utility_functions import play_n_games, pretty_outcome_display, plot_end_game_information
from matplotlib.pyplot import show

LEARNING_RATE = .005
DISCOUNT_FACTOR = .3
NUM_GAMES_TO_TRAIN = 100
NUM_TRAINING_ROUNDS = 5
NUM_VALIDATION_GAMES = 5
NUM_GAMES_TO_TEST = 0
TRAINING_RANDOM_MOVE_PROBABILITY = .25
ALPHA_BETA_DEPTH = 2
TRAINING_MOVE_LIMIT = 500
VALIDATION_MOVE_LIMIT = 1000
TESTING_MOVE_LIMIT = 2000
PLAYER1 = Q_Learning_AI(True, LEARNING_RATE, DISCOUNT_FACTOR,
                        the_random_move_probability=TRAINING_RANDOM_MOVE_PROBABILITY)  # , info_location="data.json")
PLAYER2 = AlphaBeta(False, ALPHA_BETA_DEPTH)
# PLAYER3 = Alpha_beta(False, 1)
PLAYER4 = AlphaBeta(False, 3)
# PLAYER5 = Q_Learning_AI(False, LEARNING_RATE, DISCOUNT_FACTOR, the_random_move_probability=TRAINING_RANDOM_MOVE_PROBABILITY)


# PLAYER1.print_transition_information(PLAYER1.get_transitions_information())

training_info = []
validation_info = []
for j in range(NUM_TRAINING_ROUNDS):
    training_info.extend(play_n_games(PLAYER1, PLAYER2, NUM_GAMES_TO_TRAIN, TRAINING_MOVE_LIMIT))
    PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
    PLAYER1.set_random_move_probability(0)
    PLAYER1.set_learning_rate(0)
    validation_info.extend(play_n_games(PLAYER1, PLAYER4, NUM_VALIDATION_GAMES, VALIDATION_MOVE_LIMIT))
    print("Round " + str(j + 1) + " completed!")
    PLAYER1.set_random_move_probability(TRAINING_RANDOM_MOVE_PROBABILITY)
    PLAYER1.set_learning_rate(LEARNING_RATE)
    # print("")
    # PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
    print("")
    PLAYER1.save_transition_information()

plot_end_game_information(training_info, NUM_GAMES_TO_TRAIN, "Training Information")
plot_end_game_information(validation_info, NUM_VALIDATION_GAMES, "Validation Information")
show()

pretty_outcome_display(training_info)
print("")
pretty_outcome_display(validation_info)

"""

PLAYER1.set_random_move_probability(0)
pretty_outcome_display(play_n_games(PLAYER1, PLAYER2, NUM_GAMES_TO_TEST, TESTING_MOVE_LIMIT))
PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
print(" ")
pretty_outcome_display(play_n_games(PLAYER1, PLAYER3, NUM_GAMES_TO_TEST, TESTING_MOVE_LIMIT))
PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
print(" ")
pretty_outcome_display(play_n_games(PLAYER1, PLAYER4, NUM_GAMES_TO_TEST, TESTING_MOVE_LIMIT))
PLAYER1.print_transition_information(PLAYER1.get_transitions_information())

"""

PLAYER1.save_transition_information()