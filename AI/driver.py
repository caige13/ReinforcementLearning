import datetime
import matplotlib.pyplot as plt

# Establishing global logFile to use across the project
logFile = open("LogFile.txt", "w")
logFile.write("Starting logging: "+str(datetime.datetime.now())+"\n")

from alpha_beta import AlphaBeta
from q_learning import QLearningAI
from utility_functions import PlayNGames, PrintOutcome, PlotEndGameInformation
from matplotlib.pyplot import show

parameters = {'learning_rate': [.001, .005, .1], 'discount_factor': .4, 'num_train_games': [100, 200],
              'num_train_rounds': [5, 25], 'num_validation_games': 5, 'num_test_games': 5, 'random_move_chance': .1,
              'alpha_beta_depth': 2, 'move_limit': [500, 1000]}
training_info = []
validation_info = []

logFile.write("________________________________________________________________________\n")
logFile.write("|  Experiment  |      Hyper Parameter      |          Results          |\n")
logFile.write("|______________|___________________________|___________________________|\n")

for learningRate in parameters['learning_rate']:
    for numTrainGames in parameters['num_train_games']:
        for moveLimit in parameters['move_limit']:
            for numTrainRound in parameters['num_train_rounds']:
                print("________________")
                print("Parameter Change")
                print("________________")
                PLAYER1 = Q_Learning_AI(True, learningRate, parameters['discount_factor'],
                                        the_random_move_probability=parameters['random_move_chance'])
                                        # , info_location="data.json")
                PLAYER2 = AlphaBeta(False, parameters['alpha_beta_depth'])
                # PLAYER3 = Alpha_beta(False, 1)
                PLAYER4 = AlphaBeta(False, 3)
                # PLAYER5 = Q_Learning_AI(False, learningRate, parameter['discount_factor'],
                # the_random_move_probability=parameter['random_move_chance'])
                training_info = []
                validation_info = []
                for j in range(numTrainRound):
                    training_info.extend(play_n_games(PLAYER2, PLAYER1, numTrainGames, moveLimit))
                    PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
                    PLAYER1.set_random_move_probability(0)
                    PLAYER1.set_learning_rate(0)
                    validation_info.extend(play_n_games(PLAYER4, PLAYER1, parameters['num_validation_games'],
                                                        moveLimit))
                    print("Round " + str(j + 1) + " completed!")
                    PLAYER1.set_random_move_probability(parameters['random_move_chance'])
                    PLAYER1.set_learning_rate(learningRate)
                    # print("")
                    # PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
                    print("")
                    PLAYER1.save_transition_information()
                # PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
                plot_end_game_information(training_info, numTrainGames, "Training Information")
                plot_end_game_information(validation_info, parameters['num_validation_games'], "Validation Information")
                plt.savefig("../Graphs/stepsize"+str(learningRate)+";trainGames:"+str(numTrainGames)+
                                                     ";moveLimit:"+str(moveLimit)+";numRound"+str(numTrainRound))

LEARNING_RATE = .001
DISCOUNT_FACTOR = .4
NUM_GAMES_TO_TRAIN = 100
NUM_TRAINING_ROUNDS = 5
NUM_VALIDATION_GAMES = 5
NUM_GAMES_TO_TEST = 0
TRAINING_RANDOM_MOVE_PROBABILITY = .05
ALPHA_BETA_DEPTH = 2
TRAINING_MOVE_LIMIT = 500
VALIDATION_MOVE_LIMIT = 1000
TESTING_MOVE_LIMIT = 2000


# PLAYER1.print_transition_information(PLAYER1.get_transitions_information())
plot_end_game_information(training_info, NUM_GAMES_TO_TRAIN, "Training Information")
plot_end_game_information(validation_info, NUM_VALIDATION_GAMES, "Validation Information")
show()

PrintOutcome(training_info)
print("")
PrintOutcome(validation_info)

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
logFile.close()
PLAYER1.save_transition_information()
