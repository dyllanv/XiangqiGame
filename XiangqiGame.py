# Author: Dyllan Vangemert
# Date: 03/09/2020
# Description: Fully functional Xiangqi Game.
# Contains classes for game and each piece type.

class XiangqiGame:
    """Represents a game of Xiangqi. Keeps track of the board, game state, piece
    locations, 'check' status. Contains method to move pieces. Game ends when a
    player's General is in 'checkmate'."""

    def __init__(self):
        """Initializes all of the pieces, the board with pieces in their staring
        positions, the game state, the accepted column and row values, the 'check'
        status of both teams, and lists of active pieces for each team."""
        self._bs1 = Soldier("black", "S", (6, 0))
        self._bs2 = Soldier("black", "S", (6, 2))
        self._bs3 = Soldier("black", "S", (6, 4))
        self._bs4 = Soldier("black", "S", (6, 6))
        self._bs5 = Soldier("black", "S", (6, 8))
        self._bc1 = Cannon("black", "C", (7, 1))
        self._bc2 = Cannon("black", "C", (7, 7))
        self._br1 = Rook("black", "R", (9, 0))
        self._br2 = Rook("black", "R", (9, 8))
        self._bh1 = Horse("black", "H", (9, 1))
        self._bh2 = Horse("black", "H", (9, 7))
        self._be1 = Elephant("black", "E", (9, 2))
        self._be2 = Elephant("black", "E", (9, 6))
        self._ba1 = Advisor("black", "A", (9, 3))
        self._ba2 = Advisor("black", "A", (9, 5))
        self._bg = General("black", "G", (9, 4))

        self._rs1 = Soldier("red", "S", (3, 0))
        self._rs2 = Soldier("red", "S", (3, 2))
        self._rs3 = Soldier("red", "S", (3, 4))
        self._rs4 = Soldier("red", "S", (3, 6))
        self._rs5 = Soldier("red", "S", (3, 8))
        self._rc1 = Cannon("red", "C", (2, 1))
        self._rc2 = Cannon("red", "C", (2, 7))
        self._rr1 = Rook("red", "R", (0, 0))
        self._rr2 = Rook("red", "R", (0, 8))
        self._rh1 = Horse("red", "H", (0, 1))
        self._rh2 = Horse("red", "H", (0, 7))
        self._re1 = Elephant("red", "E", (0, 2))
        self._re2 = Elephant("red", "E", (0, 6))
        self._ra1 = Advisor("red", "A", (0, 3))
        self._ra2 = Advisor("red", "A", (0, 5))
        self._rg = General("red", "G", (0, 4))

        self._board = [[self._rr1, self._rh1, self._re1, self._ra1, self._rg,
                        self._ra2, self._re2, self._rh2, self._rr2],
                       [None, None, None, None, None, None, None, None, None],
                       [None, self._rc1, None, None, None,
                        None, None, self._rc2, None],
                       [self._rs1, None, self._rs2, None, self._rs3,
                        None, self._rs4, None, self._rs5],
                       [None, None, None, None, None, None, None, None, None],
                       [None, None, None, None, None, None, None, None, None],
                       [self._bs1, None, self._bs2, None, self._bs3,
                        None, self._bs4, None, self._bs5],
                       [None, self._bc1, None, None, None,
                        None, None, self._bc2, None],
                       [None, None, None, None, None, None, None, None, None],
                       [self._br1, self._bh1, self._be1, self._ba1, self._bg,
                        self._ba2, self._be2, self._bh2, self._br2]]
        self._bpieces = [self._br1, self._bh1, self._be1, self._ba1,
                         self._bg, self._ba2, self._be2, self._bh2,
                         self._br2, self._bc1, self._bc2, self._bs1,
                         self._bs2, self._bs3, self._bs4, self._bs5]
        self._rpieces = [self._rr1, self._rh1, self._re1, self._ra1,
                         self._rg, self._ra2, self._re2, self._rh2,
                         self._rr2, self._rc1, self._rc2, self._rs1,
                         self._rs2, self._rs3, self._rs4, self._rs5]

        # All columns and rows on board. Index of letter/number match board index
        self._columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        self._rows = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self._game_state = "UNFINISHED"
        self._red_check = False
        self._black_check = False
        self._turn = "red"

    def get_board(self):
        """Returns the board"""
        return self._board

    def get_game_state(self):
        """Returns the current game state"""
        return self._game_state

    def get_bpieces(self):
        """Returns a list of active Black pieces"""
        return self._bpieces

    def get_rpieces(self):
        """Returns a list of active Red pieces"""
        return self._rpieces

    def get_turn(self):
        """Returns whose turn it is"""
        return self._turn

    def make_move(self, current, next):
        """Moves a piece from it's current space on the board to another space
        on the board, if a legal move."""
        # Check game state and make sure moves are within board boundaries
        if self._game_state != "UNFINISHED":
            return False
        elif current[0] not in self._columns or next[0] not in self._columns:
            return False
        elif current[1:] not in self._rows or next[1:] not in self._rows:
            return False

        # Convert input move coordinates into tuples of (row index, column index)
        # by using columns/rows lists to find board indexes
        current = (self._rows.index(current[1:]), self._columns.index(current[0]))
        next = (self._rows.index(next[1:]), self._columns.index(next[0]))

        # If attempted move is valid, change turn. If not, return False.
        if self.move_piece(current, next):
            if self._turn == "red":
                self._turn = "black"
            else:
                self._turn = "red"
        else:
            return False

        # Update check status of opposing player after valid move is made
        self.is_in_check(self._turn)

        # Check to see if opposing player can make any moves.
        # If not, checkmate or stalemate, depending on check status
        if self.any_valid_moves() is False:
            if self._red_check:
                self._game_state = "CHECKMATE: BLACK WON!"
            elif self._black_check:
                self._game_state = "CHECKMATE: RED WON!"
            else:
                # No moves can be made, not in check = Stalemate case
                # Player who cannot move loses.
                if self._turn == "red":
                    self._game_state = "STALEMATE: BLACK WON!"
                else:
                    self._game_state = "STALEMATE: RED WON!"

        return True  # Move completed successfully

    def move_piece(self, current, next):
        """Takes the board coordinates of an attempted move, determines if
        the move is valid and doesn't place the moving player in check."""
        # Create variables to represent piece on current space (if any),
        # and piece on next space (if any)
        current_piece = self._board[current[0]][current[1]]
        next_piece = self._board[next[0]][next[1]]

        # Player can only move own pieces on turn
        if current_piece is None:
            return False
        if self._turn != Piece.get_team(current_piece):  # Player can only move own pieces on their turn
            return False

        # Check to see if current board space is occupied by piece to be moved
        # Check if next board space is occupied by team's own piece
        if next_piece is not None:
            if Piece.get_team(next_piece) == self._turn:
                return False

        # Function to call based on particular movement rules of piece being moved.
        # Check to see if desired move is invalid
        piece_moves = Piece.get_moves(current_piece, self._board)
        if next not in piece_moves:
            # print("Piece function returned FALSE")
            return False

        # If move was valid, update board before checking for 'check' conditions.
        self.update_board(current, next, current_piece, next_piece)

        # If move puts player in check, revert board and return False
        if self.is_in_check(self._turn):
            self.revert_board(current, next, current_piece, next_piece)
            return False

        # If move is valid, and does not put player in 'check', move is made
        return True

    def is_in_check(self, player):
        """Returns whether the specified player is in check"""
        count = 0
        if self.flying_general():  # Check for flying general check/rule
            return True

        # If any black piece is within striking distance of red general,
        # red is in check.
        if player == "red":
            general = Piece.get_space(self._rg)
            for piece in self._bpieces:
                if general in Piece.get_moves(piece, self._board):
                    self._red_check = True
                    count += 1
                    break
            # If no opposing piece has general's space in possible moves,
            # not in check
            if count == 0:
                self._red_check = False

            return self._red_check

        # If any red piece is within striking distance of black general,
        # black is in check.
        elif player == "black":
            general = Piece.get_space(self._bg)
            for piece in self._rpieces:
                if general in Piece.get_moves(piece, self._board):
                    self._black_check = True
                    count += 1
                    break
            # If no opposing piece has general's space in possible moves,
            # not in check
            if count == 0:
                self._black_check = False

            return self._black_check

    def flying_general(self):
        """Flying General Rule: If a move is made that leaves both generals
        in the same row, with no pieces in between, then move is invalid."""
        black_general = Piece.get_space(self._bg)
        red_general = Piece.get_space(self._rg)

        # If generals in same column: Check all spaces in between generals
        # for another piece. Must be a piece to block general sight-line.
        if black_general[1] == red_general[1]:
            for row in range(red_general[0] + 1, black_general[0]):
                if self._board[row][red_general[1]] is not None:
                    return False
            return True  # If in same column, but no pieces blocking sight-line
        else:
            return False  # If not in same column, not in sight-line

    def any_valid_moves(self):
        """Checks to see if a player can make any valid moves without
        putting themselves in check by simulating possible moves"""
        if self._turn == "red":
            # Store check status before simulations.
            check_status = self._red_check
            # Attempt every possible move of every piece, until valid move found
            for piece in self._rpieces:
                current = Piece.get_space(piece)
                for move in Piece.get_moves(piece, self._board):
                    next_piece = self._board[move[0]][move[1]]
                    # If a potential move is valid
                    if self.move_piece(current, move):
                        # Revert board to 'pre-simulation' state
                        self.revert_board(current, move, piece, next_piece)
                        return True
            # Revert check status to 'pre-simulation' state
            self._red_check = check_status

        elif self._turn == "black":
            # Store check status before simulations
            check_status = self._black_check
            # Attempt every possible move of every piece, until valid move found
            for piece in self._bpieces:
                current = Piece.get_space(piece)
                for move in Piece.get_moves(piece, self._board):
                    next_piece = self._board[move[0]][move[1]]
                    # If a potential move is valid
                    if self.move_piece(current, move):
                        # Revert board to 'pre-simulation' state
                        self.revert_board(current, move, piece, next_piece)
                        return True
            # Revert check status to 'pre-simulation' state
            self._black_check = check_status
        return False

    def update_board(self, current, next, current_piece, next_piece):
        """Updates the board when a move is attempted/made"""
        self._board[next[0]][next[1]] = current_piece
        self._board[current[0]][current[1]] = None
        Piece.set_space(current_piece, next)
        if next_piece is not None:
            self.remove_piece(next_piece)

    def revert_board(self, current, next, current_piece, next_piece):
        """Reverts the board to it's previous state if the attempted move
        leaves the player's general in check"""
        self._board[current[0]][current[1]] = current_piece
        self._board[next[0]][next[1]] = next_piece
        Piece.set_space(current_piece, current)
        if next_piece is not None:
            Piece.set_space(next_piece, next)
            self.reinstate_piece(next_piece)

    def remove_piece(self, piece):
        """Removes piece from the active piece lists and sets it's current
        space to None"""
        Piece.set_space(piece, None)
        if piece in self._rpieces:
            self._rpieces.remove(piece)
        elif piece in self._bpieces:
            self._bpieces.remove(piece)

    def reinstate_piece(self, piece):
        """Reinstates a removed piece to it's corresponding active piece list"""
        if Piece.get_team(piece) == "red":
            self._rpieces.append(piece)
        elif Piece.get_team(piece) == "black":
            self._bpieces.append(piece)


class Piece:
    """Parent class for all piece types"""

    def __init__(self, team, type, space):
        """Initializes things"""
        self._team = team
        self._type = type
        self._space = space
        self._possible_moves = []

    def get_team(self):
        """Returns the team of a piece"""
        return self._team

    def get_type(self):
        """Returns the type of piece"""
        return self._type

    def get_space(self):
        """Returns the current space of a piece"""
        return self._space

    def set_space(self, new_space):
        """Updates a pieces current space"""
        self._space = new_space

    def get_moves(self, board):
        """Returns a list of possible moves by the piece, based on
        current board state"""
        self._possible_moves = []
        self.valid_moves(board)
        return self._possible_moves


class General(Piece):
    """General class containing General specific rules"""

    def valid_moves(self, board):
        """Move rules for the general: Must stay within own 'Castle'.
        May move orthogonally one space."""
        # Castle boundaries: rows 7-9 and columns 3-5
        if self._team == "black":
            # Can only move forward from row 8 or 9
            if self._space[0] == 8 or self._space[0] == 9:
                self._possible_moves.append((self._space[0] - 1, self._space[1]))
            # Can only move backward from row 7 or 8
            if self._space[0] == 7 or self._space[0] == 8:
                self._possible_moves.append((self._space[0] + 1, self._space[1]))
            # Can only move right from columns 3 or 4
            if self._space[1] == 3 or self._space[1] == 4:
                self._possible_moves.append((self._space[0], self._space[1] + 1))
            # Can only move left from columns 4 or 5
            if self._space[1] == 4 or self._space[1] == 5:
                self._possible_moves.append((self._space[0], self._space[1] - 1))

        # Castle boundaries: rows 0-2 and columns 3-5
        elif self._team == "red":
            # Can only move forward from row 0 or 1
            if self._space[0] == 0 or self._space[0] == 1:
                self._possible_moves.append((self._space[0] + 1, self._space[1]))
            # Can only move backward from row 1 or 2
            if self._space[0] == 1 or self._space[0] == 2:
                self._possible_moves.append((self._space[0] - 1, self._space[1]))
            # Can only move right from columns 3 or 4
            if self._space[1] == 3 or self._space[1] == 4:
                self._possible_moves.append((self._space[0], self._space[1] + 1))
            # Can only move left from columns 4 or 5
            if self._space[1] == 4 or self._space[1] == 5:
                self._possible_moves.append((self._space[0], self._space[1] - 1))


class Advisor(Piece):
    """Advisor class containing Advisor specific rules"""

    def valid_moves(self, board):
        """Move rules for the advisor: Must stay within own 'Castle'.
        May move diagonally one space."""
        if self._team == "black":
            # Advisors may only occupy 5 different spaces within castle.
            # Castle boundaries: rows 7-9 and columns 3-5
            # Must move to each space diagonally (row +- 1, column +- 1)
            if self._space == (9, 3) or self._space == (9, 5) or \
                    self._space == (7, 3) or self._space == (7, 5):
                self._possible_moves.append((8, 4))
            elif self._space == (8, 4):
                self._possible_moves.append((9, 3))
                self._possible_moves.append((9, 5))
                self._possible_moves.append((7, 3))
                self._possible_moves.append((7, 5))

        elif self._team == "red":
            # Advisors may only occupy 5 different spaces within castle.
            # Castle boundaries: rows 0-2 and columns 3-5
            # Must move to each space diagonally (row +- 1, column +- 1)
            if self._space == (0, 3) or self._space == (0, 5) or \
                    self._space == (2, 3) or self._space == (2, 5):
                self._possible_moves.append((1, 4))
            elif self._space == (1, 4):
                self._possible_moves.append((0, 3))
                self._possible_moves.append((0, 5))
                self._possible_moves.append((2, 3))
                self._possible_moves.append((2, 5))


class Elephant(Piece):
    """Elephant class containing Elephant specific rules"""

    def valid_moves(self, board):
        """Move rules for the elephant: May not cross the river. May only move
        two spaces diagonally. Move cannot be made if first diagonal space is
        occupied. No jumping pieces."""
        # Must not pass river (confined to rows 5-9)
        if self._team == "black":
            # Can only move forward from rows 7 or 9.
            if self._space[0] == 9 or self._space[0] == 7:
                # Can move right if not in far right column
                if self._space[1] < 8:
                    if board[self._space[0] - 1][self._space[1] + 1] is None:
                        self._possible_moves.append((self._space[0] - 2, self._space[1] + 2))
                # Can move left if not in far left column
                if self._space[1] > 0:
                    if board[self._space[0] - 1][self._space[1] - 1] is None:
                        self._possible_moves.append((self._space[0] - 2, self._space[1] - 2))
            # Can only move backwards from rows 5 or 7.
            if self._space[0] == 5 or self._space[0] == 7:
                # Can move right if not in far right column
                if self._space[1] < 8:
                    if board[self._space[0] + 1][self._space[1] + 1] is None:
                        self._possible_moves.append((self._space[0] + 2, self._space[1] + 2))
                # Can move left if not in far left column
                if self._space[1] > 0:
                    if board[self._space[0] + 1][self._space[1] - 1] is None:
                        self._possible_moves.append((self._space[0] + 2, self._space[1] - 2))

        # Must not pass river (confined to rows 0-4)
        elif self._team == "red":
            # Can only move forward from rows 0 or 2
            if self._space[0] == 0 or self._space[0] == 2:
                # Can move right if not in far right column
                if self._space[1] < 8:
                    if board[self._space[0] + 1][self._space[1] + 1] is None:
                        self._possible_moves.append((self._space[0] + 2, self._space[1] + 2))
                # Can move left if not in far left column
                if self._space[1] > 0:
                    if board[self._space[0] + 1][self._space[1] - 1] is None:
                        self._possible_moves.append((self._space[0] + 2, self._space[1] - 2))
            # Can only move backward from row 2 or 4
            if self._space[0] == 2 or self._space[0] == 4:
                # Can move right if not in far right column
                if self._space[1] < 8:
                    if board[self._space[0] - 1][self._space[1] + 1] is None:
                        self._possible_moves.append((self._space[0] - 2, self._space[1] + 2))
                # Can move left if not in far left column
                if self._space[1] > 0:
                    if board[self._space[0] - 1][self._space[1] - 1] is None:
                        self._possible_moves.append((self._space[0] - 2, self._space[1] - 2))


class Horse(Piece):
    """Horse class containing Horse specific rules"""

    def valid_moves(self, board):
        """Move rules for the horse: If immediate orthogonal space is not
        blocked, may move that direction one space, and then one space
        diagonally in either direction AWAY from current space.
        If blocked, cannot move that direction. Move must be 2 row change and
        1 column change, or 2 column change and 1 row change."""

        # Can only move two rows towards row 0 if row >= 2
        if self._space[0] >= 2:
            # Orthogonal space row-1 must be empty
            if board[self._space[0] - 1][self._space[1]] is None:
                # Column +/- 1 must be within bounds
                if self._space[1] > 0:
                    self._possible_moves.append((self._space[0] - 2, self._space[1] - 1))
                if self._space[1] < 8:
                    self._possible_moves.append((self._space[0] - 2, self._space[1] + 1))

        # Can only move two rows towards row 9 if row <= 7
        if self._space[0] <= 7:
            # Orthogonal space row+1 must be empty
            if board[self._space[0] + 1][self._space[1]] is None:
                # Column +/- 1 must be within bounds
                if self._space[1] > 0:
                    self._possible_moves.append((self._space[0] + 2, self._space[1] - 1))
                if self._space[1] < 8:
                    self._possible_moves.append((self._space[0] + 2, self._space[1] + 1))

        # Can only move two columns towards column 0 if column >= 2
        if self._space[1] >= 2:
            # Orthogonal space column-1 must be empty
            if board[self._space[0]][self._space[1] - 1] is None:
                # Row +/- 1 must be within bounds
                if self._space[0] > 0:
                    self._possible_moves.append((self._space[0] - 1, self._space[1] - 2))
                if self._space[0] < 8:
                    self._possible_moves.append((self._space[0] + 1, self._space[1] - 2))

        # Can only move two columns towards column 8 if column <= 6
        if self._space[1] <= 6:
            # Orthogonal space column+1 must be empty
            if board[self._space[0]][self._space[1] + 1] is None:
                # Row +/- 1 must be within bounds
                if self._space[0] > 0:
                    self._possible_moves.append((self._space[0] - 1, self._space[1] + 2))
                if self._space[0] < 8:
                    self._possible_moves.append((self._space[0] + 1, self._space[1] + 2))


class Rook(Piece):
    """Rook class containing Rook specific rules. AKA Chariot"""

    def valid_moves(self, board):
        """Move rules for the rook: May move any distance along the same row
        or the same column, unless the path to the desired space is blocked
        by another piece. No jumping. May take first encountered piece."""

        # Checks self row between self column and first column,
        # until other piece found. Include other piece's space.
        for column in range(1, self._space[1] + 1):
            space = board[self._space[0]][self._space[1] - column]
            if space is None:
                self._possible_moves.append((self._space[0], self._space[1] - column))
            else:
                self._possible_moves.append((self._space[0], self._space[1] - column))
                break

        # Checks self row between self column and last column,
        # until other piece found. Include other piece's space.
        for column in range(self._space[1] + 1, 9):
            space = board[self._space[0]][column]
            if space is None:
                self._possible_moves.append((self._space[0], column))
            else:
                self._possible_moves.append((self._space[0], column))
                break

        # Checks self column between self row and first row,
        # until other piece is found. Include other piece's space.
        for row in range(1, self._space[0] + 1):
            space = board[self._space[0] - row][self._space[1]]
            if space is None:
                self._possible_moves.append((self._space[0] - row, self._space[1]))
            else:
                self._possible_moves.append((self._space[0] - row, self._space[1]))
                break

        # Checks self column between self row and last row,
        # until other piece is found. Include other piece's space.
        for row in range(self._space[0] + 1, 10):
            space = board[row][self._space[1]]
            if space is None:
                self._possible_moves.append((row, self._space[1]))
            else:
                self._possible_moves.append((row, self._space[1]))
                break


class Cannon(Piece):
    """Cannon class containing Cannon specific rules"""

    def valid_moves(self, board):
        """Move rules for the cannon: May move any distance along the same row
        or the same column, unless the path to the desired space is blocked
        by another piece. May not take that piece. May only "jump" first
        encountered piece and move to the next encountered piece in the
        row/column to take the piece. May only jump one piece."""

        # Checks self row between self column and first column,
        # until other piece found. May not take piece, but may
        # jump that piece only to take next encountered piece.
        count = 0
        for column in range(1, self._space[1] + 1):
            space = board[self._space[0]][self._space[1] - column]
            if count == 0 and space is None:
                self._possible_moves.append((self._space[0], self._space[1] - column))
            elif count == 1 and space is not None:
                self._possible_moves.append((self._space[0], self._space[1] - column))
                break
            elif space is not None:
                count += 1

        # Checks self row between self column and last column,
        # until other piece found. May not take piece, but may
        # jump that piece only to take next encountered piece.
        count = 0
        for column in range(self._space[1] + 1, 9):
            space = board[self._space[0]][column]
            if count == 0 and space is None:
                self._possible_moves.append((self._space[0], column))
            elif count == 1 and space is not None:
                self._possible_moves.append((self._space[0], column))
                break
            elif space is not None:
                count += 1

        # Checks self column between self row and first row,
        # until other piece found. May not take piece, but may
        # jump that piece only to take next encountered piece.
        count = 0
        for row in range(1, self._space[0] + 1):
            space = board[self._space[0] - row][self._space[1]]
            if count == 0 and space is None:
                self._possible_moves.append((self._space[0] - row, self._space[1]))
            elif count == 1 and space is not None:
                self._possible_moves.append((self._space[0] - row, self._space[1]))
                break
            elif space is not None:
                count += 1

        # Checks self column between self row and last row,
        # until other piece found. May not take piece, but may
        # jump that piece only to take next encountered piece.
        count = 0
        for row in range(self._space[0] + 1, 10):
            space = board[row][self._space[1]]
            if count == 0 and space is None:
                self._possible_moves.append((row, self._space[1]))
            elif count == 1 and space is not None:
                self._possible_moves.append((row, self._space[1]))
                break
            elif space is not None:
                count += 1


class Soldier(Piece):
    """Soldier class containing Soldier specific rules"""

    def valid_moves(self, board):
        """Move rules for the soldier: May only move one space at a time.
        May only move forward until river is crossed. Once river is crossed,
        may move forward or laterally one space. May never retreat."""
        if self._team == "black":
            if self._space[0] > 4:  # Before river (rows 5-9)
                self._possible_moves.append((self._space[0] - 1, self._space[1]))
            else:  # After river (rows 0-4)
                self._possible_moves.append((self._space[0] - 1, self._space[1]))
                self._possible_moves.append((self._space[0], self._space[1] + 1))
                self._possible_moves.append((self._space[0], self._space[1] - 1))

        elif self._team == "red":
            if self._space[0] < 5:  # Before river (rows 0-4)
                self._possible_moves.append((self._space[0] + 1, self._space[1]))
            else:  # After river (rows 5-9)
                self._possible_moves.append((self._space[0] + 1, self._space[1]))
                self._possible_moves.append((self._space[0], self._space[1] + 1))
                self._possible_moves.append((self._space[0], self._space[1] - 1))


class Board:
    """Class for displaying the Xiangqi game board"""

    def display_board(self, board):
        """Displays the current state of the board in color"""
        from colorama import Fore, Back, Style
        index = 1
        print(Fore.YELLOW + "   --a----b----c----d----e----f----g----h----i--"
              + Style.RESET_ALL)
        for row in board:
            if index == 6:
                print("  ", Fore.YELLOW + Back.BLUE +
                      "~~~~~~~~~~~~~~~~~~~~RIVER~~~~~~~~~~~~~~~~~~~~" +
                      Style.RESET_ALL)
            if index == 10:
                print(Fore.YELLOW + str(index) + "|", end="" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + " " + str(index) + "|",
                      end="" + Style.RESET_ALL)
            for i in range(len(row)):
                if row[i] == None:
                    print(Fore.WHITE + Back.YELLOW + "[  ]",
                          end=" " + Style.RESET_ALL)
                else:
                    columns = 1
                    team = row[i].get_team()[0]
                    type = row[i].get_type()
                    piece = team.upper() + type
                    if team == "r":
                        print(Fore.RED + Back.YELLOW +
                              "[" + piece + "]", end=" " + Style.RESET_ALL)
                    elif team == "b":
                        print(Fore.LIGHTBLUE_EX + Back.YELLOW +
                              "[" + piece + "]", end=" " + Style.RESET_ALL)
                    columns += 1
            print(Fore.YELLOW + "|" + str(index) + Style.RESET_ALL)
            index += 1
        print(Fore.YELLOW + "   --a----b----c----d----e----f----g----h----i--"
              + Style.RESET_ALL)


class Play:
    """Starts a Xiangqi game and plays until finished"""

    def play_game(self):
        """Starts a Xiangqi game, displays the board, informs the players whose turn it is,
        asks for player to move a piece, and makes the move if valid. Ends when a player
        wins the game via Checkmate or Stalemate"""
        game = XiangqiGame()
        while game.get_game_state() == "UNFINISHED":
            Board().display_board(game.get_board())
            if game.is_in_check(game.get_turn()):
                print(game.get_turn().upper(), "is in check")
            print(game.get_turn().upper(), "MOVE")

            current = str(input("Enter the position of the piece you would like to move (ex., 'a1'): "))
            next = str(input("Enter the space you would like to move to (ex., 'a1'): "))
            if not game.make_move(current, next):
                print("Invalid Move")
        Board().display_board(game.get_board())
        print(game.get_game_state())