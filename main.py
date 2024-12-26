import pygame
import sys
import random
from menu import main_menu

WIDTH, HEIGHT = 800, 850 
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

White = (255, 235, 205)
Black = (0, 0, 0)
DarkBrown = (139, 69, 19)
Blue = (0, 0, 255)
Gray = (128, 128, 128)
Brown = (210, 180, 135)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")

pygame.font.init()
FONT = pygame.font.SysFont('arial', 32)
BUTTON_FONT = pygame.font.SysFont('arial', 24) 

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def draw(self, screen):
        radius = SQUARE_SIZE // 3
        pygame.draw.circle(screen, self.color, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), radius)
        if self.king:
            pygame.draw.circle(screen, Gray, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), radius // 2)

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.turn = White  # white goes first
        self.pieces_captured_player = 0  # counter yang udah dimakan buat User
        self.pieces_captured_ai = 0      # counter yang udah dimakan buat AI
        self.create_board()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, DarkBrown))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, White))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw_squares(self):
        for row in range(ROWS):
            for col in range(COLS):
                # Change the color of the squares
                if (row + col) % 2 == 0:
                    color = (169, 169, 169)  # Light gray for light squares
                else:
                    color = (105, 105, 105)  # Dark gray for dark squares
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

            jump_row, jump_col = row + direction, col + dcol
            if 0 <= jump_row < ROWS and 0 <= jump_col < COLS:
                if self.board[row][col] != 0 and self.board[row][col].color != piece.color and self.board[jump_row][jump_col] == 0:
                    moves[(jump_row, jump_col)] = (row, col)
        return moves

    def remove(self, pieces):
        for piece in pieces:
            if piece.color == White:
                self.pieces_captured_ai += 1
            elif piece.color == DarkBrown:
                self.pieces_captured_player += 1
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
            captured_piece = self.valid_moves[(row, col)]
            if captured_piece:
                self.board.remove([self.board.board[captured_piece[0]][captured_piece[1]]])

            self.change_turn()
            return True
        return False

    def change_turn(self):
        self.valid_moves = {}
        self.board.turn = White if self.board.turn == DarkBrown else DarkBrown

    def update(self):
        self.board.draw()

        # blank hitam
        pygame.draw.rect(screen, Black, (0, HEIGHT - 50, WIDTH, 50))
        player_text = FONT.render(f"You: {self.board.pieces_captured_player}", True, White)
        ai_text = FONT.render(f"Opponent: {self.board.pieces_captured_ai}", True, White)
        screen.blit(player_text, (40, HEIGHT - 45))
        screen.blit(ai_text, (WIDTH - 200, HEIGHT - 45))

        button_text = BUTTON_FONT.render("Back to Main Menu", True, White)
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 40, 200, 30)
        pygame.draw.rect(screen, Gray, button_rect)
        screen.blit(button_text, (WIDTH // 2 - 80, HEIGHT - 40))

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
            captured_piece = valid_moves[best_move]
            if captured_piece:
                self.board.remove([self.board.board[captured_piece[0]][captured_piece[1]]])
            self.change_turn()

def main():
    clock = pygame.time.Clock()
    game = Game()
    main_menu(game)  # show menu dulu

    while True:
        clock.tick(60)

        # AI melakukan langkah jika gilirannya
        if game.board.turn == DarkBrown:
            game.ai_move()

        # Periksa apakah ada pemenang
        winner = game.board.winner()
        if winner:
            win_text = "You Win!" if winner == White else "Opponent Wins!"
            text = FONT.render(win_text, True, Blue)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # Check if "Back to Main Menu" button is clicked
                if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and HEIGHT - 40 <= y <= HEIGHT - 10:
                    main_menu(game)

                # Handle game board selection
                if game.board.turn == White:
                    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                    game.select(row, col)

        # Update game state and display
        game.update()
        pygame.display.update()

if __name__ == "__main__":
    main()
