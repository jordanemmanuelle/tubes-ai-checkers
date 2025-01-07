import pygame
import sys
import random
from menu import main_menu

# window
WIDTH, HEIGHT = 800, 850
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# warna yang bakal dipake
White = (255, 235, 205)
Black = (0, 0, 0)
DarkBrown = (139, 69, 19)
Blue = (0, 0, 255)
Gray = (128, 128, 128)
Brown = (210, 180, 135)
HighlightColor = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers Game")

pygame.font.init()
FONT = pygame.font.SysFont('arial', 32)
BUTTON_FONT = pygame.font.SysFont('arial', 24)

class Piece:
    def __init__(self, row, col, color): # bikin pieces
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def draw(self, screen):
        radius = SQUARE_SIZE // 3           # size lingkarannya 
        center_x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

        outline_color = tuple(max(0, c - 50) for c in self.color) # piece's outline
        pygame.draw.circle(screen, outline_color, (center_x, center_y), radius + 3)
        pygame.draw.circle(screen, self.color, (center_x, center_y), radius)

        if self.king:
            pygame.draw.circle(screen, Gray, (center_x, center_y), radius // 2)


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.turn = White # white goes first
        self.pieces_captured_player = 0 # counter yang udah dimakan sama kita
        self.pieces_captured_ai = 0 # counter yang udah dimakan sama AI
        self.create_board() 

    def create_board(self):
        for row in range(ROWS):
            self.board.append([]) # nambah baris baru 
            for col in range(COLS):
                if (row + col) % 2 == 1: # buat piece-nya cuma ada di kotak warna gelap
                    if row < 3: # baris 0-2 diisi sama piece lawan
                        self.board[row].append(Piece(row, col, DarkBrown))
                    elif row > 4: # barus 4 -7 diisi sama piece kita
                        self.board[row].append(Piece(row, col, White))
                    else: # baris 3-4 kosong
                        self.board[row].append(0)
                else:
                    self.board[row].append(0) # kotak warna terang tetep kosong

    def draw_squares(self):
        for row in range(ROWS):
            for col in range(COLS):
                # bikin papannya jadi kaya catur
                color = (169, 169, 169) if (row + col) % 2 == 0 else (105, 105, 105)
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw(self):
        self.draw_squares()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def move(self, piece, row, col):
        # mindahin piece ke posisi baru
        self.board[piece.row][piece.col] = 0 # posisi sebelumnya jadi kosong
        self.board[row][col] = piece
        piece.row, piece.col = row, col # update posisi piece

        # jika sudah sampai baris terakhir, piecenya berubah jadi king
        if row == 0 and piece.color == White or row == ROWS - 1 and piece.color == DarkBrown:
            piece.make_king()

    def get_valid_moves(self, piece):
        moves = {} # save gerakan valid
        direction = -1 if piece.color == White else 1 # arah jalan (atas buat kita, bawah buat musuh)
        for dcol in [-1, 1]: # cek gerakan ke kiri (-1) atau ke kanan (1)
            row, col = piece.row + direction, piece.col + dcol # posisi tujuan
            if 0 <= row < ROWS and 0 <= col < COLS and self.board[row][col] == 0:
                moves[(row, col)] = None # add langkah biasa ke daftar gerakan

            # periksa langkah lompat (untuk makan lawan)
            jump_row, jump_col = row + direction, col + dcol
            if 0 <= row < ROWS and 0 <= col < COLS and 0 <= jump_row < ROWS and 0 <= jump_col < COLS:
                if self.board[row][col] != 0 and self.board[row][col].color != piece.color and self.board[jump_row][jump_col] == 0:
                    moves[(jump_row, jump_col)] = (row, col) # add langkah lompat ke daftar gerakan
        return moves

    def remove(self, pieces): # buat kalau piece-nya dimakan
        for piece in pieces:
            if piece.color == White: # kalau warna putih
                self.pieces_captured_ai += 1 # +1 counter yang ditangkap sama lawan (AI)
            elif piece.color == DarkBrown: # kalau warna coklat
                self.pieces_captured_player += 1 # tambahin ke counter kita
            self.board[piece.row][piece.col] = 0 # set posisi piecenya jadi kosong

    def winner(self):

        DarkBrown_left = sum(piece.color == DarkBrown for row in self.board for piece in row if piece != 0)
        White_left = sum(piece.color == White for row in self.board for piece in row if piece != 0)
        if DarkBrown_left == 0: # jika semua piece coklat habis
            return White # kita menang
        elif White_left == 0: # kalau semua piece putih habis
            return DarkBrown # musuh menang
        return None 

    def get_all_pieces(self, color):
        pieces = [] # array untuk menyimpan piece
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color: # kalau elemen bukan 0 dan warnanya sesuai
                    pieces.append(piece) # tambahkan ke array piece
        return pieces


class Game:
    def __init__(self):
        self.board = Board()
        self.selected = None
        self.valid_moves = {}
        self.difficulty = 'easy'  # default difficulty

    def reset(self):
        self.board = Board()
        self.selected = None
        self.valid_moves = {}

    def select(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            if self.selected:
                result = self._move(row, col) # mindahin piece ke posisi baru
                if not result:
                    self.selected = None
                    self.select(row, col)

            piece = self.board.board[row][col]
            if piece != 0 and piece.color == self.board.turn: # pastikan piecenya dari giliran yang seharusnya
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece) # ambil gerakan valid dari piece ini
                return True
        return False

    def _move(self, row, col):
        piece = self.selected # bidak yang dipilih
        if piece and (row, col) in self.valid_moves: # kalau valid
            self.board.move(piece, row, col) # pindahkan piece ke posisi baru 
            captured_piece = self.valid_moves[(row, col)] # ambil piece yang sudah dimakan (kalau ada)
            if captured_piece:
                # hapus piece yang sudah dimakan
                self.board.remove([self.board.board[captured_piece[0]][captured_piece[1]]])

            self.change_turn() # ganti giliran
            return True
        return False

    def change_turn(self):
        self.valid_moves = {} # clear daftar gerakan valid
        self.board.turn = White if self.board.turn == DarkBrown else DarkBrown # ganti giliran

    def update(self):
        self.board.draw()

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
            # beri dot biru untuk opsi langkah
            pygame.draw.circle(screen, Blue, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)
            
            for move in self.valid_moves: # tampilkan dot biru di langkah yang valid
                pygame.draw.circle(screen, Blue, (move[1] * SQUARE_SIZE + SQUARE_SIZE // 2, move[0] * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def ai_move(self): # otak AI
        pieces = self.board.get_all_pieces(DarkBrown) # ambil semua pieces AI (coklat)
        if self.difficulty == 'easy':
            self.random_move(pieces)
        elif self.difficulty == 'medium':
            self.capture_move(pieces)  # AI mencoba menangkap piece jika memungkinkan
        elif self.difficulty == 'hard':
            self.smart_move(pieces)  # AI menggunakan strategi dasar
        elif self.difficulty == 'extreme':
            self.optimal_move(pieces)  # AI menggunakan algoritma canggih

    def random_move(self, pieces):
        while pieces:
            piece = random.choice(pieces)
            valid_moves = self.board.get_valid_moves(piece)
            if valid_moves:
                move = random.choice(list(valid_moves.keys()))
                self.board.move(piece, move[0], move[1])
                captured_piece = valid_moves[move]
                if captured_piece:
                    self.board.remove([self.board.board[captured_piece[0]][captured_piece[1]]])
                self.change_turn()
                return
            pieces.remove(piece)
        self.change_turn()

    def capture_move(self, pieces):
        for piece in pieces:
            valid_moves = self.board.get_valid_moves(piece)
            for move in valid_moves:
                captured_piece = valid_moves[move]
                if captured_piece:
                    self.board.move(piece, move[0], move[1])
                    self.board.remove([self.board.board[captured_piece[0]][captured_piece[1]]])
                    self.change_turn()
                    return
        self.random_move(pieces)

    def smart_move(self, pieces):
        for piece in pieces:
            valid_moves = self.board.get_valid_moves(piece)
            for move in valid_moves:
                captured_piece = valid_moves[move]
                if captured_piece:
                    self.board.move(piece, move[0], move[1])
                    self.board.remove([self.board.board[captured_piece[0]][captured_piece[1]]])
                    self.change_turn()
                    return
        for piece in pieces:
            valid_moves = self.board.get_valid_moves(piece)
            for move in valid_moves:
                if move[0] > piece.row:  # move forward
                    self.board.move(piece, move[0], move[1])
                    self.change_turn()
                    return
        self.random_move(pieces)

    def optimal_move(self, pieces):
        # Implement a more advanced AI strategy here (e.g., minimax with alpha-beta pruning)
        pass


def main():
    clock = pygame.time.Clock() # buat ngatur kecepatan frame
    game = Game() # membuat objek game untuk memulai permainan
    main_menu(game) # tampilkan menu dulu sebelumnya

    while True:
        clock.tick(60) # max 60 FPS

        if game.board.turn == DarkBrown: # jika giliran coklat (AI), gerak otomatis
            game.ai_move() # otak AI

        winner = game.board.winner()
        if winner:
            win_text = "You Win!" if winner == White else "Opponent Wins!"
            text = FONT.render(win_text, True, Blue)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos() # ambil posisi mouse saat diklik
                if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100 and HEIGHT - 40 <= y <= HEIGHT - 10:
                    game.reset()
                    main_menu(game)
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                game.select(row, col)

        game.update()
        pygame.display.update() # update layar dengan recent updates


if __name__ == "__main__":
    main()