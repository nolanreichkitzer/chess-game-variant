import unittest
from ChessVar import ChessVar, ChessPiece, Pawn, Knight, Bishop, Rook, Queen, King

class MyTestCase(unittest.TestCase):

    def test_piece_init_get_methods(self):

        pawn = Pawn('BLACK')
        knight = Knight('BLACK')
        bishop = Bishop('BLACK')
        rook = Rook('BLACK')
        queen = Queen('BLACK')
        king = King('BLACK')

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

        game.forfeit()
        self.assertEqual(game.get_game_state(), 'BLACK_WON')

    def test_make_move(self):

        game = ChessVar()
        self.assertFalse(game.make_move('a3', 'a6'))  # Try to move a piece from an empty square
        self.assertFalse(game.make_move('a7', 'a6'))  # White tries to move Black's piece
        self.assertFalse(game.make_move('d1', 'd2'))  # White tries to take their own piece
        game.make_move('A2', 'a3')                    # Mix of cases should still work
        self.assertEqual(game.get_player_turn(),'BLACK')
        self.assertFalse(game.make_move('a3', 'a4'))  # Black tries to move White's piece


if __name__ == '__main__':
    unittest.main()
