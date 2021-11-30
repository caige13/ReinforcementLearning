from checkersplayer import CheckersPlayer
import random
import math
from utility_functions import RewardPolicy
import json
from ast import literal_eval


class QLearningAI(CheckersPlayer):
    def __init__(self, turn, learningRate, discountFactor, dataLoc=None,
                 randomMoveChance=0, board=None):
        if not dataLoc is None:
            self.file_transition_info_load(dataLoc)
        else:
            self.transitions = {}
        # both before and after are used as kinda temporary variables when
        # evaluating the next move
        self.beforeMovState = None
        self.afterMovState = None

        # This is a term in RL that refers to dose the AI care about
        # immediate reward or long term rewards.
        self.discountFactor = discountFactor

        self.learningRate = learningRate
        self.checkersBoard = board

        # use this to determine if there should be a random move made
        # utilized during training.
        self.randomMoveChance = randomMoveChance
        self.id = turn

    # If the board exists and is legal then get the next move
    def get_next_move(self):
        # slight optimization of looking ahead.
        if not (self.beforeMovState is None):
            # Get current state
            currentState = self.get_state_with_board_slots([self.checkersBoard.slots])[0]
            # set up transition input for self.transition and reward function.
            transitionIndex = (self.beforeMovState, self.afterMovState)
            # when looking for next best move may return None which will cause error in math equation
            try:
                nextBestMove = self.get_best_forward_looking_value()
                self.transitions[transitionIndex] = self.transitions[transitionIndex] + self.learningRate * (
                        RewardPolicy(transitionIndex[0], currentState) + self.discountFactor * nextBestMove -
                        self.transitions[transitionIndex])
            except:
                self.transitions[transitionIndex] = self.transitions[transitionIndex] + self.learningRate * (
                    RewardPolicy(transitionIndex[0], currentState))
        # begin process of deciding move.
        self.beforeMovState = self.get_state_with_board_slots([self.checkersBoard.slots])[
            0]
        # Getting the new information as if we made the move
        nextAvailableMoves = self.checkersBoard.get_moves_available()
        nextAvailableStates = self.get_state_with_board_slots(
            self.checkersBoard.get_new_game_states(nextAvailableMoves))

        # getting information for when a move is made
        self.afterMovState = self.get_best_state_transition(nextAvailableStates)[1]
        considered_moves = []
        # loop through to determine the considered moves given a state
        for j in range(len(nextAvailableStates)):
            if tuple(nextAvailableStates[j]) == self.afterMovState:
                considered_moves.append(nextAvailableMoves[j])
        return considered_moves[random.randint(0, len(considered_moves) - 1)]

    # grabs the desired transition for current board config - if none exist it creates one
    def get_best_state_transition(self, allPossibleStates,
                                  initialTransValue=10):
        # Get the current state from the board with its slots.
        currentState = tuple(self.get_state_with_board_slots([self.checkersBoard.slots])[0])
        prevTransitions = {}
        for state in allPossibleStates:
            # updating the transition that drives the function
            if prevTransitions.get((currentState, tuple(state))) is None:
                # also updating the class transitions if not found.
                if self.transitions.get((currentState, tuple(state))) is None:
                    self.transitions.update({(currentState, tuple(state)): initialTransValue})
                prevTransitions.update({(currentState, tuple(state)): self.transitions.get((currentState, tuple(state)))})

        # Determine if random move based off the randomMoveChance, also checks edge case of 0%
        if  random.random() < self.randomMoveChance and random != 0:
            # need the try catch because a transition may be None.
            try:
                return list(prevTransitions.keys())[random.randint(0, len(prevTransitions) - 1)]
            except:
                return []

        # expected return value is to reverse the key value
        try:
            backwardTransitions = {j: i for i, j in prevTransitions.items()}
            return backwardTransitions.get(max(backwardTransitions))
        except:
            return []

    # grabs a tuple array from the inputted board spots -each tuple represents characteristics to define the board state
    def get_state_with_board_slots(self, boardsSlots):
        pieceCount = [{'own_reg': 0, 'opp_reg': 0, 'own_edge_piece': 0, 'own_kings': 0,
                       'opp_kings': 0, 'own_vert_cent_mass': 0, 'opp_vert_cent_mass': 0}
                      for i in range(len(boardsSlots))]

        # for the most part the first forloop will only be ran once.
        for i in range(len(boardsSlots)):
            for row in range(len(boardsSlots[i])):
                for col in range(len(boardsSlots[i][row])):
                    # null checker
                    if boardsSlots[i][row][col] != 0:
                        # pieceCount is a two dimensional array
                        if boardsSlots[i][row][col] == 1:
                            pieceCount[i]['own_reg'] += 1
                        elif boardsSlots[i][row][col] == 2:
                            pieceCount[i]['opp_reg'] += 1
                        elif boardsSlots[i][row][col] == 3:
                            pieceCount[i]['own_kings'] += 1
                        elif boardsSlots[i][row][col] == 4:
                            pieceCount[i]['opp_kings'] += 1
                        if (not self.id and (boardsSlots[i][row][col] == 2 or boardsSlots[i][row][col] == 4)) \
                                or (self.id and (boardsSlots[i][row][col] == 1 or boardsSlots[i][row][col] == 3)):
                            if col == 0 and row % 2 == 0:
                                # Own piece on the edge
                                pieceCount[i]['own_edge_piece'] += 1
                            elif col == 3 and row % 2 == 1:
                                # Own piece on the edge
                                pieceCount[i]['own_edge_piece'] += 1
                            # update own center mass
                            pieceCount[i]['own_vert_cent_mass'] += row
                        else:
                            # update opponent's center mass
                            pieceCount[i]['opp_vert_cent_mass'] += row

            if pieceCount[i]['opp_reg'] + pieceCount[i]['opp_kings'] != 0:
                # update opponent's center mass
                pieceCount[i]['opp_vert_cent_mass'] = int(pieceCount[i]['opp_vert_cent_mass'] /
                                                          (pieceCount[i]['opp_reg'] + pieceCount[i]['opp_kings']))
            else:
                # update opponent's center mass
                pieceCount[i]['opp_vert_cent_mass'] = 0
            if pieceCount[i]['own_reg'] + pieceCount[i]['own_kings'] != 0:
                # update own center mass
                pieceCount[i]['own_vert_cent_mass'] = int(pieceCount[i]['own_vert_cent_mass'] /
                                                          (pieceCount[i]['own_reg'] + pieceCount[i]['own_kings']))
            else:
                # update own center mass
                pieceCount[i]['own_vert_cent_mass'] = 0

        # convert output to list of tuples
        returnValue = []
        for pieces in pieceCount:
            returnValue.append((pieces['own_reg'], pieces['opp_reg'], pieces['own_kings'],
                                pieces['opp_kings'], pieces['own_edge_piece'],
                                pieces['own_vert_cent_mass'], pieces['opp_vert_cent_mass']))
        return returnValue

    # sets the AI's learning rate
    def set_learning_rate(self, learningRate):
        self.learningRate = learningRate

    # Save our current transition information to json file
    def save_transition_information(self, file="dataset.json"):
        with open(file, 'w') as filePath:
            json.dump({str(key): value for key, value in self.transitions.items()}, filePath)

    # Get array of information about the dictionary self.transitions
    # in form num_transitions, num_start_of_transitions, avg_value, max_value, min_value]
    def get_transitions_info(self):
        begTransitions = {}
        # positive infinite initialization
        maxValue = -math.inf
        # negative infinite initialization
        minValue = math.inf
        cumulativeValue = 0

        # key value iteration
        for key, value in self.transitions.items():
            # Getting total value
            cumulativeValue = cumulativeValue + value
            # filling in blanks
            if begTransitions.get(key[0]) is None:
                begTransitions.update({key[0]: 0})
            # Get min value
            if value < minValue:
                minValue = value
            # Get max value
            if value > maxValue:
                maxValue = value

        return [len(self.transitions), len(begTransitions), float(cumulativeValue / len(self.transitions)),
                maxValue,
                minValue]

    # Load transition info from inputted json file
    # allows us to replicate an AI given a correctly formatted dataset
    def file_transition_info_load(self, file):
        with open(file, 'r') as filePath:
            self.transitions = {literal_eval(key): value for key, value in json.load(filePath).items()}

    # Look forward a inputted number of moves then return the best values associated with a move of that depth
    # Due to complexity the AI can only look at a depth of 1.
    def get_best_forward_looking_value(self):
        # gets the board current state
        currentState = self.get_state_with_board_slots([self.checkersBoard.spots])[0]
        solution = -math.inf
        # k short for key
        for k, value in self.transitions.items():
            # finding bigger values as a possible next move
            if value > solution and k[0] == currentState:
                solution = value
        # There was no found best move given the current state
        if solution == -math.inf:
            return None
        return solution

    # Prints the output of get transition_information to console
    def print_transition_info(self, info):
        result_title = ["Total transitions: ", "Total visited states: ", "Average value of transition: ",
                        "Maximum value of transition: ", "Minimum value of transition: "]
        for i in range(len(result_title)):
            print("{:35}".format(result_title[i]), str(info[i]))

    # update self.transition with a finished game before board clear
    def isGameFinished(self):
        # reset state
        currentState = self.get_state_with_board_slots([self.checkersBoard.slots])[0]
        transition = (self.beforeMovState, self.afterMovState)
        # reset values
        self.beforeMovState = None
        self.afterMovState = None

        self.transitions[transition] = self.transitions[transition] + self.learningRate * RewardPolicy(
            transition[0], currentState)

    # sets the AI's random move probability
    def set_likelihood_random_move_(self, probability):
        self.randomMoveChance = probability