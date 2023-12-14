# Author: Nolan Reichkitzer
# GitHub username: nolanreichkitzer
# Date: 11/27/2023
# Description: Unit Tests for ChessVar.py

import unittest
from ChessVar import ChessVar, Pawn, Knight, Bishop, Rook, Queen, King

class MyTestCase(unittest.TestCase):

    def test_piece_init_get_methods(self):

        game = ChessVar()

        pawn = Pawn('BLACK', game)
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
        self.assertTrue(game.make_move('A2', 'a3'))   # Mix of cases should still work
        self.assertEqual(game.get_player_turn(),'BLACK')
        self.assertFalse(game.make_move('a3', 'a4'))  # Black tries to move White's piece

    def test_pawn_move(self):
        game = ChessVar()
        self.assertFalse(game.make_move('a2', 'b3')) # White tries to move diagonal without capturing
        self.assertFalse(game.make_move('d2', 'd5')) # White tries to move 3 spaces forward
        self.assertFalse(game.make_move('d2', 'f4')) # White tries to move 2 spaces diagonal
        self.assertTrue(game.make_move('d2', 'd4'))  # White moves 2 spaces from starting row
        self.assertFalse(game.make_move('e7', 'd6')) # Black tries to move diagonal without capturing
        self.assertTrue(game.make_move('e7', 'e5')) # Black moves 2 spaces from starting row
        self.assertTrue(game.make_move('d4', 'e5')) # White captures diagonal
        self.assertTrue(game.make_move('c7', 'c6')) # Black moves 1 space forward
        game.make_move('c2', 'c4')
        game.make_move('c6', 'c5')
        self.assertFalse(game.make_move('c4', 'c5')) # White tries to move forward into black piece
        game.make_move('a2', 'a3')
        self.assertFalse(game.make_move('c5', 'c4'))  # Black tries to move forward into white piece
        game.make_move('b7', 'b5')
        game.make_move('a3', 'a4')
        self.assertTrue(game.make_move('b5', 'a4'))  # Black captures diagonal
        game.make_move('h2', 'h3')
        game.make_move('g7', 'g6')
        self.assertFalse(game.make_move('h3', 'h5')) # White tries to move 2 spaces forward after 1st move
        self.assertTrue(game.make_move('h3', 'h4'))  # White tries to move 1 space forward
        self.assertFalse(game.make_move('g6', 'g4'))  # Black tries to move 2 spaces forward after 1st move
        self.assertTrue(game.make_move('g6', 'g5'))  # Black tries to move 1 space forward


    def test_knight_move(self):
        game = ChessVar()
        self.assertFalse(game.make_move('b1', 'd2')) # Knight tries to capture own piece
        self.assertTrue(game.make_move('b1', 'c3')) # Knight moves normally
        self.assertTrue(game.make_move('g8', 'f6')) # Black knight moves normally
        game.make_move('g1', 'f3')
        game.make_move('f6', 'e4')
        self.assertTrue(game.make_move('c3', 'e4')) # White knight captures black knight
        game.make_move('b8', 'c6')
        game.make_move('f3', 'd4')
        game.make_move('g7', 'g6')
        game.make_move('d4', 'c6')
        self.assertEqual(game.get_game_state(), 'WHITE_WON') # White takes both black knights and wins

    def test_bishop_move(self):
        game = ChessVar()
        self.assertFalse(game.make_move('c1', 'h6')) # Bishop can't move through pawns
        self.assertTrue(game.make_move('d2', 'd3')) # Pawn moves out of the way
        self.assertFalse(game.make_move('c1', 'g5'))  # White tries to move out of turn
        self.assertTrue(game.make_move('g7', 'g5')) # Black pawn moves 2 spaces
        self.assertFalse(game.make_move('c1', 'h6')) # Bishop tries to move through black pawn
        self.assertTrue(game.make_move('c1', 'g5'))  # Bishop takes black pawn instead
        game.make_move('e7', 'e6')
        self.assertFalse(game.make_move('g5', 'g7'))  # Bishop tries to move vertically
        self.assertFalse(game.make_move('g5', 'd5'))  # Bishop tries to move horizontally
        self.assertTrue(game.make_move('g5', 'd8'))  # Bishop takes black queen
        self.assertEqual(game.get_game_state(), 'WHITE_WON')  # White wins

    def test_rook_move(self):
        game = ChessVar()
        self.assertFalse(game.make_move('a1', 'a7')) # Rook can't move through pawns
        self.assertTrue(game.make_move('a2', 'a4')) # Pawn moves out of the way
        self.assertTrue(game.make_move('e7', 'e6')) # Black pawn moves 1 space
        self.assertTrue(game.make_move('a1', 'a3')) # Rook moves forward
        self.assertTrue(game.make_move('e6', 'e5'))  # Black pawn moves 1 space
        self.assertFalse(game.make_move('a3', 'e6'))  # Rook attempts to move diagonally
        self.assertTrue(game.make_move('a3', 'e3'))  # Rook moves horizontally
        self.assertTrue(game.make_move('e5', 'e4'))  # Black pawn moves 1 space
        self.assertFalse(game.make_move('e3', 'e8'))  # Rook attempts to move through Pawn
        self.assertTrue(game.make_move('e3', 'e4'))  # Rook takes Pawn
        self.assertTrue(game.make_move('h7', 'h6'))  # Black pawn moves 1 space
        self.assertTrue(game.make_move('e4', 'e8'))  # Rook takes black king
        self.assertEqual(game.get_game_state(), 'WHITE_WON')  # White wins

    def test_queen_move(self):
        game = ChessVar()
        self.assertFalse(game.make_move('d1', 'd8')) # Queen can't move through pawns
        self.assertTrue(game.make_move('e2', 'e4')) # Pawn moves out of the way
        self.assertTrue(game.make_move('e7', 'e6')) # Black pawn moves 1 space
        self.assertTrue(game.make_move('d1', 'f3')) # Queen moves diagonally
        self.assertTrue(game.make_move('e6', 'e5'))  # Black pawn moves 1 space
        self.assertTrue(game.make_move('f3', 'd3'))  # Queen moves horizontally
        self.assertTrue(game.make_move('h7', 'h6'))  # Black pawn moves 1 space
        self.assertFalse(game.make_move('d3', 'd8'))  # Queen attempts to move through Pawn
        self.assertTrue(game.make_move('d3', 'd6'))  # Queen moves vertically
        self.assertTrue(game.make_move('f8', 'd6'))  # Black bishop takes white queen
        self.assertEqual(game.get_game_state(), 'BLACK_WON')  # Black wins

    def test_king_move(self):
        game = ChessVar()
        self.assertFalse(game.make_move('e1', 'd2')) # King can't move through pawns
        self.assertTrue(game.make_move('d2', 'd3')) # Pawn moves out of the way
        self.assertTrue(game.make_move('e7', 'e6')) # Black pawn moves 1 space
        self.assertFalse(game.make_move('e1', 'c3'))  # King tries to move more than 1 space
        self.assertTrue(game.make_move('e1', 'd2')) # King moves diagonally
        self.assertTrue(game.make_move('e6', 'e5'))  # Black pawn moves 1 space
        self.assertTrue(game.make_move('d2', 'c3')) # King moves diagonally
        self.assertTrue(game.make_move('e5', 'e4'))  # Black pawn moves 1 space
        self.assertTrue(game.make_move('c3', 'c4')) # King moves vertically
        self.assertTrue(game.make_move('h7', 'h6'))  # Black pawn moves 1 space
        self.assertTrue(game.make_move('c4', 'd4'))  # King moves horizontally
        self.assertTrue(game.make_move('h6', 'h5'))  # Black pawn moves 1 space
        self.assertTrue(game.make_move('d4', 'e4')) # King moves horizontally and takes pawn

if __name__ == '__main__':
    unittest.main()
