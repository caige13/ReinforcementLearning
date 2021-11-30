import math
from functools import reduce
import copy

class CheckerBoard:

    # Creates a new Board class instance, in the starting configuration
    def __init__(self, oldSpots=None, playersTurn=True):
        self.player1 = 1
        self.player1King = 3
        self.player2 = 2
        self.player2King = 4
        self.reversePlayer = self.player2
        self.blankSquare = 0
        # Width of the board, there will only be 4 possible columns for a given row.
        self.W = 4
        # 8 rows
        self.H = 8
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
        self.slots = [[val, val, val, val] for val in
                      [self.blankSquare] * self.H]

    # Restarts the checkers game to the beginning state of a checkers game.
    def game_reset(self):
        self.slots = CheckerBoard().slots

    # Gets all the moves that can be made that don't require capturing an enemy piece
    def basicMoves(self, begLocation):
        if self.slots[begLocation[0]][begLocation[1]] > 2:
            # getting basic moves
            nextLoc = self.n_possible_moves(begLocation, 1)
            nextLoc.extend(self.n_possible_moves(begLocation, 1, True))
        elif self.slots[begLocation[0]][begLocation[1]] == self.reversePlayer:
            nextLoc = self.n_possible_moves(begLocation, 1, True)
        else:
            nextLoc = self.n_possible_moves(begLocation, 1)

        possNextLoc = []

        for location in nextLoc:
            # checking if not empty
            if len(location) != 0:
                if self.slots[location[0]][location[1]] == self.blankSquare:
                    possNextLoc.append(location)

        return [[begLocation, end] for end in possNextLoc]

    # Gets possible moves diagonally forward or back 'n' number of times with no directional change midway
    def n_possible_moves(self, begLocation, valueN, reverse=False):
        if valueN % 2 == 0:
            # temporary values
            t2 = 0
            t1 = 0
        elif begLocation[0] % 2 == 0:
            # temporary values
            t2 = 1
            t1 = 0
        else:
            # temporary values
            t2 = 0
            t1 = 1

        solution = [[begLocation[0], begLocation[1] + math.floor(valueN / 2) + t1],
                    [begLocation[0], begLocation[1] - math.floor(valueN / 2) - t2]]
        # condition for reverse
        if reverse:
            solution[1][0] -= valueN
            solution[0][0] -= valueN
        else:
            solution[1][0] += valueN
            solution[0][0] += valueN

        if self.is_invalid_square(solution[1]):
            solution[1] = []
        if self.is_invalid_square(solution[0]):
            solution[0] = []

        return solution

    # Use recursion to grab all of the potential moves that involve taking an enemy piece
    def jumpMoves(self, begLocation, startingMoves=None):
        if startingMoves is None:
            startingMoves = [begLocation]

        solution = []
        if self.slots[begLocation[0]][begLocation[1]] > 2:
            n2 = self.n_possible_moves(begLocation, 2)
            n2.extend(self.n_possible_moves(begLocation, 2, True))
            n1 = self.n_possible_moves(begLocation, 1)
            n1.extend(self.n_possible_moves(begLocation, 1, True))
        elif self.slots[begLocation[0]][begLocation[1]] == self.reversePlayer:
            n2 = self.n_possible_moves(begLocation, 2, True)
            n1 = self.n_possible_moves(begLocation, 1, True)
        else:
            n2 = self.n_possible_moves(begLocation, 2)
            n1 = self.n_possible_moves(begLocation, 1)

        for next in range(len(n1)):
            if (not self.is_invalid_square(n2[next])) and (not self.is_invalid_square(n1[next])):
                if self.get_info(n1[next]) != self.blankSquare and self.get_info(
                        n1[next]) % 2 != self.get_info(begLocation) % 2:
                    # checking if blank space on board
                    if self.get_info(n2[next]) == self.blankSquare:
                        answerLen = len(solution)
                        tm1 = copy.deepcopy(startingMoves)
                        tm1.append(n2[next])
                        if self.get_info(begLocation) != self.player1 or n2[next][0] != self.H - 1:
                            if self.get_info(begLocation) != self.player2 or n2[next][0] != 0:
                                tm_2 = [begLocation, n2[next]]
                                tBoard = CheckerBoard(copy.deepcopy(self.slots), self.playersTurn)
                                tBoard.execute_move(tm_2, False)
                                solution.extend(tBoard.jumpMoves(tm_2[1], tm1))
                        if len(solution) == answerLen:
                            solution.append(tm1)
        return solution

    # Get all the moves that can be made from the current state of the board
    def get_moves_available(self):
        positionOfPieces = []
        for row in range(self.H):
            for col in range(self.W):
                if (self.playersTurn == True and (self.slots[row][col] == self.player1 or
                                                    self.slots[row][col] == self.player1King)) or \
                        (self.playersTurn == False and (self.slots[row][col] == self.player2 or
                                                        self.slots[row][col] == self.player2King)):
                    positionOfPieces.append([row, col])

        try:  # potentially unnecessary
            jumpMoves = list(reduce(lambda a, b: a + b, list(
                map(self.jumpMoves, positionOfPieces))))

            #know if jump moves is more important.
            if len(jumpMoves) > 0:
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
            self.execute_move(move, swapPlayer=False)
            solution.append(self.slots)
            self.slots = originalSpots
        return solution

    # executes the inputted move and changes the state of the board to reflect it - switches to other player's turn
    def execute_move(self, move, swapPlayer=True):
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
        # Checking if king
        if move[len(move) - 1][0] == self.H - 1 and self.slots[move[len(move) - 1][0]][
            move[len(move) - 1][1]] == self.player1:
            self.slots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.player1King
        # checking if king
        elif move[len(move) - 1][0] == 0 and self.slots[move[len(move) - 1][0]][
            move[len(move) - 1][1]] == self.player2:
            self.slots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.player2King
        # not a king
        else:
            self.slots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.slots[move[0][0]][move[0][1]]
        self.slots[move[0][0]][move[0][1]] = self.blankSquare

        if swapPlayer:
            self.playersTurn = not self.playersTurn


    # get's the symbol for the location inputted
    def get_symbol(self, loc):
        if self.slots[loc[0]][loc[1]] == self.player1King:
            return "O"
        elif self.slots[loc[0]][loc[1]] == self.player2King:
            return "X"
        elif self.slots[loc[0]][loc[1]] == self.player2:
            return "x"
        elif self.slots[loc[0]][loc[1]] == self.blankSquare:
            return " "
        elif self.slots[loc[0]][loc[1]] == self.player1:
            return "o"
