#Skeleton Program code for the AQA A Level Paper 1 Summer 2023 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team (and awesome notes written by rabil)
#developed in the Python 3.9 programming environment

# NOTE:
# ATTRIBUTES/METHODS GIVEN A SINGLE UNDERSCORE (E.G. self._Board) ARE PROTECTED
# ATTRIBUTES/METHODS GIVEN A DOUBLE UNDERSCORE (E.G. self.__CreateMoveOptions()) ARE PRIVATE
# ANYTHING ELSE IS A PUBLIC METHOD/ATTRIBUTE

import random

class Dastan:
    # Encapsulation (information hiding)
    def __init__(self, R, C, NoOfPieces):
        self._Board = []
        self._Players = []
        self._MoveOptionOffer = [] # MoveOption Offer queue for BOTH Players (both players use the same queue)
        # Names are defaulted to Player One and Player Two... Keep this in mind for a potential Section D question
        self._Players.append(Player("Player One", 1)) # Player instances

        self._Players.append(Player("Player Two", -1))
        self.__CreateMoveOptions()
        self._NoOfRows = R # Number of Rows
        self._NoOfColumns = C # Number of Columns
        self._MoveOptionOfferPosition = 0
        self.__CreateMoveOptionOffer()
        self.__CreateBoard()
        self.__CreatePieces(NoOfPieces) # Add standard pieces and Mirza pieces
        self._CurrentPlayer = self._Players[0] # Start game with Player One first

    def __DisplayBoard(self):
        # Iterate through to the number of columns printing column number and a space
        print("\n" + "   ", end="")
        for Column in range(1, self._NoOfColumns + 1):
            print(str(Column) + "  ", end="")
        print("\n" + "  ", end="")
        # Iterate through to the number of columns printing a short sequence of hyphens
        for Count in range(1, self._NoOfColumns + 1):
            print("---", end="")
        print("-")
        for Row in range(1, self._NoOfRows + 1):
            print(str(Row) + " ", end="")
            # Nested iteration to print associated symbol for each square followed by '|'
            for Column in range(1, self._NoOfColumns + 1):
                Index = self.__GetIndexOfSquare(Row * 10 + Column)
                print("|" + self._Board[Index].GetSymbol(), end="")
                PieceInSquare = self._Board[Index].GetPieceInSquare()
                # Piece symbol printed if Piece exists in square, otherwise blank space printed
                if PieceInSquare is None:
                    print(" ", end="")
                else:
                    print(PieceInSquare.GetSymbol(), end="")
            # Print a final '|' symbol at the end of each row
            print("|")
        print("  -", end="")
        # Iterate through number of columns printing short sequence of hyphens followed by two blank lines
        for Column in range(1, self._NoOfColumns + 1):
            print("---", end="")
        print()
        print()

    def __DisplayState(self):
        # Display information abbout the CurrentPlayer
        # Print the board on the screen
        self.__DisplayBoard()
        # Choosing a move option offer if wanted
        print("Move option offer: " + self._MoveOptionOffer[self._MoveOptionOfferPosition])
        print()
        # GetPlayerStateAsString method to display the score and move option queue
        print(self._CurrentPlayer.GetPlayerStateAsString())
        print("Turn: " + self._CurrentPlayer.GetName())
        print()

    def __GetIndexOfSquare(self, SquareReference):
        # Convert a SquareReference to a list position in the Board for the associated Square
        # Split SquareReference into Row number and Column number
        # Something to note is that board sizes greater than 10 will have issues as we would get incorrect Squares
        Row = SquareReference // 10
        Col = SquareReference % 10
        # 1 is subtracted from both variables to include index 0 (zero bound)
        return (Row - 1) * self._NoOfColumns + (Col - 1)

    def __CheckSquareInBounds(self, SquareReference):
        # Error handler to check if SquareReference is within the bounds of the board
        # DIV used to split off the row, and MOD to split off the column
        Row = SquareReference // 10
        Col = SquareReference % 10
        # Confirm that Row and Col are outside the range of 1 to the number of rows and columns
        if Row < 1 or Row > self._NoOfRows:
            return False
        elif Col < 1 or Col > self._NoOfColumns:
            return False
        else:
            return True

    def __CheckSquareIsValid(self, SquareReference, StartSquare):
        # Test to see if SquareReference is a valid Square choice
        # StartSquare is a boolean, if a StartSquareReference is passed as SquareReference,
        # StartSquare is set to True.
        # Otherwise, if SquareReference is a FinishSquareReference, StartSquare is set to False.
        if not self.__CheckSquareInBounds(SquareReference):
            # If SquareReference is not within the bounds of the board, return False
            return False
        # Get a piece at the Board location from SquareReference.
        # If there is no piece at that location, a blank square was selected.
        # If a StartSquareReference was chosen, return False (we chose a blank square)
        # Otherwise, we can move to the given square (given it is legal)
        PieceInSquare = self._Board[self.__GetIndexOfSquare(SquareReference)].GetPieceInSquare()
        if PieceInSquare is None:
            if StartSquare:
                return False
            else:
                return True
        # If a piece is in that Square, check to see if the piece belongs to the Player
        # If so, check again to see if a StartSquareReference was chosen to verify we move
        # our own piece. Otherwise we'd be capturing our own piece which isn't legal

        # If instead, it is a piece belonging to the opponent, check if we had chosen a
        # FinishSquareReference, meaning we can capture that piece.
        # Othwerwise we'd be trying to move the opponents piece, which isn't legal either
        elif self._CurrentPlayer.SameAs(PieceInSquare.GetBelongsTo()):
            if StartSquare:
                return True
            else:
                return False
        else:
            if StartSquare:
                return False
            else:
                return True

    def __CheckIfGameOver(self):
        # Iterate through the Board list checking each Square for a Piece
        Player1HasMirza = False
        Player2HasMirza = False
        for S in self._Board:
            PieceInSquare = S.GetPieceInSquare()
            # If the Square contains a Piece, the method returns True if a Kotla is contained in the Square
            # and the piece in the Square is a Mirza belonging to the opponent owning that Square
            # This means the player who owns the Mirza has just captured their opponent's Kotla (Game Over)
            if PieceInSquare is not None:
                if S.ContainsKotla() and PieceInSquare.GetTypeOfPiece() == "mirza" and not PieceInSquare.GetBelongsTo().SameAs(S.GetBelongsTo()):
                    return True
                # Otherwise, confirm that the Piece contains a Player 1 or Player 2 Mirza
                elif PieceInSquare.GetTypeOfPiece() == "mirza" and PieceInSquare.GetBelongsTo().SameAs(self._Players[0]):
                    Player1HasMirza = True
                elif PieceInSquare.GetTypeOfPiece() == "mirza" and PieceInSquare.GetBelongsTo().SameAs(self._Players[1]):
                    Player2HasMirza = True
        # Negated logical AND of both attributes returned.
        # If both players have lost their Mirza, True is returned (Game Over)
        return not (Player1HasMirza and Player2HasMirza)

    def __GetSquareReference(self, Description):
        # Get a SquareReference on the board from the user
        # Description is concatenated giving an appropriate output - can be different (Polymorphism)
        # ! NOTE: Input from the user is casted WITHOUT ANY ERROR HANDLING !, and stored in a local
        # variable SelectedSquare which is then returned
        SelectedSquare = int(input("Enter the square " + Description + " (row number followed by column number): "))
        return SelectedSquare # Returns an integer

    def __UseMoveOptionOffer(self):
        # Place the move from the MoveOptionOffer list into the current player move option queue
        # Position is asked for for the MoveOption to be replaced with !(Without any error handling, again...)!
        ReplaceChoice = int(input("Choose the move option from your queue to replace (1 to 5): "))
        # UpdateMoveOptionQueueWithOffer is called on the CurrentPlayer to replace the selected move with the current offer
        self._CurrentPlayer.UpdateMoveOptionQueueWithOffer(ReplaceChoice - 1, self.__CreateMoveOption(self._MoveOptionOffer[self._MoveOptionOfferPosition], self._CurrentPlayer.GetDirection()))
        # Score is then reduced using ChangeScore() based on the position of the move option selected by the Player
        self._CurrentPlayer.ChangeScore(-(10 - (ReplaceChoice * 2)))
        # MoveOptionOfferPosition is updated, with a random number between 0 to 4 to get a new move
        # Currently the Player can use as many new move options as they want per turn... Keep this in mind for a potential Section D question
        self._MoveOptionOfferPosition = random.randint(0, 4)

    def __GetPointsForOccupancyByPlayer(self, CurrentPlayer):
        # Calculate total points for any squres occupied by the CurrentPlayer
        ScoreAdjustment = 0 # Score is incremented through the Board occupied by the current player
        for S in self._Board:
            # GetPointsForOccupancy method called on each Square in the board, default score of 0
            # The method is overridden by the Kotla class, to return 5 if the Kotla belongs to current player
            # AND is occupied by the current player Mirza or a current player piece.
            # It will return 1 if the Kotla occupied by a current player piece or Mirza belong to the opponent player

            # Polymorphism is used here
            ScoreAdjustment += (S.GetPointsForOccupancy(CurrentPlayer))
        return ScoreAdjustment # Total score is returned at the end

    def __UpdatePlayerScore(self, PointsForPieceCapture):
        # Calculates the change in player score for the move which the player has just made
        self._CurrentPlayer.ChangeScore(self.__GetPointsForOccupancyByPlayer(self._CurrentPlayer) + PointsForPieceCapture)

    def __CalculatePieceCapturePoints(self, FinishSquareReference):
        # Use the GetPieceInSquare method to get the piece at the Board location from the FinishSquareReference
        # If there is a piece at that location, the PointsIfCaptured attribute for that piece is returned.
        # If there is no piece at that location the method returns 0 
        if self._Board[self.__GetIndexOfSquare(FinishSquareReference)].GetPieceInSquare() is not None:
            return self._Board[self.__GetIndexOfSquare(FinishSquareReference)].GetPieceInSquare().GetPointsIfCaptured()
        return 0

    def PlayGame(self):
        # Main game loop playing loop, public method using the local variable GameOver
        GameOver = False
        while not GameOver:
            # Firstly displays current game state, board and current player queue
            self.__DisplayState()
            SquareIsValid = False
            Choice = 0
            while Choice < 1 or Choice > 3:
                # Choosing move option 1-3 or 9 for move offer
                Choice = int(input("Choose move option to use from queue (1 to 3) or 9 to take the offer: "))
                if Choice == 9:
                    self.__UseMoveOptionOffer()
                    self.__DisplayState()
            while not SquareIsValid:
                # Loop unit valid square is chosen, choosing a piece to move
                StartSquareReference = self.__GetSquareReference("containing the piece to move")
                SquareIsValid = self.__CheckSquareIsValid(StartSquareReference, True)
            SquareIsValid = False
            while not SquareIsValid:
                # Loop until square chosen in bounds, piece to move to
                FinishSquareReference = self.__GetSquareReference("to move to")
                SquareIsValid = self.__CheckSquareIsValid(FinishSquareReference, False)
            # NOTE: This does not deal with the case whether the move is not legal.
            # If this is the case, the Player's turn is skipped... Keep this in mind for a potential Section C/D question
            MoveLegal = self._CurrentPlayer.CheckPlayerMove(Choice, StartSquareReference, FinishSquareReference)
            if MoveLegal:
                # If the move is legal, calculate any points for capturing pieces
                # Update player score based on position of move option used from player queue ising ChangeScore
                PointsForPieceCapture = self.__CalculatePieceCapturePoints(FinishSquareReference)
                self._CurrentPlayer.ChangeScore(-(Choice + (2 * (Choice - 1))))
                # Update Player Queue to move the selected MoveOption choice to the back of the queue
                # Call UpdateBoard to update the positions made, and UpdatePlayerScore for current player score
                self._CurrentPlayer.UpdateQueueAfterMove(Choice)
                self.__UpdateBoard(StartSquareReference, FinishSquareReference)
                self.__UpdatePlayerScore(PointsForPieceCapture)
                # Print the updated score onto the screen, and now it is opponent's turn
                print("New score: " + str(self._CurrentPlayer.GetScore()) + "\n")
            if self._CurrentPlayer.SameAs(self._Players[0]):
                self._CurrentPlayer = self._Players[1]
            else:
                self._CurrentPlayer = self._Players[0]
            # Check if current player has their Mirza in the opponent Kotla, or the opponent Mirza has been captured
            # If so, the game is over, and break out of the main game loop
            GameOver = self.__CheckIfGameOver()
        # Print the final playing position of the board, and confirm which player has won using DisplayFinalResult
        self.__DisplayState()
        self.__DisplayFinalResult()

    def __UpdateBoard(self, StartSquareReference, FinishSquareReference):
        # Performs the actual move of a piece from one location on the board to another
        # RemovePiece() is used on the Board in the StartSquareReference. This piece is subsequently passed as a parameter
        # to the SetPiece() method to be placed at the Board list index calculated from the FinishSquareReference parameter
        self._Board[self.__GetIndexOfSquare(FinishSquareReference)].SetPiece(self._Board[self.__GetIndexOfSquare(StartSquareReference)].RemovePiece())

    def __DisplayFinalResult(self):
        # Winner of the game determined by player with the highest score
        # Comparision of both scores, using the GetScore method.
        # GetName is used from the Player object to print out the player name
        if self._Players[0].GetScore() == self._Players[1].GetScore():
            print("Draw!")
        elif self._Players[0].GetScore() > self._Players[1].GetScore():
            print(self._Players[0].GetName() + " is the winner!")
        else:
            print(self._Players[1].GetName() + " is the winner!")

    def __CreateBoard(self):
        # Nested iteration of NoOfRows and NoOfColumns to populate the Board list
        for Row in range(1, self._NoOfRows + 1):
            for Column in range(1, self._NoOfColumns + 1):
                if Row == 1 and Column == self._NoOfColumns // 2:
                    # Player 1's Kotla placed to the left of the centre of row 1
                    S = Kotla(self._Players[0], "K")
                elif Row == self._NoOfRows and Column == self._NoOfColumns // 2 + 1:
                    # Player 2's Kotla placed in the centre of the last row
                    # Or right of the centre of the last row, if an even number of columns
                    S = Kotla(self._Players[1], "k")
                else:
                    # Remaining locations filled with Square objects
                    S = Square()
                self._Board.append(S)

    def __CreatePieces(self, NoOfPieces):
        # Places the default playing pieces and Mirza for each player on the Board
        for Count in range(1, NoOfPieces + 1):
            # Place 'NoOfPieces' standard pieces on the board. Player 1's go onto row 2
            # and Player 2's on the penultimate row
            # Player 1 has standard pieces labelled as '!'
            CurrentPiece = Piece("piece", self._Players[0], 1, "!")
            self._Board[self.__GetIndexOfSquare(2 * 10 + Count + 1)].SetPiece(CurrentPiece)
        # Pieces are given the parameters of a name, who they belong to, points scored if captured, and their symbol.
        # Player 1's Mirza given the symbol '1'
        CurrentPiece = Piece("mirza", self._Players[0], 5, "1")
        self._Board[self.__GetIndexOfSquare(10 + self._NoOfColumns // 2)].SetPiece(CurrentPiece)
        for Count in range(1, NoOfPieces + 1):
            # Player 2 has standard pieces labelled as '"'
            CurrentPiece = Piece("piece", self._Players[1], 1, '"')
            self._Board[self.__GetIndexOfSquare((self._NoOfRows - 1) * 10 + Count + 1)].SetPiece(CurrentPiece)
        # Player 2's Mirza given the symbol '2'
        CurrentPiece = Piece("mirza", self._Players[1], 5, "2")
        # The Mirza's are to be placed in the position of the players Kotla (initally)
        self._Board[self.__GetIndexOfSquare(self._NoOfRows * 10 + (self._NoOfColumns // 2 + 1))].SetPiece(CurrentPiece)

    def __CreateMoveOptionOffer(self):
        # Adds the five default MoveOptions to the MoveOptionOffer queue
        self._MoveOptionOffer.append("jazair")
        self._MoveOptionOffer.append("chowkidar")
        self._MoveOptionOffer.append("cuirassier")
        self._MoveOptionOffer.append("ryott")
        self._MoveOptionOffer.append("faujdar")

    # Creating the different moves available... Keep this in mind for a potential Section D question

    # MoveOption and Move instantiations made

    # The first parameter for Move is the number of rows to move from starting location to end location
    # Second parameter is number of columns to move from starting location to end location
    # Third parameter is the direction
    # Direction of 1 moves down the board - for Player 1. Direction of -1 moves up the board - for Player 2

    def __CreateRyottMoveOption(self, Direction):
        NewMoveOption = MoveOption("ryott")
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateFaujdarMoveOption(self, Direction):
        NewMoveOption = MoveOption("faujdar")
        NewMove = Move(0, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateJazairMoveOption(self, Direction):
        NewMoveOption = MoveOption("jazair")
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateCuirassierMoveOption(self, Direction):
        NewMoveOption = MoveOption("cuirassier")
        NewMove = Move(1 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(2 * Direction, 0)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateChowkidarMoveOption(self, Direction):
        NewMoveOption = MoveOption("chowkidar")
        NewMove = Move(1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, 1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(-1 * Direction, -1 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, 2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        NewMove = Move(0, -2 * Direction)
        NewMoveOption.AddToPossibleMoves(NewMove)
        return NewMoveOption

    def __CreateMoveOption(self, Name, Direction):
        # Use selection of on the Name parameter for the specific MoveOption
        # NOTE: There are many literals, and repeated strings e.g. "chowkidar" and "mirza" throughout the program.
        # Keep this in mind for a potential Section C question. (If one string is mispelt, this can cause errors, so may be better to use constants to store the names)
        if Name == "chowkidar":
            return self.__CreateChowkidarMoveOption(Direction)
        elif Name == "ryott":
            return self.__CreateRyottMoveOption(Direction)
        elif Name == "faujdar":
            return self.__CreateFaujdarMoveOption(Direction)
        elif Name == "jazair":
            return self.__CreateJazairMoveOption(Direction)
        else:
            return self.__CreateCuirassierMoveOption(Direction)

    def __CreateMoveOptions(self):
        # Adds the five default MoveOptions to the MoveOptionQueue for each player
        # CreateMoveOption is called, passing in the Name of the MoveOption and the Direction
        # Players[0] --> Player 1 (Direction = 1)
        # Players[1] --> Player 2 (Direction = -1)
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", 1))
        self._Players[0].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", 1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("ryott", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("chowkidar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("jazair", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("faujdar", -1))
        self._Players[1].AddToMoveOptionQueue(self.__CreateMoveOption("cuirassier", -1))

class Piece:
    # Aggregation relationship with Square
    # Encapsulation (information hiding) Abstraction
    # Abstraction
    def __init__(self, T, B, P, S):
        self._TypeOfPiece = T # String
        self._BelongsTo = B # Player
        self._PointsIfCaptured = P # Integer
        self._Symbol = S # String

    def GetSymbol(self):
        # Retuns the piece symbol as a String
        return self._Symbol

    def GetTypeOfPiece(self):
        # Either a piece or a mirza
        return self._TypeOfPiece

    def GetBelongsTo(self):
        # Returns a Player
        return self._BelongsTo

    def GetPointsIfCaptured(self):
        # Integer returned
        return self._PointsIfCaptured

class Square:
    # Composition relationship with Dastan
    # Encapsulation and Abstraction


    def __init__(self):
        self._PieceInSquare = None
        self._BelongsTo = None
        self._Symbol = " "

    def SetPiece(self, P):
        # Placing a Piece on the Board
        self._PieceInSquare = P

    def RemovePiece(self):
        # Remove Piece from a square
        # Temporary copy of the Piece made in the local variable PieceToReturn
        # Then set the attribute PieceInSquare to null to delete it
        # Returns the Piece
        PieceToReturn = self._PieceInSquare
        self._PieceInSquare = None
        return PieceToReturn

    def GetPieceInSquare(self):
        # Returns a Piece
        return self._PieceInSquare

    def GetSymbol(self):
        # Returning a string, kotla, piece or empty
        return self._Symbol

    def GetPointsForOccupancy(self, CurrentPlayer):
        # Virtual method -> Polymorphism
        # Base class method for the GetPointsForOccupancy()
        # method in the Kotla class.
        # If the method was not overridden, it would return 0
        return 0

    def GetBelongsTo(self):
        # Returns a Player
        return self._BelongsTo

    def ContainsKotla(self):
        # If symbol is a kotla, piece is a kota in the square
        if self._Symbol == "K" or self._Symbol == "k":
            return True
        else:
            return False

class Kotla(Square):
    # Inheritance relationship with Square
    def __init__(self, P, S):
        super(Kotla, self).__init__()
        self._BelongsTo = P
        self._Symbol = S

    def GetPointsForOccupancy(self, CurrentPlayer):
        # Overridden method from base class (Use of Polymorphism)
        if self._PieceInSquare is None:
            # If there is no piece in the Kotla Square, return 0
            return 0
        elif self._BelongsTo.SameAs(CurrentPlayer):
            # If Piece in Kotla square belongs to current player, and the piece in the Kotla square is either a Mirza or standard piece also owned by CurrentPlayer, return 5
            # Otherwise return 0
            if CurrentPlayer.SameAs(self._PieceInSquare.GetBelongsTo()) and (self._PieceInSquare.GetTypeOfPiece() == "piece" or self._PieceInSquare.GetTypeOfPiece() == "mirza"):
                return 5
            else:
                return 0
        else:
            # If Kotla square belongs to opponent, and piece in it is either a Mirza or standard piece owned by CurrentPlayer
            # return a score of one point, otherwise return 0 points
            if CurrentPlayer.SameAs(self._PieceInSquare.GetBelongsTo()) and (self._PieceInSquare.GetTypeOfPiece() == "piece" or self._PieceInSquare.GetTypeOfPiece() == "mirza"):
                return 1
            else:
                return 0


                
class MoveOption:
    # Aggregation relationship with MoveOptionQueue
    # Encapsulation
    def __init__(self, N):
        self._Name = N # Name of moves (ryott, jazair, etc.)
        self._PossibleMoves = []

    def AddToPossibleMoves(self, M):
        # Adding to the list all possible moves
        self._PossibleMoves.append(M)

    def GetName(self):
        return self._Name

    def CheckIfThereIsAMoveToSquare(self, StartSquareReference, FinishSquareReference):
        StartRow = StartSquareReference // 10 # DIV to split off the StartRow
        StartColumn = StartSquareReference % 10 # MOD to split off the StartColumn
        FinishRow = FinishSquareReference // 10
        FinishColumn = FinishSquareReference % 10
        for M in self._PossibleMoves:
            # Iterate through each Move in PossibleMoves
            # Check if StartRow, StartColumn, FinishRow, FinishColumn
            # combination represent a valid move for one of the possible positions
            # a piece could move to
            if StartRow + M.GetRowChange() == FinishRow and StartColumn + M.GetColumnChange() == FinishColumn:
                return True
        return False

class Move:
    # Composition relationship with MoveOption
    def __init__(self, R, C):
        # Defined as the number of 'rows' that can be moved either up or down
        # And the number of 'columns' that can be moved either left or right
        # From a given starting square. Used for the different moves (ryott, jazair, etc.)
        # in what (legal) squares they can move to

        # Use of Encapsulation
      
        self._RowChange = R # Integer (Row)
        self._ColumnChange = C # Integer (Column)

    def GetRowChange(self):
        return self._RowChange

    def GetColumnChange(self):
        return self._ColumnChange

class MoveOptionQueue:
    # Composition relationship with Player
    # Encapsulation (information hiding)
    def __init__(self):
        self.__Queue = []

    def GetQueueAsString(self):
        QueueAsString = ""
        # Returns the move queue for the given player
        # Iterates through Queue, concatenating the Count variable
        # together with the name of each Move in the Queue using GetName()
        Count = 1
        for M in self.__Queue:
            QueueAsString += str(Count) + ". " + M.GetName() + "   "
            Count += 1
        return QueueAsString # Returns a string

    def Add(self, NewMoveOption):
        # Adds a new MoveOption to the Queue
        self.__Queue.append(NewMoveOption)

    def Replace(self, Position, NewMoveOption):
        # Replaces a MoveOption in the Queue indexed at a given position
        self.__Queue[Position] = NewMoveOption

    def MoveItemToBack(self, Position):
        # Temporary copy of MoveOption at the index Position in Queue
        # Uses the static pop method to remove the MoveOption at the given index
        # Appends the temporary copy of the MoveOption back into the Queue
        # which has the effect of placing it at the end of the queue
        Temp = self.__Queue[Position]
        self.__Queue.pop(Position)
        self.__Queue.append(Temp)

    def GetMoveOptionInPosition(self, Pos):
        # Returns a MoveOption
        return self.__Queue[Pos]

class Player:
    # Composition relationship with Dastan
    # Aggregation relationship with Piece
    # Aggregation (belongs to) relationship with Square

    # Encapsulation
    def __init__(self, N, D):
        self.__Score = 100
        self.__Name = N # Player name (Defaulted to Player One and Player Two)
        self.__Direction = D # 1 or -1 (downwards taken as positive y-direction)
        self.__Queue = MoveOptionQueue()

    def SameAs(self, APlayer):
        # APlayer is a Player object
        # Check to see if APlayer is the same player as the current player
        # From comparing their names !(Ensure both players have different names)!
        if APlayer is None:
            return False
        elif APlayer.GetName() == self.__Name:
            return True
        else:
            return False

    def GetPlayerStateAsString(self):
        # Expose the GetQueueAsString() method in the MoveOptionQueue class to the Dastan class through the player
        # The method returns a concatenation of the player score attribute and the player
        # represented as a single string using the GetQueueAsString() method
        return self.__Name + "\n" + "Score: " + str(self.__Score) + "\n" + "Move option queue: " + self.__Queue.GetQueueAsString() + "\n"

    def AddToMoveOptionQueue(self, NewMoveOption):
        # For the individual Player, add their MoveOptions to their Queue
        self.__Queue.Add(NewMoveOption)

    def UpdateQueueAfterMove(self, Position):
        # Expose the MoveItemToBack() method in the MoveOptionQueue class to the
        # Dastan class through the player
        # Calls the MoveItemToBack() method on player queue passig the Position
        # minus 1 (index starting at zero). This MoveOption will be moved to the
        # back of the queue
        self.__Queue.MoveItemToBack(Position - 1)

    def UpdateMoveOptionQueueWithOffer(self, Position, NewMoveOption):
        # Expose the Replace() method in the MoveOptionQueue class to the
        # Dastan class through the player.
        # Replace the MoveOption at index Position with NewMoveOption
        self.__Queue.Replace(Position, NewMoveOption)

    def GetScore(self):
        # Public method to return the private attribute for the Player's score
        return self.__Score

    def GetName(self):
        # Public method to return the private attribute for the Player's name
        return self.__Name

    def GetDirection(self):
        # Public method to return the private attribute for the Player's direction
        return self.__Direction

    def ChangeScore(self, Amount):
        # Increment player's score by a specified amount
        self.__Score += Amount

    def CheckPlayerMove(self, Pos, StartSquareReference, FinishSquareReference):
        # Check if a move selected by a Player is valid using CheckIfThereIsAMoveToSquare()
        # Temporary move object is made from the Player queue as selected
        # StartSquareReference is where the piece is at currently
        # FinishSquareReference is where the piece is to be moved to
        Temp = self.__Queue.GetMoveOptionInPosition(Pos - 1)
        return Temp.CheckIfThereIsAMoveToSquare(StartSquareReference, FinishSquareReference)

def Main():
    ThisGame = Dastan(6, 6, 4) # Object instantiation to start the game. 6 Rows, 6 Columns, 4 Pieces (excluding mirza)
    ThisGame.PlayGame()
    print("Goodbye!")
    input()

if __name__ == "__main__":
    Main()