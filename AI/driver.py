import matplotlib.pyplot as plt
from global_logging import file
from alpha_beta import AlphaBeta
from q_learning import QLearningAI
from utility_functions import PlayNGames, PrintOutcome, PlotEndGameInformation

parameters = {'learning_rate': [.001, .005], 'discount_factor': .7, 'num_train_games': [100, 200],
              'num_train_rounds': [5, 20], 'num_validation_games': 5, 'num_test_games': 5, 'random_move_chance': .1,
              'alpha_beta_depth': 2, 'move_limit': [500, 1000]}
# parameters = {'learning_rate': [.001], 'discount_factor': .4, 'num_train_games': [100],
#               'num_train_rounds': [5], 'num_validation_games': 5, 'num_test_games': 5, 'random_move_chance': .1,
#               'alpha_beta_depth': 2, 'move_limit': [500]}

logFile = open(file, "w")
logFile.write("___________________________________________________________________________________________\n")
logFile.write("|   Exp.   |         Hyper Parameter        |                   Results                   |\n")
logFile.write("|__________|________________________________|_____________________________________________|\n")
logFile.close()

experimentCount = 0
training_info = []
validation_info = []
for learningRate in parameters['learning_rate']:
    for numTrainGames in parameters['num_train_games']:
        for moveLimit in parameters['move_limit']:
            for numTrainRound in parameters['num_train_rounds']:
                experimentCount += 1
                log_param = {'learning_rate': learningRate, 'discount_factor': .4, 'num_train_games': numTrainGames,
              'num_train_rounds': numTrainRound, 'num_validation_games': 5, 'num_test_games': 5, 'random_move_chance': .1,
              'alpha_beta_depth': 2, 'move_limit': moveLimit}
                print("________________")
                print("Parameter Change")
                print("________________")
                print("Learn Rate: "+str(learningRate))
                print("number of train games: "+str(numTrainGames))
                print("move limit: "+str(moveLimit))
                print("number of train rounds: "+str(numTrainRound)+"\n")
                PLAYER1 = QLearningAI(True, learningRate, parameters['discount_factor'],
                                      randomMoveChance=parameters['random_move_chance'])
                                        # , dataLoc="data.json")
                PLAYER2 = AlphaBeta(False, parameters['alpha_beta_depth'])
                PLAYER4 = AlphaBeta(False, 3)
                training_info = []
                validation_info = []
                for j in range(numTrainRound):
                    training_info.extend(PlayNGames(PLAYER1, PLAYER2, numTrainGames, moveLimit))
                    PLAYER1.print_transition_info(PLAYER1.get_transitions_info())
                    PLAYER1.set_likelihood_random_move_(0)
                    PLAYER1.set_learning_rate(0)
                    validation_info.extend(PlayNGames(PLAYER1, PLAYER4, parameters['num_validation_games'],
                                                        moveLimit))
                    print("Round " + str(j + 1) + " completed!")
                    PLAYER1.set_likelihood_random_move_(parameters['random_move_chance'])
                    PLAYER1.set_learning_rate(learningRate)
                    print("")
                    PLAYER1.save_transition_information()
                PlotEndGameInformation(training_info, numTrainGames, "Training Information")
                plt.savefig("Graphs/Train_stepsize" + str(learningRate) + "_trainGames" + str(numTrainGames) +
                            "_moveLimit" + str(moveLimit) + "_numRound" + str(numTrainRound) + ".png")
                plt.show()
                PlotEndGameInformation(validation_info, parameters['num_validation_games'], "Validation Information")
                plt.savefig("Graphs/Validate_stepsize"+str(learningRate)+"_trainGames"+str(numTrainGames)+
                                                     "_moveLimit"+str(moveLimit)+"_numRound"+str(numTrainRound)+".png")
                plt.show()
                PLAYER1.save_transition_information()
                PrintOutcome(training_info, log_param, experimentCount, "train")
                print("")
                PrintOutcome(validation_info, log_param, experimentCount, "validation")