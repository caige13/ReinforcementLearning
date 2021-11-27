
import math
from functools import reduce
import copy

class CheckerBoard:
    player1 = 1
    player1O = 3
    player2 = 2
    player2O = 4
    reversePlayer = player2
    blankSquare = 0
    # Width of the board, there will only be 4 possible columns for a given row.
    W = 4
    # 8 rows
    H = 8

    # Creates a new Board class instance, in the starting configuration
    def __init__(self, oldSpots=None, playersTurn=True):
        if not (oldSpots is None):
            self.slots = oldSpots
        else:
            self.slots = [[j, j, j, j] for j in
                          [self.player1, self.player1, self.player1, self.blankSquare,
                           self.blankSquare, self.player2, self.player2, self.player2]]
        self.playersTurn = playersTurn

    # A visual representation of the board
    def show_checker_board(self):
        begEndRow = "|---|---|---|---|---|---|---|---|"
        print(begEndRow)
        for row in range(self.H):
            if row % 2 == 1:
                unplayableSlot = "|///|"
            else:
                unplayableSlot = "|"
            for i in range(self.W):
                unplayableSlot = unplayableSlot + " " + self.get_symbol([row, i]) + " |"
                if i != 3 or row % 2 != 1:
                    unplayableSlot = unplayableSlot + "///|"
            print(unplayableSlot)
            print(begEndRow)

    # Returns if the spot at the inputted coordinates is a spot on the board
    def is_invalid_square(self, location):
        if len(location) == 0 or location[0] < 0 or location[0] > self.H - 1 or \
                location[1] < 0 or location[1] > self.W - 1:
            return True
        return False

    # Returns true if the game is over, false if it's still being played
    def check_game_finished(self):
        if len(self.get_moves_available()) > 0:
            return False
        return True

    # Retreives the information on the inputted location spot
    def get_info(self, loc):
        return self.slots[loc[0]][loc[1]]

    # Completely clears the board, leaving only empty spaces
    def board_clear(self):
        self.slots = [[j, j, j, j] for j in
                      [self.blankSquare] * self.H]

    # Restarts the checkers game to the beginning state of a checkers game.
    def game_reset(self):
        self.slots = CheckerBoard().slots

    # Gets all the moves that can be made that don't require capturing an enemy piece
    def basicMoves(self, begLocation):
        if self.slots[begLocation[0]][begLocation[1]] > 2:
            nextLoc = self.n_possible_moves(begLocation, 1)
            nextLoc.extend(self.n_possible_moves(begLocation, 1, True))
        elif self.slots[begLocation[0]][begLocation[1]] == self.reversePlayer:
            nextLoc = self.n_possible_moves(begLocation, 1, True)
        else:
            nextLoc = self.n_possible_moves(begLocation, 1)

        possibleNexLoc = []

        for location in nextLoc:
            if len(location) != 0:
                if self.slots[location[0]][location[1]] == self.blankSquare:
                    possibleNexLoc.append(location)

        return [[begLocation, endSpot] for endSpot in possibleNexLoc]

    # Gets possible moves diagonally forward or back 'n' number of times with no directional change midway
    def n_possible_moves(self, begLocation, n, reverse=False):
        if n % 2 == 0:
            t1 = 0
            t2 = 0
        elif begLocation[0] % 2 == 0:
            t1 = 0
            t2 = 1
        else:
            t1 = 1
            t2 = 0

        solution = [[begLocation[0], begLocation[1] + math.floor(n / 2) + t1],
                    [begLocation[0], begLocation[1] - math.floor(n / 2) - t2]]
        if reverse:
            solution[0][0] = solution[0][0] - n
            solution[1][0] = solution[1][0] - n
        else:
            solution[0][0] = solution[0][0] + n
            solution[1][0] = solution[1][0] + n

        if self.is_invalid_square(solution[0]):
            solution[0] = []
        if self.is_invalid_square(solution[1]):
            solution[1] = []

        return solution

    # Use recursion to grab all of the potential moves that involve taking an enemy piece
    def jumpMoves(self, begLocation, startingMoves=None):
        if startingMoves is None:
            startingMoves = [begLocation]

        solution = []
        if self.slots[begLocation[0]][begLocation[1]] > 2:
            n1 = self.n_possible_moves(begLocation, 1)
            n2 = self.n_possible_moves(begLocation, 2)
            n1.extend(self.n_possible_moves(begLocation, 1, True))
            n2.extend(self.n_possible_moves(begLocation, 2, True))
        elif self.slots[begLocation[0]][begLocation[1]] == self.reversePlayer:
            n1 = self.n_possible_moves(begLocation, 1, True)
            n2 = self.n_possible_moves(begLocation, 2, True)
        else:
            n1 = self.n_possible_moves(begLocation, 1)
            n2 = self.n_possible_moves(begLocation, 2)

        for j in range(len(n1)):
            if (not self.is_invalid_square(n2[j])) and (not self.is_invalid_square(n1[j])):
                if self.get_info(n1[j]) != self.blankSquare and self.get_info(
                        n1[j]) % 2 != self.get_info(begLocation) % 2:
                    if self.get_info(n2[j]) == self.blankSquare:
                        tm1 = copy.deepcopy(startingMoves)
                        tm1.append(n2[j])
                        answerLen = len(solution)
                        if self.get_info(begLocation) != self.player1 or n2[j][0] != self.H - 1:
                            if self.get_info(begLocation) != self.player2 or n2[j][0] != 0:
                                tm_2 = [begLocation, n2[j]]
                                tBoard = CheckerBoard(copy.deepcopy(self.slots), self.playersTurn)
                                tBoard.executeMove(tm_2, False)
                                solution.extend(tBoard.jumpMoves(tm_2[1], tm1))
                        if len(solution) == answerLen:
                            solution.append(tm1)
        return solution

    # Get all the moves that can be made from the current state of the board
    def get_moves_available(self):
        positionOfPieces = []
        for j in range(self.H):
            for i in range(self.W):
                if (self.playersTurn == True and (self.slots[j][i] == self.player1 or
                                                    self.slots[j][i] == self.player1O)) or \
                        (self.playersTurn == False and (self.slots[j][i] == self.player2 or
                                                        self.slots[j][i] == self.player2O)):
                    positionOfPieces.append([j, i])

        try:  # potentially unnecessary
            jumpMoves = list(reduce(lambda a, b: a + b, list(
                map(self.jumpMoves, positionOfPieces))))

            if len(jumpMoves) != 0:
                return jumpMoves

            return list(reduce(lambda a, b: a + b,
                               list(map(self.basicMoves, positionOfPieces))))
        except TypeError:
            return []



    # Get's the new board states given the moves inputted
    def get_new_game_states(self, moves):
        if moves is None:
            return self.slots
        solution = []
        for move in moves:
            originalSpots = copy.deepcopy(self.slots)
            self.executeMove(move, swapPlayer=False)
            solution.append(self.slots)
            self.slots = originalSpots
        return solution

    # executes the inputted move and changes the state of the board to reflect it - switches to other player's turn
    def executeMove(self, move, swapPlayer=True):
        if abs(move[0][0] - move[1][0]) == 2:
            for j in range(len(move) - 1):
                if move[j][0] % 2 == 1:
                    if move[j + 1][1] < move[j][1]:
                        middleY = move[j][1]
                    else:
                        middleY = move[j + 1][1]
                else:
                    if move[j + 1][1] < move[j][1]:
                        middleY = move[j + 1][1]
                    else:
                        middleY = move[j][1]

                self.slots[int((move[j][0] + move[j + 1][0]) / 2)][middleY] = self.blankSquare

        self.slots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.slots[move[0][0]][move[0][1]]
        if move[len(move) - 1][0] == self.H - 1 and self.slots[move[len(move) - 1][0]][
            move[len(move) - 1][1]] == self.player1:
            self.slots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.player1O
        elif move[len(move) - 1][0] == 0 and self.slots[move[len(move) - 1][0]][
            move[len(move) - 1][1]] == self.player2:
            self.slots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.player2O
        else:
            self.slots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.slots[move[0][0]][move[0][1]]
        self.slots[move[0][0]][move[0][1]] = self.blankSquare

        if swapPlayer:
            self.playersTurn = not self.playersTurn


    # get's the symbol for the location inputted
    def get_symbol(self, loc):
        if self.slots[loc[0]][loc[1]] == self.blankSquare:
            return " "
        elif self.slots[loc[0]][loc[1]] == self.player1:
            return "o"
        elif self.slots[loc[0]][loc[1]] == self.player2:
            return "x"
        elif self.slots[loc[0]][loc[1]] == self.player1O:
            return "O"
        else:
            return "X"
