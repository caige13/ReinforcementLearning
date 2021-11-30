from checkersplayer import CheckersPlayer
from utility_functions import GetPieces
import math
from board import CheckerBoard


# This class is a AI learning to play checkers using Alpha-Beta pruning
class AlphaBeta(CheckersPlayer):

    def __init__(self, id, depth, board=None):
        self.checkersBoard = board
        self.depth = depth
        self.id = id

    def get_next_move(self):
        # python doesn't support tail recursion, and I think this looks better.
        results = self.alpha_beta(self.checkersBoard, self.depth, -math.inf, math.inf, self.id)[1]
        return results

    # A class that implements the pruning algorithm to make move decisions based on the current state
    # Doesn't necessarily only use the class variables because its recursive.
    def alpha_beta(self, checkersBoard, treeDepth, A, B, maxing):
        if checkersBoard.check_game_finished():
            integerInfinite = 10000000
            # bad
            if GetPieces(checkersBoard.slots, checkersBoard.playersTurn) == [0, 0]:
                if maxing == False:
                    # Using integers instead of math.inf
                    # Other wise a bug is introduced and it will return None when not expected.
                    return integerInfinite, None
                else:
                    return -integerInfinite, None
            # good.
            elif GetPieces(checkersBoard.slots, not checkersBoard.playersTurn) == [0, 0]:
                # when maxing not player turn want to max when maxing and min when minning
                if maxing == False:
                    return -integerInfinite, None
                else:
                    return integerInfinite, None
            else:
                return 0, None

        # base case
        if treeDepth == 0:
            pieceInformation = GetPieces(checkersBoard.slots)
            # for maxing levels of the tree
            if pieceInformation['p2_reg'] != None and pieceInformation['p1_reg'] != None and \
                    pieceInformation['p1_king'] != None and pieceInformation['p2_king'] != None:
                if checkersBoard.playersTurn == maxing:
                    return pieceInformation['p1_reg'] + 2 * pieceInformation['p1_king'] - (
                            pieceInformation['p2_reg'] + 2 * pieceInformation['p2_king']), None
                return pieceInformation['p2_reg'] + 2 * pieceInformation['p2_king'] - (
                        pieceInformation['p1_reg'] + 2 * pieceInformation['p1_king']), None
            else:
                print("ERROR")
                exit(1)
        # recursive steps
        # getting the overall moves that are possible to decide what should happen next
        availableMoves = checkersBoard.get_moves_available()
        currentCheckersBoard = None
        allAvailableSlots = checkersBoard.get_new_game_states(availableMoves)
        bisMoveIndex = None

        # in the case of the max level.
        if not maxing:
            value = math.inf
            for slot in range(len(allAvailableSlots)):
                # recursively goes into a max level with False as the last parameter
                currentCheckersBoard = CheckerBoard(allAvailableSlots[slot], not checkersBoard.playersTurn)
                results = self.alpha_beta(currentCheckersBoard, treeDepth - 1, A, B, True)

                # beta portion of algorithm
                if B <= A:
                    if value > results[0]:
                        bisMoveIndex = slot
                        value = results[0]
                    break
                # getting beta value
                if value > results[0]:
                    B = min(B, value)
                    bisMoveIndex = slot
                    value = results[0]

            # did not find the best move
            if bisMoveIndex is None:
                return value, None
            return value, availableMoves[bisMoveIndex]
        else:
            value = -math.inf
            for slot in range(len(allAvailableSlots)):
                currentCheckersBoard = CheckerBoard(allAvailableSlots[slot], not checkersBoard.playersTurn)
                # recursively goes into a min level with False as the last parameter
                results = self.alpha_beta(currentCheckersBoard, treeDepth - 1, A, B, False)

                # B is beta
                # beginning of beta operation
                if B <= A:
                    if value < results[0]:
                        value = results[0]
                        bisMoveIndex = slot
                    break
                # getting alpha value
                if value < results[0]:
                    A = max(A, value)
                    value = results[0]
                    bisMoveIndex = slot
            # did not find the best move, may not be one possible
            if bisMoveIndex is None:
                return value, None
            return value, availableMoves[bisMoveIndex]