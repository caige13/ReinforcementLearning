import math
import matplotlib.pyplot as plt
from global_logging import file
from board import CheckerBoard

# Grabs the number of pieces and kings that each player has currently
def GetPieces(spots, idPL=None):
    PieceCounter = {'p1_reg': 0, 'p1_king': 0, 'p2_reg': 0, 'p2_king': 0}
    for row in spots:
        for element in row:
            if element == 1:
                PieceCounter['p1_reg'] += 1
            elif element == 2:
                PieceCounter['p2_reg'] += 1
            elif element == 3:
                PieceCounter['p1_king'] += 1
            elif element == 4:
                PieceCounter['p2_king'] += 1
    if idPL == False:
        return [PieceCounter['p2_reg'], PieceCounter['p2_king']]
    elif idPL == True:
        return [PieceCounter['p1_reg'], PieceCounter['p1_king']]
    else:
        return PieceCounter



def PlotEndGameInformation(gameResults, gamesPlayedPerRound, title="End of Game Results"):
    tiedGames = [0 for i in range(int(len(gameResults) / gamesPlayedPerRound))]
    p1Wins = [0 for i in range(int(len(gameResults) / gamesPlayedPerRound))]
    moveLimitHit = [0 for i in range(int(len(gameResults) / gamesPlayedPerRound))]
    p2Wins = [0 for i in range(int(len(gameResults) / gamesPlayedPerRound))]
    for i in range(int(len(gameResults) / gamesPlayedPerRound)):
        for gameCount in range(gamesPlayedPerRound):
            if gameResults[i * gamesPlayedPerRound + gameCount]['game_outcome'] == 0:
                p1Wins[i] = p1Wins[i] + 1
            elif gameResults[i * gamesPlayedPerRound + gameCount]['game_outcome'] == 1:
                p2Wins[i] = p2Wins[i] + 1
            elif gameResults[i * gamesPlayedPerRound + gameCount]['game_outcome'] == 2:
                tiedGames[i] = tiedGames[i] + 1
            else:
                moveLimitHit[i] = moveLimitHit[i] + 1
    plt.figure(title)
    plotTieGames, = plt.plot(tiedGames, label="Ties", color="green")
    plotP1Wins, = plt.plot(p1Wins, label="Player 1 is the winner!", color="blue")
    plotMoveLimitHit, = plt.plot(moveLimitHit, label="Move limit has been reached", color="red")
    plotP2Wins, = plt.plot(p2Wins, label="Player 2 is the winner!", color="orange")
    plt.ylabel("Occurance per " + str(gamesPlayedPerRound) + " games")
    plt.xlabel("Interval")
    plt.legend(handles=[plotP1Wins, plotP2Wins, plotTieGames, plotMoveLimitHit])

# function rewards for transitioning from one input state to the other
def RewardPolicy(preStateInformation, postStateInformation):
    winReward = 14
    if postStateInformation[2] == 0 and postStateInformation[0] == 0:
        return -winReward
    if  postStateInformation[3] == 0 and postStateInformation[1] == 0:
        return winReward
    intermediateReward = postStateInformation[0] - preStateInformation[0] + 2 * \
                            (postStateInformation[2] - preStateInformation[2]) - (
                                postStateInformation[1] - preStateInformation[1]) - 2 * (
                                postStateInformation[3] - preStateInformation[3])
    return intermediateReward

# Plays n games of checkers, games stop after given move limit
# outputs arrays in format of
# [[game_outcome, num_moves, num_own_pieces, num_opp_pieces, num_own_kings, num_opp_kings]...]
def PlayNGames(p1, p2, gamesToPlay, numMoveLimitation):
    board = CheckerBoard()
    # setting up players to play on same game board
    p2.set_checkersBoard(board)
    p1.set_checkersBoard(board)
    # initialize outcome with negatives
    gameResults = [{'game_outcome':-1, 'move_count':-1, 'p1_reg': -1,
                    'p2_reg':-1, 'p1_king':-1, 'p2_king':-1} for j in range(gamesToPlay)]
    isPlayersTurn = p1
    for gameNum in range(gamesToPlay):
        moves = 0
        # play the actual game
        while not board.check_game_finished() and moves < numMoveLimitation:
            board.execute_move(isPlayersTurn.get_next_move())
            moves = moves + 1
            # swap the players
            if isPlayersTurn is p2:
                isPlayersTurn = p1
            elif isPlayersTurn is p1:
                isPlayersTurn = p2
            # This case should never happen
            else:
                print("ERROR")
                exit(1)
        else:
            # contain the regular pieces and king counts for both players
            PieceCount = GetPieces(board.slots)
            if PieceCount['p1_reg'] != 0 or PieceCount['p1_king'] != 0:
                if PieceCount['p2_reg'] != 0 or PieceCount['p2_king'] != 0:
                    # max move limit hit
                    if moves == numMoveLimitation:
                        gameResults[gameNum]['game_outcome'] = 3
                    # Tie game
                    else:
                        gameResults[gameNum]['game_outcome'] = 2
                # P1 won
                else:
                    gameResults[gameNum]['game_outcome'] = 0
            # P2 won
            else:
                gameResults[gameNum]['game_outcome'] = 1

            # Defining gameOutcome
            gameResults[gameNum]['p2_king'] = PieceCount['p2_king']
            gameResults[gameNum]['p1_reg'] = PieceCount['p1_reg']
            gameResults[gameNum]['move_count'] = moves
            gameResults[gameNum]['p1_king'] = PieceCount['p1_king']
            gameResults[gameNum]['p2_reg'] = PieceCount['p2_reg']

            # do necessary resets to start new game
            p1.isGameFinished()
            p2.isGameFinished()
            board.game_reset()
    # Game outcome will hav the number of "rows" equal to the number of games played
    return gameResults

# prints the outcome of PlayNGames in nice format and logs it in the log file
def PrintOutcome(gameResults, logParam, experimentCount, type):
    logFile = open(file, "a")
    gameWins = [0, 0, 0, 0]
    formatParam = ["step size: " + str(logParam['learning_rate']), "discount factor: " + str(logParam['discount_factor']),
                    "num of train games: " + str(logParam['num_train_games']),
                    "num of train rounds: " + str(logParam['num_train_rounds']),
                    "num of validation games: " + str(logParam['num_validation_games']),
                    "num of test games: " + str(logParam['num_test_games']),
                    "rand. move chance: " + str(logParam['random_move_chance']),
                    "Alpha-Beta Depth: " + str(logParam['alpha_beta_depth']), "move limit: " + str(logParam['move_limit'])]
    cumulativeMvs = 0
    maxMvs = -math.inf
    minMvs = math.inf
    for outcome in gameResults:
        cumulativeMvs = cumulativeMvs + outcome['move_count']
        if outcome['move_count'] > maxMvs:
            maxMvs = outcome['move_count']
        if outcome['move_count'] < minMvs:
            minMvs = outcome['move_count']
        gameWins[outcome['game_outcome']] = gameWins[outcome['game_outcome']] + 1

    resultTitle = ["Games Played: ", "Num. games player1 won: ", "Num. games player2 won: ",
                    "Num. games move limit hit: ", "Num. games tied: ", "Total moves made: ",
                    "Average moves made: ", "Max move made (may be move limit): ",
                    "Min move made: "]
    result = [len(gameResults), gameWins[0], gameWins[1], gameWins[3], gameWins[2],
              cumulativeMvs, cumulativeMvs / len(gameResults), maxMvs, minMvs]
    logFile.write("|{:^10}|{:^32}|{:^45}|\n".format(experimentCount, formatParam[0],
                                                   resultTitle[0]+str(result[0])))
    logFile.write("|{:^10}|{:^32}|{:^45}|\n".format(type, formatParam[1],
                                                    resultTitle[1] + str(result[1])))
    for i in range(2, len(formatParam)):
        logFile.write("|{:^10}|{:^32}|{:^45}|\n".format("", formatParam[i],
                                                                      resultTitle[i]+str(result[i])))
    logFile.write("|__________|________________________________|_____________________________________________|\n")
    logFile.close()
    for i in range(len(result)):
        print("{:35}".format(resultTitle[i]), result[i])


