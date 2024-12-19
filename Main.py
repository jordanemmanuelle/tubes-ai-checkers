import pygame
import sys
from copy import deepcopy
import random

# window
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# colors
White = (255, 235, 205)
Black = (0, 0, 0)
DarkBrown = (139, 69, 19)
Blue = (0, 0, 255)
Gray = (128, 128, 128)
Brown = (210, 180, 135)

# init pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")
FONT = pygame.font.SysFont('arial', 32)

# __ atau 2 under score: buat nandain metode khusus
class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False 

    def make_king(self):
        self.king = True # kalo udah jd king bisa gerak diagonal maju dan mundur

    def draw(self, screen):
        radius = SQUARE_SIZE // 3
        # gambar lingkaran
        pygame.draw.circle(screen, self.color, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), radius)
        if self.king:
            pygame.draw.circle(screen, Gray, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), radius // 2)

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None 
        self.turn = White  # white goes first
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, DarkBrown)) # kasih piece musuh
                    elif row > 4:
                        self.board[row].append(Piece(row, col, White)) # kasih piece kita
                    else:
                        self.board[row].append(0) # else = koooosongggggg
                else:
                    self.board[row].append(0) # kosong

    def draw_squares(self):
        for row in range(ROWS):
            for col in range(COLS):
                color = Brown if (row + col) % 2 == 0 else Black
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw(self):
        self.draw_squares()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = 0
        self.board[row][col] = piece
        piece.row, piece.col = row, col

        if row == 0 and piece.color == White or row == ROWS - 1 and piece.color == DarkBrown:
            piece.make_king()

    def get_valid_moves(self, piece):
        moves = {}
        direction = -1 if piece.color == White else 1
        for dcol in [-1, 1]:
            row, col = piece.row + direction, piece.col + dcol
            if 0 <= row < ROWS and 0 <= col < COLS and self.board[row][col] == 0:
                moves[(row, col)] = None

            # Check for captures
            jump_row, jump_col = row + direction, col + dcol
            if 0 <= jump_row < ROWS and 0 <= jump_col < COLS:
                if self.board[row][col] != 0 and self.board[row][col].color != piece.color and self.board[jump_row][jump_col] == 0:
                    moves[(jump_row, jump_col)] = (row, col)
        return moves

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0

    def winner(self):
        DarkBrown_left = sum(piece.color == DarkBrown for row in self.board for piece in row if piece != 0)
        White_left = sum(piece.color == White for row in self.board for piece in row if piece != 0)
        if DarkBrown_left == 0:
            return White
        elif White_left == 0:
            return DarkBrown
        return None

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

class Game:
    def __init__(self):
        self.board = Board()
        self.selected = None
        self.valid_moves = {}

    def reset(self):
        self.__init__()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.board[row][col]
        if piece != 0 and piece.color == self.board.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def _move(self, row, col):
        piece = self.selected
        if piece and (row, col) in self.valid_moves:
            self.board.move(piece, row, col)
            captuDarkBrown = self.valid_moves[(row, col)]
            if captuDarkBrown:
                self.board.remove([self.board.board[captuDarkBrown[0]][captuDarkBrown[1]]])

            self.change_turn()
            return True
        return False

    def change_turn(self):
        self.valid_moves = {}
        self.board.turn = White if self.board.turn == DarkBrown else DarkBrown

    def update(self):
        self.board.draw()
        if self.selected:
            row, col = self.selected.row, self.selected.col
            pygame.draw.circle(screen, Blue, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
            for move in self.valid_moves:
                pygame.draw.circle(screen, Blue, (move[1] * SQUARE_SIZE + SQUARE_SIZE // 2, move[0] * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def ai_move(self):
        pieces = self.board.get_all_pieces(DarkBrown)
        best_move = None
        for piece in pieces:
            valid_moves = self.board.get_valid_moves(piece)
            if valid_moves:
                best_move = random.choice(list(valid_moves.keys()))
                break

        if best_move:
            self.board.move(piece, best_move[0], best_move[1])
            captuDarkBrown = valid_moves[best_move]
            if captuDarkBrown:
                self.board.remove([self.board.board[captuDarkBrown[0]][captuDarkBrown[1]]])
            self.change_turn()

def main():
    clock = pygame.time.Clock()
    game = Game()

    while True:
        clock.tick(60)
        if game.board.turn == DarkBrown:
            game.ai_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and game.board.turn == White:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                game.select(row, col)

        game.update()
        pygame.display.flip()

if __name__ == "__main__":
    main()
