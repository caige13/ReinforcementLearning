
# Class represents a checkers player -> inherited by alphabeta and q learning classes
class CheckersPlayer:

    # get the AI's desired next move
    def get_next_move(self):
        pass

    # set the board object
    def set_checkersBoard(self, board):
        self.checkersBoard = board

    #can be overrwritten if AI that implements this needs to be notified the game ended before wiping
    def isGameFinished(self):
        pass