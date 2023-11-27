import unittest
from ChessVar import ChessVar, ChessPiece, Pawn, Knight, Bishop, Rook, Queen, King

class MyTestCase(unittest.TestCase):

    def test_piece_init_get_methods(self):

        pawn = Pawn('BLACK', 'A2')
        knight = Knight('BLACK', 'A2')
        bishop = Bishop('BLACK', 'A2')
        rook = Rook('BLACK', 'A2')
        queen = Queen('BLACK', 'A2')
        king = King('BLACK', 'A2')

        self.assertEqual(pawn.get_name(), 'BP')
        self.assertEqual(pawn.get_type(), 'PAWN')
        self.assertEqual(knight.get_name(), 'BN')
        self.assertEqual(knight.get_type(), 'KNIGHT')
        self.assertEqual(bishop.get_name(), 'BB')
        self.assertEqual(bishop.get_type(), 'BISHOP')
        self.assertEqual(rook.get_name(), 'BR')
        self.assertEqual(rook.get_type(), 'ROOK')
        self.assertEqual(queen.get_name(), 'BQ')
        self.assertEqual(queen.get_type(), 'QUEEN')
        self.assertEqual(king.get_name(), 'BK')
        self.assertEqual(king.get_type(), 'KING')

    def test_ChessVar_init_get_methods(self):

        game = ChessVar()

        self.assertEqual(game.get_player_turn(), "WHITE")
        self.assertEqual(game.get_game_state(), "UNFINISHED")

    def test_forfeit(self):

        game = ChessVar()

        self.assertFalse(game.forfeit('black'))
        game.forfeit('white')
        self.assertEqual(game.get_game_state(), 'BLACK_WON')

    def test_make_move(self):

        game = ChessVar()
        self.assertFalse(game.make_move('3a', '6a'))  # Try to move a piece from an empty square
        self.assertFalse(game.make_move('7a', '6a')) # White tries to move Black's piece
        game.make_move('2a', '3a')
        self.assertEqual(game.get_player_turn(),'BLACK')
        self.assertFalse(game.make_move('3a', '4a'))  # Black tries to move White's piece


if __name__ == '__main__':
    unittest.main()
