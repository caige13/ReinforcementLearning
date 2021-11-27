
import matplotlib.pyplot as plt
from board import Board

# function rewards for transitioning from one input state to the other
def RewardFunction(state1_info, state2_info):
    if state2_info[1] == 0 and state2_info[3] == 0:
        return 12
    if state2_info[0] == 0 and state2_info[2] == 0:
        return -12
    return state2_info[0] - state1_info[0] + 2 * (state2_info[2] - state1_info[2]) - (
            state2_info[1] - state1_info[1]) - 2 * (state2_info[3] - state1_info[3])

# Grabs the number of pieces and kings that each player has currently
# output in form [P1_pieces, P2_pieces, P1_kings, P2_kings]
def GetPieces(spots, pl_id=None):
    PieceCounter = [0, 0, 0, 0]
    for row in spots:
        for element in row:
            if element != 0:
                PieceCounter[element - 1] = PieceCounter[element - 1] + 1
    if pl_id:
        return [PieceCounter[0], PieceCounter[2]]
    elif not pl_id:
        return [PieceCounter[1], PieceCounter[3]]
    else:
        return PieceCounter

# Plays n games of checkers, games stop after given move limit
# outputs arrays in format of
# [[game1_outcome, num_moves, num_own_pieces, num_opp_pieces, num_own_kings, num_opp_kings]...]
def PlayNGames(p1, p2, num_games, mv_limit):
    game_board = Board()
    p1.set_board(game_board)
    p2.set_board(game_board)
    players_mv = p1
    outcome_counter = [[-1, -1, -1, -1, -1, -1] for j in range(num_games)]
    for j in range(num_games):
        move_counter = 0
        while not game_board.check_game_finished() and move_counter < mv_limit:
            game_board.execute_move(players_mv.get_next_move())
            move_counter = move_counter + 1
            if players_mv is p1:
                players_mv = p2
            else:
                players_mv = p1
        else:
            piece_counter = GetPieces(game_board.spots)
            if piece_counter[0] != 0 or piece_counter[2] != 0:
                if piece_counter[1] != 0 or piece_counter[3] != 0:
                    if move_counter == mv_limit:
                        outcome_counter[j][0] = 3
                    else:
                        outcome_counter[j][0] = 2
                else:
                    outcome_counter[j][0] = 0
            else:
                outcome_counter[j][0] = 1
            outcome_counter[j][1] = move_counter
            outcome_counter[j][2] = piece_counter[0]
            outcome_counter[j][3] = piece_counter[1]
            outcome_counter[j][4] = piece_counter[2]
            outcome_counter[j][5] = piece_counter[3]
            p1.game_completed()
            p2.game_completed()
            game_board.game_reset()
    return outcome_counter

# prints the outcome of PlayNGames in nice format
def PrintOutcome(outcomes):
    game_wins = [0, 0, 0, 0]
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
    print("Games Played: ".ljust(35), len(outcomes))
    print("Player 1 is the winner: ".ljust(35), game_wins[0])
    print("Player 2 is the winner: ".ljust(35), game_wins[1])
    print("Games have exceeded move limit: ".ljust(35), game_wins[3])
    print("Number of games tied: ".ljust(35), game_wins[2])
    print("Total moves that were made: ".ljust(35), cumulative_mvs)
    print("Average moves that were made: ".ljust(35), cumulative_mvs / len(outcomes))
    print("Max moves that were made: ".ljust(35), max_mvs)
    print("Min moves that were made: ".ljust(35), min_mvs)


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
    p1_win_graph, = plt.plot(p1_wins, label="Player 1 is the winner!")
    p2_win_graph, = plt.plot(p2_wins, label="Player 2 is the winner!")
    tie_graph, = plt.plot(ties, label="Ties")
    move_limit_graph, = plt.plot(move_limit, label="Move limit has been reached")
    plt.ylabel("Occurance per " + str(interval) + " games")
    plt.xlabel("Interval")
    plt.legend(handles=[p1_win_graph, p2_win_graph, tie_graph, move_limit_graph])
