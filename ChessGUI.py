# Author: Nolan Reichkitzer
# GitHub username: nolanreichkitzer
# Date: 12/12/2023
# Description: CS 162 - Portfolio Project
#
#              This module contains the graphical user interface for the chess game defined in ChessVar.
#              Pygame is employed to render the graphics of the game. The rules of this game are different
#              from the normal rules. In this version, the winner is the first player to capture all of an
#              opponent's pieces of one type. Also, castling, en passant, and pawn promotion are not allowed.

from ChessVar import ChessVar
import pygame

# Global Variables
WIDTH = HEIGHT = 512
DIMENSION = 10  # 8x8 chessboard with empty squares around it
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations
IMAGES = {}
COLUMN_LETTER = {1 : 'a', 2 : 'b', 3 : 'c', 4 : 'd', 5 : 'e', 6 : 'f', 7 : 'g', 8 : 'h'}
FLIP_ROW = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

def load_images():
    """Initializes global dictionary of images"""
    pieces = ['WP', 'WN', 'WB', 'WR', 'WQ', 'WK', 'BP', 'BN', 'BB', 'BR', 'BQ', 'BK']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Images for each piece can now be accessed by accessing the IMAGES dictionary

def main():

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    pygame.display.set_caption('Chess Variant')
    game = ChessVar()
    load_images() # Load images once

    square_selected = () # Keeps track of last mouse click (row, column)
    player_clicks = [] # Keeps track of player clicks [(row, col), (row, col)]

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() # (x, y) location of the mouse
                column = location[0]//SQ_SIZE
                row = FLIP_ROW[location[1]//SQ_SIZE]
                square_selected = (column, row)
                player_clicks.append(square_selected)

                # Determine if that was the user's second click and attempt to make proposed move
                if len(player_clicks) == 2:
                    game.make_move(COLUMN_LETTER[player_clicks[0][0]] + str(player_clicks[0][1]), \
                                   COLUMN_LETTER[player_clicks[1][0]] + str(player_clicks[1][1]))
                    player_clicks = []

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    # Forfeit the game when f is pressed
                    game.forfeit()


        draw_game_state(screen, game)

        if game.get_game_state() != 'UNFINISHED':

            if game.get_game_state() == 'BLACK_WON':
                display_text(screen, 'Black wins!')
            if game.get_game_state() == 'WHITE_WON':
                display_text(screen, 'White wins!')

        clock.tick(MAX_FPS)
        pygame.display.flip()

def draw_game_state(screen, game):
    """ Responsible for displaying game graphics"""
    draw_chessboard(screen)
    draw_pieces(screen, game.get_board())

def draw_chessboard(screen):
    """Draw squares on the board"""
    # Top left square is always the lighter color
    colors = [pygame.Color('white'), pygame.Color('gray')]

    for row in range(DIMENSION):
        for column in range(DIMENSION):
            pygame.draw.rect(screen, colors[0], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    for row in range(1, DIMENSION - 1):
        for column in range(1, DIMENSION - 1):
            color = colors[(row + column) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Draw borders around the board
    pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(0, 0, WIDTH, HEIGHT), 4)
    pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(SQ_SIZE, SQ_SIZE, WIDTH - SQ_SIZE*2, HEIGHT - SQ_SIZE*2), 4)

    # Display column/row text
    font = pygame.font.Font(None, 36)
    for number, letter in COLUMN_LETTER.items():
        text = font.render(letter, 1, (10, 10, 10))
        screen.blit(text, pygame.Rect(number*SQ_SIZE + SQ_SIZE/3, SQ_SIZE/2, SQ_SIZE, SQ_SIZE))
    for number, letter in COLUMN_LETTER.items():
        text = font.render(letter, 1, (10, 10, 10))
        screen.blit(text, pygame.Rect(number*SQ_SIZE + SQ_SIZE/3, (9.1)*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    for number in COLUMN_LETTER.keys():
        text = font.render(str(number), 1, (10, 10, 10))
        screen.blit(text, pygame.Rect(SQ_SIZE/2, number*SQ_SIZE + SQ_SIZE/3, SQ_SIZE, SQ_SIZE))
    for number in COLUMN_LETTER.keys():
        text = font.render(str(number), 1, (10, 10, 10))
        screen.blit(text, pygame.Rect((9.25)*SQ_SIZE, number*SQ_SIZE + SQ_SIZE/3, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, chessboard):
    """Draw pieces on top of squares"""

    for row in range(1, DIMENSION - 1):
        for column in range(1, DIMENSION - 1):
            piece = chessboard[COLUMN_LETTER[column] + str(row)]
            if piece:
                screen.blit(IMAGES[chessboard[COLUMN_LETTER[column] + str(row)].get_name()], pygame.Rect(column* \
                        SQ_SIZE, FLIP_ROW[row]*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def display_text(screen, text):
    font = pygame.font.Font(None, 36)
    text_object = font.render(text, 0, pygame.Color('grey'))
    text_location = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, pygame.Color('black'))
    screen.blit(text_object, text_location.move(1, 1))

if __name__ == '__main__':
    main()

