# Author: Nolan Reichkitzer
# GitHub username: nolanreichkitzer
# Date: 11/27/2023
# Description: CS 162 - Portfolio Project

class ChessPiece:
    """
    A class used to represent a Chess piece

    Attributes
    ----------
    color : string
        Represents the color of the chess piece. Data member can either be 'WHITE' or 'BLACK'
    location : string
        Represents the current location of the chess piece on the chessboard
    status : string
        Represents the status of the chess piece. Data member is 'ACTIVE' or 'TAKEN'
    type : string
        Represents the type of ChessPiece. Initialized to None and is overwritten by subclasses
    name : string
        Represents a name identifier for the chess piece. Initialized to None and is overwritten by subclasses

    Methods
    -------
    get_color()
        Returns the color of the chess piece
    get_status()
        Returns the status of the chess piece
    get_type()
        Returns the type of chess piece
    get_name()
        Returns the name identifier of the chess piece
    """

    def __init__(self, color, location):
        self._color = color
        self._location = location
        self._status = 'ACTIVE'
        self._type = None
        self._name = None

    def get_color(self):
        """Returns the color of the chess piece"""
        return self._color

    def get_status(self):
        """Returns the status of the chess piece"""
        return self._status

    def get_type(self):
        """Returns the type of chess piece"""
        return self._type

    def get_name(self):
        """Returns the name identifier of the chess piece"""
        return self._name


class Pawn(ChessPiece):
    """
    A subclass used to represent a Pawn chess piece

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BP' for a black Pawn or 'WP' for white
    Methods
    -------

    """

    def __init__(self, color, location):
        super().__init__(color, location)
        self._type = 'PAWN'
        self._name = color[0] + self._type[0]


class Knight(ChessPiece):
    """
    A subclass used to represent a KNIGHT chess piece

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BN' for a black Knight or 'WN' for white
    Methods
    -------

    """

    def __init__(self, color, location):
        super().__init__(color, location)
        self._type = 'KNIGHT'
        self._name = color[0] + 'N'


class Bishop(ChessPiece):
    """
    A subclass used to represent a Bishop chess piece

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BB' for a black Bishop or 'WB' for white
    Methods
    -------

    """

    def __init__(self, color, location):
        super().__init__(color, location)
        self._type = 'BISHOP'
        self._name = color[0] + self._type[0]


class Rook(ChessPiece):
    """
    A subclass used to represent a Rook chess piece

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BR' for a black Rook or 'WR' for white
    Methods
    -------

    """

    def __init__(self, color, location):
        super().__init__(color, location)
        self._type = 'ROOK'
        self._name = color[0] + self._type[0]


class Queen(ChessPiece):
    """
    A subclass used to represent a Queen chess piece

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BQ' for a black Queen or 'WQ' for white
    Methods
    -------

    """

    def __init__(self, color, location):
        super().__init__(color, location)
        self._type = 'QUEEN'
        self._name = color[0] + self._type[0]


class King(ChessPiece):
    """
    A subclass used to represent a King chess piece

    Attributes
    ----------
    In addition to ChessPiece Attributes

    type : string
        Represents the type of ChessPiece (same as the name of this class)
    name : string
        Represents a name identifier for the chess piece. 'BK' for a black King or 'WK' for white
    Methods
    -------

    """

    def __init__(self, color, location):
        super().__init__(color, location)
        self._type = 'KING'
        self._name = color[0] + self._type[0]


class ChessVar:
    """
    A class used to represent a Chess game

    Attributes
    ----------
    chessboard : dictionary
        A dictionary representing the chessboard grid. Initialized to the starting state of a normal chess game using
        set_board method
    player_turn : string
        Represents who has the current turn. Data member will either be 'WHITE' or 'BLACK' and is initialized to 'WHITE'
    game_state : string
        Represents the status of the game. Data member is initialized to 'UNFINISHED' and will be set to 'WHITE_WON'
        if white makes a winning move or 'BLACK_WON' if black makes a winning move

    Methods
    -------
    set_board()
        Populates the chessboard data member with ChessPiece Objects
    display_board()
        Displays the current chessboard arrangement to the user
    get_player_turn()
        Returns the player who has the current turn
    swap_player_turn()
        Switches current player_turn to the other player
    get_game_state()
        Returns the value of the game_state data member
    white_wins()
        Sets game_state data member to 'WHITE_WON'
    black_wins()
        Sets game_state data member to 'BLACK_WON'
    forfeit(player)
        Allows the player who has the current turn to forfeit the game
    make_move(current_square, destination)
        Takes a piece's current square and proposed destination as strings and moves the piece if it is a legal move
    """

    def __init__(self):
        self._chessboard = {}
        self.set_board()
        self._player_turn = 'WHITE'
        self._game_state = 'UNFINISHED'

    def set_board(self):
        """Populates the chessboard data member with ChessPiece Objects"""

        # Populate blank spaces for every square of the chessboard
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for row in range(8, 0, -1):
            for column in columns:
                self._chessboard[str(row) + str(column)] = None

        # Generate Black Pawns
        for column in columns:
            self._chessboard['7' + str(column)] = Pawn('BLACK', '7' + str(column))

        # Generate Black Knights
        self._chessboard['8b'] = Knight('BLACK', '8b')
        self._chessboard['8g'] = Knight('BLACK', '8g')

        # Generate Black Bishops
        self._chessboard['8c'] = Bishop('BLACK', '8c')
        self._chessboard['8f'] = Bishop('BLACK', '8f')

        # Generate Black Rooks
        self._chessboard['8a'] = Rook('BLACK', '8a')
        self._chessboard['8h'] = Rook('BLACK', '8h')

        # Generate Black Queen
        self._chessboard['8d'] = Queen('BLACK', '8d')

        # Generate Black King
        self._chessboard['8e'] = King('BLACK', '8e')

        # Generate White Pawns
        for column in columns:
            self._chessboard['2' + str(column)] = Pawn('WHITE', '2' + str(column))

        # Generate White Knights
        self._chessboard['1b'] = Knight('WHITE', '1b')
        self._chessboard['1g'] = Knight('WHITE', '1g')

        # Generate White Bishops
        self._chessboard['1c'] = Bishop('WHITE', '1c')
        self._chessboard['1f'] = Bishop('WHITE', '1f')

        # Generate White Rooks
        self._chessboard['1a'] = Rook('WHITE', '1a')
        self._chessboard['1h'] = Rook('WHITE', '1h')

        # Generate White Queen
        self._chessboard['1d'] = Queen('WHITE', '1d')

        # Generate White King
        self._chessboard['1e'] = King('WHITE', '1e')

    def display_board(self):
        """Displays the current chessboard arrangement to the user"""
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Print column headings
        print('  ', end='')
        for column in columns:
            print(' ' + column + '  ', end='')
        print('')

        for row in range(8, 0, -1):
            print(str(row) + ' ', end='')
            for column in columns:
                if self._chessboard[str(row) + str(column)]:
                    print('[' + self._chessboard[str(row) + str(column)].get_name() + ']', end='')
                else:
                    print('[  ]', end='')
            print(' ' + str(row), end='')
            print('')

        # Print column headings
        print('  ', end='')
        for column in columns:
            print(' ' + column + '  ', end='')
        print('\n')

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

    def white_wins(self):
        """Sets game_state data member to 'WHITE_WON'"""
        self._game_state = 'WHITE_WON'

    def black_wins(self):
        """Sets game_state data member to 'BLACK_WON'"""
        self._game_state = 'BLACK_WON'

    def forfeit(self, player):
        """
        Allows the player who has the current turn to forfeit the game

        :param player: A string representing the player wishing to forfeit.
               Accepted input is either 'WHITE' or 'BLACK' (not case-sensitive)
        :return: False if invalid forfeit. Updates the game_state data member appropriately if valid forfeit
        """
        player = player.upper()

        if player == 'WHITE' and self._player_turn == 'WHITE':
            self.black_wins()

        elif player == 'BLACK' and self._player_turn == 'BLACK':
            self.white_wins()

        else:
            print("Please wait to forfeit until it is your turn.")
            return False

    def make_move(self, current_square, destination):
        """
        Takes a piece's current square and proposed destination and moves the piece if it is a legal move

        :param current_square: a string representing the current grid location of the piece to be moved
                              Example: '2a'   - not case-sensitive
        :param destination: a string representing the proposed destination of the piece to be moved
                              Example: '3a'   - not case-sensitive
        :return: No returns. Updates the chessboard dictionary if move is legal
        """

        # Convert entered string to lowercase to avoid case sensitivity problem
        current_square = current_square.lower()
        destination = destination.lower()

        if self._player_turn != self._chessboard[current_square].get_color():
            return False

        # Since the move is legal, make the move and change player_turn
        self._chessboard[destination] = self._chessboard[current_square]
        self._chessboard[current_square] = None
        self.swap_player_turn()

        # See if the move was a winning move

        return True

def main():
    game = ChessVar()
    game.display_board()
    print(game.make_move('2a', '7a'))
    game.display_board()


if __name__ == '__main__':
    main()
