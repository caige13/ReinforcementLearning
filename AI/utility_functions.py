import matplotlib.pyplot as plt
from global_logging import file
from board import CheckerBoard

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

# Plays n games of checkers, games stop after given move limit
# outputs arrays in format of
# [[game_outcome, num_moves, num_own_pieces, num_opp_pieces, num_own_kings, num_opp_kings]...]
def PlayNGames(p1, p2, gamesToPlay, numMoveLimitation):
    board = CheckerBoard()
    # setting up players to play on same game board
    p2.set_checkersBoard(board)
    p1.set_checkersBoard(board)
    # initialize outcome with negatives
    gameOutcome = [[-1, -1, -1, -1, -1, -1] for j in range(gamesToPlay)]
    isPlayersTurn = p1
    for j in range(gamesToPlay):
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
                        gameOutcome[j][0] = 3
                    # Tie game
                    else:
                        gameOutcome[j][0] = 2
                # P1 won
                else:
                    gameOutcome[j][0] = 0
            # P2 won
            else:
                gameOutcome[j][0] = 1

            # Defining gameOutcome
            gameOutcome[j][5] = PieceCount['p2_king']
            gameOutcome[j][2] = PieceCount['p1_reg']
            gameOutcome[j][1] = moves
            gameOutcome[j][4] = PieceCount['p1_king']
            gameOutcome[j][3] = PieceCount['p2_reg']

            # do necessary resets to start new game
            p1.isGameFinished()
            p2.isGameFinished()
            board.game_reset()
    # Game outcome will hav the number of "rows" equal to the number of games played
    return gameOutcome

# prints the outcome of PlayNGames in nice format and logs it in the log file
def PrintOutcome(outcomes, log_param, experimentCount, type):
    logFile = open(file, "a")
    game_wins = [0, 0, 0, 0]
    format_param = ["step size: "+str(log_param['learning_rate']), "discount factor: "+str(log_param['discount_factor']),
                    "num of train games: "+str(log_param['num_train_games']),
                    "num of train rounds: "+str(log_param['num_train_rounds']),
                    "num of validation games: "+str(log_param['num_validation_games']),
                    "num of test games: "+str(log_param['num_test_games']),
                    "rand. move chance: "+str(log_param['random_move_chance']),
                    "Alpha-Beta Depth: "+str(log_param['alpha_beta_depth']), "move limit: "+str(log_param['move_limit'])]
    cumulative_mvs = 0
    max_mvs = float("-inf")
    min_mvs = float("inf")
    for outcome in outcomes:
        cumulative_mvs = cumulative_mvs + outcome[1]
        if outcome[1] < min_mvs:
            min_mvs = outcome[1]
        if outcome[1] > max_mvs:
            max_mvs = outcome[1]
        game_wins[outcome[0]] = game_wins[outcome[0]] + 1

    result_title = ["Games Played: ", "Num. games player1 won: ", "Num. games player2 won: ",
                    "Num. games move limit hit: ", "Num. games tied: ", "Total moves made: ",
                    "Average moves made: ", "Max move made (may be move limit): ",
                    "Min move made: "]
    result = [len(outcomes), game_wins[0], game_wins[1], game_wins[3], game_wins[2],
              cumulative_mvs, cumulative_mvs / len(outcomes), max_mvs, min_mvs]
    logFile.write("|{:^10}|{:^32}|{:^45}|\n".format(experimentCount, format_param[0],
                                                   result_title[0]+str(result[0])))
    logFile.write("|{:^10}|{:^32}|{:^45}|\n".format(type, format_param[1],
                                                    result_title[1] + str(result[1])))
    for i in range(2, len(format_param)):
        logFile.write("|{:^10}|{:^32}|{:^45}|\n".format("", format_param[i],
                                                                      result_title[i]+str(result[i])))
    logFile.write("|__________|________________________________|_____________________________________________|\n")
    logFile.close()
    for i in range(len(result)):
        print("{:35}".format(result_title[i]), result[i])

def PlotEndGameInformation(outcome, interval, title="End of Game Results"):
    p1_wins = [0 for _ in range(int(len(outcome) / interval))]
    p2_wins = [0 for _ in range(int(len(outcome) / interval))]
    ties = [0 for _ in range(int(len(outcome) / interval))]
    move_limit = [0 for _ in range(int(len(outcome) / interval))]
    for j in range(int(len(outcome) / interval)):
        for i in range(interval):
            if outcome[j * interval + i][0] == 0:
                p1_wins[j] = p1_wins[j] + 1
            elif outcome[j * interval + i][0] == 1:
                p2_wins[j] = p2_wins[j] + 1
            elif outcome[j * interval + i][0] == 2:
                ties[j] = ties[j] + 1
            else:
                move_limit[j] = move_limit[j] + 1
    plt.figure(title)
    p1_win_graph, = plt.plot(p1_wins, label="Player 1 is the winner!", color="blue")
    p2_win_graph, = plt.plot(p2_wins, label="Player 2 is the winner!", color="orange")
    tie_graph, = plt.plot(ties, label="Ties", color="green")
    move_limit_graph, = plt.plot(move_limit, label="Move limit has been reached", color="red")
    plt.ylabel("Occurance per " + str(interval) + " games")
    plt.xlabel("Interval")
    plt.legend(handles=[p1_win_graph, p2_win_graph, tie_graph, move_limit_graph])
