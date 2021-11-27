import matplotlib.pyplot as plt
import datetime
from board import CheckerBoard

global logFile
def reward_function(state_info1, state_info2):
    """
    Reward for transitioning from state with state_info1 to state with state_info2.

    NOTE:
    1) do something better with where/how this is implemented
    2) should give some kind of negative for tieing
    """
    if state_info2[1] == 0 and state_info2[3] == 0:
        return 12
    if state_info2[0] == 0 and state_info2[2] == 0:
        return -12
    return state_info2[0] - state_info1[0] + 2 * (state_info2[2] - state_info1[2]) - (
                state_info2[1] - state_info1[1]) - 2 * (state_info2[3] - state_info1[3])

def get_number_of_pieces_and_kings(spots, player_id=None):
    """
    Gets the number of pieces and the number of kings that each player has on the current
    board configuration represented in the given spots. The format of the function with defaults is:
    [P1_pieces, P2_pieces, P1_kings, P2_kings]
    and if given a player_id:
    [player_pieces, player_kings]
    """
    piece_counter = [0, 0, 0, 0]
    for row in spots:
        for element in row:
            if element != 0:
                piece_counter[element - 1] = piece_counter[element - 1] + 1

    if player_id == True:
        return [piece_counter[0], piece_counter[2]]
    elif player_id == False:
        return [piece_counter[1], piece_counter[3]]
    else:
        return piece_counter

def play_n_games(player1, player2, num_games, move_limit):
    """
    Plays a specified amount of games of checkers between player1, who goes first,
    and player2, who goes second.  The games will be stopped after the given limit on moves.
    This function outputs an array of arrays formatted as followed (only showing game 1's info):
    [[game1_outcome, num_moves, num_own_pieces, num_opp_pieces, num_own_kings, num_opp_kings]...]
    gameN_outcome is 0 if player1 won, 1 if lost, 2 if tied, and 3 if hit move limit.

    PRECONDITIONS:
    1)Both player1 and player2 inherit the Player class
    2)Both player1 and player2 play legal moves only
    """
    game_board = CheckerBoard()
    player1.set_board(game_board)
    player2.set_board(game_board)

    players_move = player1
    outcome_counter = [[-1, -1, -1, -1, -1, -1] for j in range(num_games)]
    for j in range(num_games):
        # print(j)
        move_counter = 0
        while not game_board.check_game_finished() and move_counter < move_limit:
            game_board.executeMove(players_move.get_next_move())

            move_counter = move_counter + 1
            if players_move is player1:
                players_move = player2
            else:
                players_move = player1
        else:
            piece_counter = get_number_of_pieces_and_kings(game_board.slots)
            if piece_counter[0] != 0 or piece_counter[2] != 0:
                if piece_counter[1] != 0 or piece_counter[3] != 0:
                    if move_counter == move_limit:
                        outcome_counter[j][0] = 3
                    else:
                        outcome_counter[j][0] = 2
                #                     if (j+1)%100==0:
                #                         print("Tie game for game #" + str(j + 1) + " in " + str(move_counter) + " turns!")
                else:
                    outcome_counter[j][0] = 0
            #                     if (j+1)%100==0:
            #                         print("Player 1 won game #" + str(j + 1) + " in " + str(move_counter) + " turns!")
            else:
                outcome_counter[j][0] = 1
            #                 if (j+1)%100==0:
            #                     print("Player 2 won game #" + str(j + 1) + " in " + str(move_counter) + " turns!")

            outcome_counter[j][1] = move_counter
            outcome_counter[j][2] = piece_counter[0]
            outcome_counter[j][3] = piece_counter[1]
            outcome_counter[j][4] = piece_counter[2]
            outcome_counter[j][5] = piece_counter[3]

            player1.game_completed()
            player2.game_completed()
            # game_board.print_board()
            game_board.game_reset()

    return outcome_counter

def start_logging(fileName):
    global logFile
    logFile = open(fileName, "w")
    logFile.write("Starting logging: "+str(datetime.datetime.now())+"\n")

def close_logFile():
    global logFile
    logFile.write("Ending logging session "+str(datetime.datetime.now())+"\n")
    logFile.close()

def pretty_outcome_display(outcomes):
    """
    Prints the outcome of play_n_games in a easy to understand format.

    TO DO:
    1) Add functionality for pieces in each game
    2) Add ability to take other strings for AI info and display it
    """
    game_wins = [0, 0, 0, 0]
    total_moves = 0
    max_moves_made = float("-inf")
    min_moves_made = float("inf")
    for outcome in outcomes:
        total_moves = total_moves + outcome[1]
        if outcome[1] < min_moves_made:
            min_moves_made = outcome[1]
        if outcome[1] > max_moves_made:
            max_moves_made = outcome[1]

        game_wins[outcome[0]] = game_wins[outcome[0]] + 1

    print("Games Played: ".ljust(35), len(outcomes))
    print("Player 1 wins: ".ljust(35), game_wins[0])
    print("Player 2 wins: ".ljust(35), game_wins[1])
    print("Games exceeded move limit: ".ljust(35), game_wins[3])
    print("Games tied: ".ljust(35), game_wins[2])
    print("Total moves made: ".ljust(35), total_moves)
    print("Average moves made: ".ljust(35), total_moves / len(outcomes))
    print("Max moves made: ".ljust(35), max_moves_made)
    print("Min moves made: ".ljust(35), min_moves_made)


def plot_end_game_information(outcome, interval, title="End of Game Results"):
    """
    """
    player1_wins = [0 for _ in range(int(len(outcome) / interval))]
    player2_wins = [0 for _ in range(int(len(outcome) / interval))]
    ties = [0 for _ in range(int(len(outcome) / interval))]
    move_limit = [0 for _ in range(int(len(outcome) / interval))]

    for j in range(int(len(outcome) / interval)):
        for i in range(interval):
            if outcome[j * interval + i][0] == 0:
                player1_wins[j] = player1_wins[j] + 1
            elif outcome[j * interval + i][0] == 1:
                player2_wins[j] = player2_wins[j] + 1
            elif outcome[j * interval + i][0] == 2:
                ties[j] = ties[j] + 1
            else:
                move_limit[j] = move_limit[j] + 1

    plt.figure(title)

    p1_win_graph, = plt.plot(player1_wins, label="Player 1 wins")
    p2_win_graph, = plt.plot(player2_wins, label="Player 2 wins")
    tie_graph, = plt.plot(ties, label="Ties")
    move_limit_graph, = plt.plot(move_limit, label="Move limit reached")

    plt.ylabel("Occurance per " + str(interval) + " games")
    plt.xlabel("Interval")

    plt.legend(handles=[p1_win_graph, p2_win_graph, tie_graph, move_limit_graph])
