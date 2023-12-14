# Author: Nolan Reichkitzer
# GitHub username: nolanreichkitzer
# Date: 11/27/2023
# Description: This module contains the ChessVar class that allows the user to play a chess game. There are
#              additional classes used to generate the different chess pieces. The rules of this game are different
#              from the normal rules. In this version, the winner is the first player to capture all of an opponent's
#              pieces of one type. Also, castling, en passant, and pawn promotion are not allowed.

class ChessPiece:
    """
    A class used to represent a Chess piece.  Subclasses of ChessPiece are Pawn, Knight, Bishop, Rook, Queen, and King.
    The subclasses are called by the ChessVar class to populate the chessboard.

    Attributes
    ----------
    color : string
        Represents the color of the chess piece. Data member can either be 'WHITE' or 'BLACK'
    type : string
        Represents the type of ChessPiece. Initialized to None and is overwritten by subclasses
    name : string
        Represents a name identifier for the chess piece. Initialized to None and is overwritten by subclasses

    Methods
    -------
    get_color()
        Returns the color of the chess piece
    get_type()
        Returns the type of chess piece
    get_name()
        Returns the name identifier of the chess piece
    """

    def __init__(self, color):
        self._color = color
        self._type = None
        self._name = None

    def get_color(self):
        """Returns the color of the chess piece"""
        return self._color

    def get_type(self):
        """Returns the type of chess piece"""
        return self._type

    def get_name(self):
        """Returns the name identifier of the chess piece"""
        return self._name


class Pawn(ChessPiece):
    """
    A subclass of ChessPiece used to represent a Pawn

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BP' for a black Pawn or 'WP' for white
    chess_var_object : ChessVar class Object
        ChessVar Object representing the chess game that the chess piece is being used in
        The Pawn's legal_move method needs to access the chessboard data member from ChessVar

    Methods
    -------
    legal_move(source, destination)
        Determines if the proposed move is legal for this type of chess piece
    """

    def __init__(self, color, chess_var_object):
        super().__init__(color)
        self._type = 'PAWN'
        self._name = color[0] + self._type[0]
        self._chess_var_object = chess_var_object

    def legal_move(self, source, destination):
        """
        Determines if the proposed move is legal for this type of chess piece

        :param source: a string representing the current grid location of the piece to be moved
        :param destination: a string representing the proposed destination of the piece to be moved
        :return: True if the move is legal. False if the move is illegal.
        """
        # Store row and column values, use ord function to convert column character to ASCII integer
        source_column = ord(source[0])
        source_row = int(source[1])
        destination_column = ord(destination[0])
        destination_row = int(destination[1])

        # Use ChessVar get_board method to return the chessboard dictionary to this class
        chessboard = self._chess_var_object.get_board()

        # Determine legal moves for White pawn

        if self._color == 'WHITE':

            # White can only move from row 2 to 8, and can move 2 spaces forward if source space is on row 2
            if source_row == 2 and (destination_row - source_row) == 2 and \
                    (destination_column - source_column) == 0 and not chessboard[destination]:
                return True

            # Normally, Pawns can only move forward 1 space and can't capture while moving forward
            elif (destination_row - source_row) == 1 and (destination_column - source_column) == 0 \
                    and not chessboard[destination]:
                return True

            # Pawn can move forward 1 space diagonally if it is capturing an enemy piece
            elif (destination_row - source_row) == 1 and abs(destination_column - source_column) == 1 \
                    and chessboard[destination] and chessboard[destination].get_color() == 'BLACK':
                return True

            else:
                return False

        # Determine legal moves for Black pawn
        else:

            # Black can only move from row 7 to 1, and can move 2 spaces forward if source space is on row 7
            if source_row == 7 and (source_row - destination_row) == 2 and \
                    (destination_column - source_column) == 0 and not chessboard[destination]:
                return True

            # Normally, Pawns can only move forward 1 space and can't capture while moving forward
            elif (source_row - destination_row) == 1 and (destination_column - source_column) == 0 \
                    and not chessboard[destination]:
                return True

            # Pawn can move forward 1 space diagonally if it is capturing an enemy piece
            elif (source_row - destination_row) == 1 and abs(destination_column - source_column) == 1 \
                    and chessboard[destination] and chessboard[destination].get_color() == 'WHITE':
                return True

            else:
                return False


class Knight(ChessPiece):
    """
    A subclass of ChessPiece used to represent a Knight

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BN' for a black Knight or 'WN' for white

    Methods
    -------
    legal_move(source, destination)
        Determines if the proposed move is legal for this type of chess piece
    """

    def __init__(self, color):
        super().__init__(color)
        self._type = 'KNIGHT'
        self._name = color[0] + 'N'

    def legal_move(self, source, destination):
        """
        Determines if the proposed move is legal for this type of chess piece

        :param source: a string representing the current grid location of the piece to be moved
        :param destination: a string representing the proposed destination of the piece to be moved
        :return: True if the move is legal. False if the move is illegal.
        """
        # Store row and column values, use ord function to convert column character to ASCII integer
        source_column = ord(source[0])
        source_row = int(source[1])
        destination_column = ord(destination[0])
        destination_row = int(destination[1])

        # Determine legal moves for Knights

        # Knights can move forward/backward 2 spaces and left/right 1 space
        if abs(destination_row - source_row) == 2 and abs(destination_column - source_column) == 1:
            return True

        # Or Knights can move forward/backward one space and left/right 2 spaces
        elif abs(destination_row - source_row) == 1 and abs(destination_column - source_column) == 2:
            return True

        else:
            return False


class Bishop(ChessPiece):
    """
    A subclass of ChessPiece used to represent a Bishop

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BB' for a black Bishop or 'WB' for white

    Methods
    -------
    legal_move(source, destination)
        Determines if the proposed move is legal for this type of chess piece
    """

    def __init__(self, color):
        super().__init__(color)
        self._type = 'BISHOP'
        self._name = color[0] + self._type[0]

    def legal_move(self, source, destination):
        """
        Determines if the proposed move is legal for this type of chess piece

        :param source: a string representing the current grid location of the piece to be moved
        :param destination: a string representing the proposed destination of the piece to be moved
        :return: True if the move is legal. False if the move is illegal.
        """
        # Store row and column values, use ord function to convert column character to ASCII integer
        source_column = ord(source[0])
        source_row = int(source[1])
        destination_column = ord(destination[0])
        destination_row = int(destination[1])

        # Determine legal moves for Bishops

        # Bishops can move diagonally any number of spaces in either direction
        if abs(destination_row - source_row) == abs(destination_column - source_column):
            return True
        else:
            return False


class Rook(ChessPiece):
    """
    A subclass of ChessPiece used to represent a Rook

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BR' for a black Rook or 'WR' for white

    Methods
    -------
    legal_move(source, destination)
        Determines if the proposed move is legal for this type of chess piece
    """

    def __init__(self, color):
        super().__init__(color)
        self._type = 'ROOK'
        self._name = color[0] + self._type[0]

    def legal_move(self, source, destination):
        """
        Determines if the proposed move is legal for this type of chess piece

        :param source: a string representing the current grid location of the piece to be moved
        :param destination: a string representing the proposed destination of the piece to be moved
        :return: True if the move is legal. False if the move is illegal.
        """
        # Store row and column values, use ord function to convert column character to ASCII integer
        source_column = ord(source[0])
        source_row = int(source[1])
        destination_column = ord(destination[0])
        destination_row = int(destination[1])

        # Determine legal moves for Rooks

        # Rooks can move vertically any number of spaces or horizontally any number of spaces
        if (destination_row - source_row) == 0 or (destination_column - source_column) == 0:
            return True
        else:
            return False


class Queen(ChessPiece):
    """
    A subclass of ChessPiece used to represent a Queen

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BQ' for a black Queen or 'WQ' for white

    Methods
    -------
    legal_move(source, destination)
        Determines if the proposed move is legal for this type of chess piece
    """
    def __init__(self, color):
        super().__init__(color)
        self._type = 'QUEEN'
        self._name = color[0] + self._type[0]

    def legal_move(self, source, destination):
        """
        Determines if the proposed move is legal for this type of chess piece

        :param source: a string representing the current grid location of the piece to be moved
        :param destination: a string representing the proposed destination of the piece to be moved
        :return: True if the move is legal. False if the move is illegal.
        """
        # Store row and column values, use ord function to convert column character to ASCII integer
        source_column = ord(source[0])
        source_row = int(source[1])
        destination_column = ord(destination[0])
        destination_row = int(destination[1])

        # Determine legal moves for Queen

        # Queen can move vertically, horizontally, or diagonally any number of spaces in any direction
        if abs(destination_row - source_row) == abs(destination_column - source_column):
            return True
        elif (destination_row - source_row) == 0 or (destination_column - source_column) == 0:
            return True
        else:
            return False


class King(ChessPiece):
    """
    A subclass of ChessPiece used to represent a King

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BK' for a black King or 'WK' for white

    Methods
    -------
    legal_move(source, destination)
        Determines if the proposed move is legal for this type of chess piece
    """

    def __init__(self, color):
        super().__init__(color)
        self._type = 'KING'
        self._name = color[0] + self._type[0]

    def legal_move(self, source, destination):
        """
        Determines if the proposed move is legal for this type of chess piece

        :param source: a string representing the current grid location of the piece to be moved
        :param destination: a string representing the proposed destination of the piece to be moved
        :return: True if the move is legal. False if the move is illegal.
        """
        # Store row and column values, use ord function to convert column character to ASCII integer
        source_column = ord(source[0])
        source_row = int(source[1])
        destination_column = ord(destination[0])
        destination_row = int(destination[1])

        # King can move one space in any direction
        if abs(destination_column - source_column) <= 1 and abs(destination_row - source_row) <= 1:
            return True
        else:
            return False


class ChessVar:
    """
    A class used to represent a Chess game. The game is a variant of Chess with different rules.

    The starting position for the game is the normal starting position for standard chess. This class keeps track of
    the player's turn with white having the first turn. The winner is the first player to capture all of an opponent's
    pieces of one type. The king isn't a special piece in this game, and there is no check or checkmate. Pieces move
    and capture the same as in normal chess, except that there is no castling, en passant, or pawn promotion.

    Locations on the board are specified using "algebraic notation", with columns labeled a-h and rows labeled 1-8.


    Attributes
    ----------
    chessboard : dictionary
        A dictionary representing the chessboard grid. Keys are the chessboard grid squares, values are ChessPiece
        objects occupying the squares. Dictionary is initialized to the starting state of a normal chess game using the
        set_board method and will be populated by ChessPiece objects.
    piece_inventory : dictionary
        A dictionary representing the piece inventory with piece names as keys and piece counts as values.
        Dictionary is initialized to empty dictionary and filled after the chessboard is set using the
        update_piece_inventory method. This dictionary keeps track of white and black pieces separately.
    player_turn : string
        Represents who has the current turn. Data member will either be 'WHITE' or 'BLACK' and is initialized to 'WHITE'
    game_state : string
        Represents the status of the game. Data member is initialized to 'UNFINISHED' and will be set to 'WHITE_WON'
        if white makes a winning move or 'BLACK_WON' if black makes a winning move

    Methods
    -------
    set_board()
        Populates the chessboard data member with ChessPiece Objects.
    get_board()
        Returns the chessboard dictionary
    display_board()
        Displays the current chessboard arrangement to the user
    update_piece_inventory()
        Updates the piece_inventory data member with current ChessPiece counts
    display_piece_inventory():
        Displays the piece_inventory dictionary to the user
    get_player_turn()
        Returns the player who has the current turn
    swap_player_turn()
        Switches current player_turn to the other player
    get_game_state()
        Returns the value of the game_state data member
    current_player_wins()
        Sets game_state data member to 'WHITE_WON' if it is white's turn or 'BLACK_WON' if it is black's turn
    forfeit()
        Sets game_state data member to 'BLACK_WON' if it is white's turn or 'WHITE_WON' if it is black's turn
    make_move(source, destination)
        Takes a piece's source square and proposed destination as strings and moves the piece if it is a legal move
    make_move_and_display_board(source, destination):
        Calls the make_move and display_board methods if the user wants to automatically display the board
    spaces_between_source_and_destination_clear(source, destination)
        Determines if the spaces in between the source and destination squares are clear.
    """

    def __init__(self):
        self._chessboard = {}
        self._piece_inventory = {}
        self.set_board()
        self.update_piece_inventory()
        self._player_turn = 'WHITE'
        self._game_state = 'UNFINISHED'

    def set_board(self):
        """Populates the chessboard data member with ChessPiece Objects"""

        # Populate blank spaces for every square of the chessboard
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for row in range(8, 0, -1):
            for column in columns:
                self._chessboard[str(column) + str(row)] = None

        # Generate Black Pawns
        for column in columns:
            self._chessboard[str(column) + '7'] = Pawn('BLACK', self)

        # Generate Black Knights
        self._chessboard['b8'] = Knight('BLACK')
        self._chessboard['g8'] = Knight('BLACK')

        # Generate Black Bishops
        self._chessboard['c8'] = Bishop('BLACK')
        self._chessboard['f8'] = Bishop('BLACK')

        # Generate Black Rooks
        self._chessboard['a8'] = Rook('BLACK')
        self._chessboard['h8'] = Rook('BLACK')

        # Generate Black Queen
        self._chessboard['d8'] = Queen('BLACK')

        # Generate Black King
        self._chessboard['e8'] = King('BLACK')

        # Generate White Pawns
        for column in columns:
            self._chessboard[str(column) + '2'] = Pawn('WHITE', self)

        # Generate White Knights
        self._chessboard['b1'] = Knight('WHITE')
        self._chessboard['g1'] = Knight('WHITE')

        # Generate White Bishops
        self._chessboard['c1'] = Bishop('WHITE')
        self._chessboard['f1'] = Bishop('WHITE')

        # Generate White Rooks
        self._chessboard['a1'] = Rook('WHITE')
        self._chessboard['h1'] = Rook('WHITE')

        # Generate White Queen
        self._chessboard['d1'] = Queen('WHITE')

        # Generate White King
        self._chessboard['e1'] = King('WHITE')

    def get_board(self):
        """Returns the chessboard dictionary"""
        return self._chessboard

    def display_board(self):
        """Displays the current chessboard arrangement to the user"""
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Print column headings
        print('  ', end='')
        for column in columns:
            print(' ' + column + '  ', end='')
        print('')

        # Print one row at a time
        for row in range(8, 0, -1):
            print(str(row) + ' ', end='')
            for column in columns:
                if self._chessboard[str(column) + str(row)]:
                    print('[' + self._chessboard[str(column) + str(row)].get_name() + ']', end='')
                else:
                    print('[  ]', end='')
            print(' ' + str(row), end='')
            print('')

        # Print column headings
        print('  ', end='')
        for column in columns:
            print(' ' + column + '  ', end='')
        print('\n')

    def update_piece_inventory(self):
        """Updates the piece_inventory data member with current ChessPiece counts"""

        # If piece_inventory is empty, initialize key-value pairs with piece name as keys
        if self._piece_inventory == {}:

            name_list = []

            # Generate list of piece names to use as keys
            for piece in self._chessboard.values():
                if piece and piece.get_name() not in name_list:
                    name_list.append(piece.get_name())

            # Sort the name list in alphabetical order
            name_list.sort()

            # Initialize each value in dictionary to 0
            for name in name_list:
                self._piece_inventory[name] = 0

        # Set existing counts in the dictionary to 0
        for piece in self._piece_inventory:
            self._piece_inventory[piece] = 0

        # Recount existing ChessPiece objects on chessboard
        for piece in self._chessboard.values():
            if piece:
                self._piece_inventory[piece.get_name()] = self._piece_inventory[piece.get_name()] + 1

    def display_piece_inventory(self):
        """Displays the piece_inventory dictionary to the user"""
        print(self._piece_inventory)

    def get_player_turn(self):
        """Returns the player who has the current turn"""
        return self._player_turn

    def swap_player_turn(self):
        """Switches current player_turn to the other player"""
        if self._player_turn == 'WHITE':
            self._player_turn = 'BLACK'
        else:
            self._player_turn = 'WHITE'

    def get_game_state(self):
        """Returns the value of the game_state data member"""
        return self._game_state

    def current_player_wins(self):
        """Sets game_state data member to 'WHITE_WON' if it is white's turn or 'BLACK_WON' if it is black's turn"""
        if self._player_turn == 'WHITE':
            self._game_state = 'WHITE_WON'
        else:
            self._game_state = 'BLACK_WON'

        # Display the game state to show who won
        print(self.get_game_state())

    def forfeit(self):
        """Sets game_state data member to 'BLACK_WON' if it is white's turn or 'WHITE_WON' if it is black's turn"""
        if self._game_state == 'UNFINISHED':
            if self._player_turn == 'WHITE':
                self._game_state = 'BLACK_WON'
            else:
                self._game_state = 'WHITE_WON'

            # Display the game state to show who won
            print(self.get_game_state())

    def make_move(self, source, destination):
        """
        Takes a piece's source square and proposed destination and moves the piece if it is a legal move

        :param source: a string representing the current grid location of the piece to be moved
                              Example: '2a'   - not case-sensitive
        :param destination: a string representing the proposed destination of the piece to be moved
                              Example: '3a'   - not case-sensitive
        :return: True if move is legal. False if move is illegal.
                 Updates the chessboard dictionary if move is legal
                 Updates the piece_inventory dictionary if a piece was taken
        """

        # Convert entered string to lowercase to avoid case sensitivity problems
        source = source.lower()
        destination = destination.lower()

        # Check if game has already been won
        if self._game_state != 'UNFINISHED':
            print('This game has already been won!')
            print(self.get_game_state())
            return False

        # Check that source and destination entries are actually board spaces
        # Entries can only be 2 character strings
        if len(source) != 2 or len(destination) != 2:
            print("One or both of your move entries is invalid.")
            return False

        # Store row and column values
        source_column = source[0]
        source_row = source[1]
        destination_column = destination[0]
        destination_row = destination[1]

        # Check that source and destination entries are actually board spaces
        # Columns must be between a and h (inclusive). Rows must be between 1 and 8 (inclusive).
        if source_column < 'a' or source_column > 'h' or destination_column < 'a' or destination_column > 'h' or \
                destination_row < '1' or destination_row > '8' or source_row < '1' or source_row > '8':
            print("One or both of your move entries is invalid.")
            return False

        # Check that a piece was selected
        if not self._chessboard[source]:
            print("You didn't select a piece to move. Try a different move.")
            return False

        # Check that the player selected their own piece
        if self._player_turn != self._chessboard[source].get_color():
            print("You can't move the other player's piece. Try a different move.")
            return False

        # Check that the source and destination positions are different
        if source == destination:
            print("You didn't actually move the piece. Try a different move.")
            return False

        # Determine if the selected piece can actually make the proposed move
        if not self._chessboard[source].legal_move(source, destination):
            print("That move isn't legal for this piece. Try a different move.")
            return False

        # Determine if the player tried to move through other chess pieces. Only the Knight can do this.
        if self._chessboard[source].get_type() != 'KNIGHT' and \
                not self.spaces_between_source_and_destination_clear(source, destination):
            print("You tried to move through other chess pieces. Only the Knight can do that. Try a different move")
            return False

        # Check that the player does not try to remove their own piece from the board
        if self._chessboard[destination] and self._player_turn == self._chessboard[destination].get_color():
            print("You can't remove your own piece from the board. Try a different move.")
            return False

        # If all previous tests pass, the move is legal
        # Make the move and update the chessboard
        self._chessboard[destination] = self._chessboard[source]
        self._chessboard[source] = None

        # See if the move was a winning move by updating the piece inventory and seeing if any class of ChessPiece was
        # completely removed from the board
        self.update_piece_inventory()
        if 0 in self._piece_inventory.values():
            self.current_player_wins()

        # Give turn to the other player
        self.swap_player_turn()

        return True

    def make_move_and_display_board(self, source, destination):
        """Calls the make_move and display_board methods if the user wants to automatically display the board"""
        self.make_move(source, destination)
        self.display_board()

    def spaces_between_source_and_destination_clear(self, source, destination):
        """
        Determines if the spaces in between the source and destination squares are clear.

        :param source: a string representing the current grid location of the piece to be moved
        :param destination: a string representing the proposed destination of the piece to be moved
        :return: True if the spaces are clear. False if any of the spaces are not clear.
        """

        # Store row and column values, use ord function to convert column character to ASCII integer
        source_column = ord(source[0])
        source_row = int(source[1])
        destination_column = ord(destination[0])
        destination_row = int(destination[1])

        # Determine if there is a chess piece in between source square and destination square
        # The Knight is the only piece that can move through (jump over) other chess pieces

        # Vertical move forward (1 to 8)
        if (source_column - destination_column) == 0 and (destination_row - source_row) > 0:
            for row in range(1, destination_row - source_row):
                if self._chessboard[chr(source_column) + str(source_row + row)]:
                    return False
            return True

        # Vertical move backward (8 to 1)
        if (source_column - destination_column) == 0 and (source_row - destination_row) > 0:
            for row in range(1, source_row - destination_row):
                if self._chessboard[chr(source_column) + str(source_row - row)]:
                    return False
            return True

        # Horizontal move right (a to h)
        if (source_row - destination_row) == 0 and (destination_column - source_column) > 0:
            for column in range(1, destination_column - source_column):
                if self._chessboard[chr(source_column + column) + str(source_row)]:
                    return False
            return True

        # Horizontal move left (h to a)
        if (source_row - destination_row) == 0 and (source_column - destination_column) > 0:
            for column in range(1, source_column - destination_column):
                if self._chessboard[chr(source_column - column) + str(source_row)]:
                    return False
            return True

        # Diagonal move forward right (1 to 8) and (a to h)
        if (destination_row - source_row) > 0 and (destination_column - source_column) > 0:
            for square in range(1, destination_row - source_row):
                if self._chessboard[chr(source_column + square) + str(source_row + square)]:
                    return False
            return True

        # Diagonal move forward left (1 to 8) and (h to a)
        if (destination_row - source_row) > 0 and (source_column - destination_column) > 0:
            for square in range(1, destination_row - source_row):
                if self._chessboard[chr(source_column - square) + str(source_row + square)]:
                    return False
            return True

        # Diagonal move backward right (8 to 1) and (a to h)
        if (source_row - destination_row) > 0 and (destination_column - source_column) > 0:
            for square in range(1, source_row - destination_row):
                if self._chessboard[chr(source_column + square) + str(source_row - square)]:
                    return False
            return True

        # Diagonal move backward left (8 to 1) and (h to a)
        if (source_row - destination_row) > 0 and (source_column - destination_column) > 0:
            for square in range(1, source_row - destination_row):
                if self._chessboard[chr(source_column - square) + str(source_row - square)]:
                    return False
            return True
