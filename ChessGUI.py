# Author: Nolan Reichkitzer
# GitHub username: nolanreichkitzer
# Date: 12/13/2023
# Description: This module contains the graphical user interface for the chess game defined in ChessVar.
#              Pygame is employed to render the graphics of the game. The rules of this game are different
#              from the normal rules. In this version, the winner is the first player to capture all of an
#              opponent's pieces of one type. Also, castling, en passant, and pawn promotion are not allowed.

from ChessVar import ChessVar
import pygame

# Global Variables
DIMENSION = 8  # 8x8 chessboard
SQ_SIZE = 512 // DIMENSION
WIDTH = SQ_SIZE * 14
HEIGHT = SQ_SIZE * 10
MAX_FPS = 15  # for animations
IMAGES = {}
COLUMN_LETTER = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}
FLIP_ROW = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]


def load_images():
    """Initializes global dictionary of images"""
    pieces = ['WP', 'WN', 'WB', 'WR', 'WQ', 'WK', 'BP', 'BN', 'BB', 'BR', 'BQ', 'BK']

    # Populate IMAGES dictionary with chess piece images from file
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():

    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    pygame.display.set_caption('Chess Variant')
    game = ChessVar()
    load_images()  # Load images once (labor-intensive)

    player_selection = ()  # Keeps track of current selection
    player_clicks = []  # Keeps track of player clicks [(row, col), (row, col)]

    # Game event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Get (x, y) location of the mouse
                location = pygame.mouse.get_pos()

                # Transform (x, y) to square location
                column = location[0] / SQ_SIZE
                row = location[1] / SQ_SIZE

                # Check if click is on Forfeit button
                if 10.5 <= column <= 12.5 and 4.5 <= row <= 5.5:
                    game.forfeit()
                    break

                # Check if click is on Reset button
                elif 10.5 <= column <= 12.5 and 6 <= row <= 7:
                    pygame.quit()
                    main()

                # Check if click is on chessboard
                column = location[0]//SQ_SIZE
                row = FLIP_ROW[location[1]//SQ_SIZE]
                player_selection = (column, row)

                if 1 <= column <= 8:
                    player_clicks.append(player_selection)

                    # Determine if that was the user's second click and attempt to make proposed move
                    if len(player_clicks) == 2:

                        # If piece is on ending square, store the name of the removed piece for animation purposes
                        if game.get_board()[COLUMN_LETTER[player_selection[0]] + str(player_selection[1])]:
                            removed_piece = game.get_board()[COLUMN_LETTER[player_selection[0]] +
                                                             str(player_selection[1])].get_name()
                        else:
                            removed_piece = None

                        # Store the name of the moved piece for animation purposes
                        moved_piece = game.get_board()[COLUMN_LETTER[player_clicks[0][0]] +
                                                       str(player_clicks[0][1])].get_name()

                        # Make proposed move and animate the move if move is legal
                        if game.make_move(COLUMN_LETTER[player_clicks[0][0]] + str(player_clicks[0][1]),
                                          COLUMN_LETTER[player_clicks[1][0]] + str(player_clicks[1][1])) is True:

                            animate_move(player_clicks, screen, game.get_board(), clock, moved_piece, removed_piece)

                        # Clear clicks/selection
                        player_clicks = []
                        player_selection = ()

                    # Clear selection and clicks if player tries to move opponent's piece
                    elif game.get_board()[COLUMN_LETTER[player_selection[0]] + str(player_selection[1])] and \
                            game.get_board()[COLUMN_LETTER[player_selection[0]] + str(player_selection[1])].get_color()\
                            != game.get_player_turn():

                        player_clicks = []
                        player_selection = ()

                    # Clear selection and clicks if player chooses an empty space
                    elif not game.get_board()[COLUMN_LETTER[player_selection[0]] + str(player_selection[1])]:
                        player_clicks = []
                        player_selection = ()

        # Draw the game screen
        draw_game_state(screen, game, player_selection)

        # Display a message if the game is finished
        if game.get_game_state() != 'UNFINISHED':

            if game.get_game_state() == 'BLACK_WON':
                display_text(screen, 'Black wins!')
            if game.get_game_state() == 'WHITE_WON':
                display_text(screen, 'White wins!')

        clock.tick(MAX_FPS)
        pygame.display.flip()


def draw_game_state(screen, game, player_selection):
    """ Responsible for displaying game graphics"""
    draw_chessboard(screen)
    draw_pieces(screen, game.get_board())
    print_turn(screen, game)
    highlight_selection(screen, player_selection, game.get_board())


def draw_chessboard(screen):
    """Draw squares on the board"""

    # Establish colors and font
    colors = [pygame.Color('white'), pygame.Color('gray')]
    font = pygame.font.Font(None, 36)

    # Draw white squares over and around the board
    for row in range(DIMENSION + 2):
        for column in range(DIMENSION + 2):
            pygame.draw.rect(screen, colors[0], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Top left square is always the lighter color. Draw white and grey board squares
    for row in range(1, DIMENSION + 1):
        for column in range(1, DIMENSION + 1):
            color = colors[(row + column) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Draw borders around the board
    pygame.draw.rect(screen, pygame.Color('gray'),
                     pygame.Rect(SQ_SIZE/4 - 4, SQ_SIZE/4 - 7, HEIGHT - SQ_SIZE/2 + 4, HEIGHT - SQ_SIZE/2 + 4), 5)
    pygame.draw.rect(screen, pygame.Color('black'),
                     pygame.Rect(SQ_SIZE/4 - 2, SQ_SIZE/4 - 5, HEIGHT - SQ_SIZE/2, HEIGHT - SQ_SIZE/2), 3)
    pygame.draw.rect(screen, pygame.Color('gray'), pygame.Rect(SQ_SIZE - 5, SQ_SIZE - 5, HEIGHT - SQ_SIZE*2 + 10, HEIGHT
                                                               - SQ_SIZE*2 + 10), 5)
    pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(SQ_SIZE - 3, SQ_SIZE - 3, HEIGHT - SQ_SIZE * 2 + 6,
                                                                HEIGHT - SQ_SIZE * 2 + 6), 3)

    # Draw forfeit and reset buttons
    pygame.draw.rect(screen, pygame.Color('light gray'),
                     pygame.Rect(SQ_SIZE * 10.5 - 2, SQ_SIZE * 4.5 - 2, SQ_SIZE * 2 + 4, SQ_SIZE + 4))
    pygame.draw.rect(screen, pygame.Color('black'),
                     pygame.Rect(SQ_SIZE * 10.5, SQ_SIZE * 4.5, SQ_SIZE * 2, SQ_SIZE), 3)
    text = font.render('Forfeit', 1, 'black')
    screen.blit(text, pygame.Rect(SQ_SIZE * 10.9, SQ_SIZE * 4.8, SQ_SIZE * 2, SQ_SIZE))

    pygame.draw.rect(screen, pygame.Color('light gray'),
                     pygame.Rect(SQ_SIZE * 10.5 - 2, SQ_SIZE * 6 - 2, SQ_SIZE * 2 + 4, SQ_SIZE + 4))
    pygame.draw.rect(screen, pygame.Color('black'),
                     pygame.Rect(SQ_SIZE * 10.5, SQ_SIZE * 6, SQ_SIZE * 2, SQ_SIZE), 3)
    text = font.render('Reset', 1, 'black')
    screen.blit(text, pygame.Rect(SQ_SIZE * 11, SQ_SIZE * 6.3, SQ_SIZE * 2, SQ_SIZE))

    # Display column/row text
    for number, letter in COLUMN_LETTER.items():
        text = font.render(letter, 1, 'black')
        screen.blit(text, pygame.Rect(number*SQ_SIZE + SQ_SIZE/3, SQ_SIZE/2, SQ_SIZE, SQ_SIZE))
    for number, letter in COLUMN_LETTER.items():
        text = font.render(letter, 1, 'black')
        screen.blit(text, pygame.Rect(number*SQ_SIZE + SQ_SIZE/3, 9.1*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    for number in range(1, DIMENSION + 1):
        text = font.render(str(number), 1, 'black')
        screen.blit(text, pygame.Rect(SQ_SIZE/2, FLIP_ROW[number]*SQ_SIZE + SQ_SIZE/3, SQ_SIZE, SQ_SIZE))
    for number in range(1, DIMENSION + 1):
        text = font.render(str(number), 1, 'black')
        screen.blit(text, pygame.Rect(9.25*SQ_SIZE, FLIP_ROW[number]*SQ_SIZE + SQ_SIZE/3, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, chessboard):
    """Draw pieces on top of squares"""

    # Access the chessboard in ChessVar and draw the pieces on their squares

    for row in range(1, DIMENSION + 1):
        for column in range(1, DIMENSION + 1):
            piece = chessboard[COLUMN_LETTER[column] + str(row)]
            if piece:
                screen.blit(IMAGES[chessboard[COLUMN_LETTER[column] + str(row)].get_name()], pygame.Rect(column *
                            SQ_SIZE, FLIP_ROW[row]*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def print_turn(screen, game):
    """Prints the current player's turn"""

    # Clear the previous turn
    pygame.draw.rect(screen, pygame.Color('white'),
                     pygame.Rect(SQ_SIZE * 10.5, SQ_SIZE * 3, SQ_SIZE * 2, SQ_SIZE))
    pygame.draw.rect(screen, pygame.Color('black'),
                     pygame.Rect(SQ_SIZE * 10.5, SQ_SIZE * 3, SQ_SIZE * 2, SQ_SIZE), 3)

    # Print current turn
    font = pygame.font.Font(None, 36)
    text = font.render(game.get_player_turn(), 1, 'black')
    screen.blit(text, pygame.Rect(SQ_SIZE * 10.8, SQ_SIZE * 3.3, SQ_SIZE * 2, SQ_SIZE))
    text = font.render('Turn', 1, 'black')
    screen.blit(text, pygame.Rect(SQ_SIZE * 11, SQ_SIZE * 2.6, SQ_SIZE * 2, SQ_SIZE))


def highlight_selection(screen, player_selection, chessboard):
    """Highlights the selected square"""

    # Highlight selected square if a square is currently selected
    if player_selection != ():
        column = player_selection[0]
        row = player_selection[1]
        pygame.draw.rect(screen, pygame.Color('light green'), pygame.Rect(column * SQ_SIZE, FLIP_ROW[row] * SQ_SIZE,
                                                                          SQ_SIZE, SQ_SIZE))

        # After square is highlighted, redraw the piece occupying the square
        piece = chessboard[COLUMN_LETTER[column] + str(row)]
        if piece:
            screen.blit(IMAGES[chessboard[COLUMN_LETTER[column] + str(row)].get_name()], pygame.Rect(column *
                        SQ_SIZE, FLIP_ROW[row] * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def display_text(screen, text):
    """Displays input text to the middle of the chessboard"""

    font = pygame.font.Font(None, 36)
    text_object = font.render(text, 0, pygame.Color('grey'))
    text_location = pygame.Rect(0, 0, WIDTH, HEIGHT).move(HEIGHT/2 - text_object.get_width()/2, HEIGHT/2 -
                                                          text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, pygame.Color('black'))
    screen.blit(text_object, text_location.move(1, 1))


def animate_move(player_clicks, screen, chessboard, clock, moved_piece, removed_piece):
    """Animate the given chess move"""

    colors = [pygame.Color('white'), pygame.Color('gray')]

    # Store starting/ending columns in prettier variables
    start_column = player_clicks[0][0]
    end_column = player_clicks[1][0]

    start_row = player_clicks[0][1]
    end_row = player_clicks[1][1]

    delta_column = end_column - start_column
    delta_row = end_row - start_row

    frames_per_square = 10
    frame_count = (abs(delta_row) + abs(delta_column)) * frames_per_square

    # Draw the animation one frame at a time
    for frame in range(frame_count + 1):
        column, row = (start_column + delta_column*frame/frame_count, FLIP_ROW[start_row] - delta_row*frame/frame_count)
        draw_chessboard(screen)
        draw_pieces(screen, chessboard)

        # Erase piece moved from ending square
        color = colors[(FLIP_ROW[end_row] + end_column) % 2]
        end_square = pygame.Rect(end_column * SQ_SIZE, FLIP_ROW[end_row] * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, end_square)

        # Draw captured piece onto ending square:
        if removed_piece:
            screen.blit(IMAGES[removed_piece], end_square)

        # Draw moving piece
        screen.blit(IMAGES[moved_piece], pygame.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        pygame.display.flip()
        clock.tick(frame_count / 0.5)


if __name__ == '__main__':
    main()
