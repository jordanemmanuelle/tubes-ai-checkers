import pygame
import sys

def draw_text(screen, text, font, color, x, y):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def draw_button(screen, color, text, font, text_color, x, y, width, height, hover=False):
    if hover:
        border_color = (255, 215, 0)  # Gold border for hover effect
        button_color = (255, 223, 186)  # Light gold color for hover
    else:
        border_color = (139, 69, 19)  # DarkBrown border
        button_color = color  # Default button color

    # Draw button with gradient
    pygame.draw.rect(screen, button_color, (x + 5, y + 5, width - 10, height - 10))  # Inner rectangle
    pygame.draw.rect(screen, border_color, (x, y, width, height), 5)  # Outer rectangle

    # Draw the text in the center of the button
    draw_text(screen, text, font, text_color, x + (width // 2 - font.size(text)[0] // 2), y + (height // 2 - font.get_height() // 2))

def main_menu(game):
    menu_font = pygame.font.SysFont('arial', 60)
    button_font = pygame.font.SysFont('arial', 36)
    BACKGROUND_COLOR = (47, 79, 79)  # DarkSlateGray for background
    BUTTON_COLOR = (210, 180, 140)  # Tan for buttons
    TEXT_COLOR = (255, 255, 255)  # White for text

    screen = pygame.display.get_surface()

    button_width = 300
    button_height = 80
    button_x = (screen.get_width() - button_width) // 2
    button_y = 250
    button_spacing = 100

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text(screen, "Checkers Game", menu_font, TEXT_COLOR, 200, 100)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, difficulty in enumerate(["Easy", "Medium", "Hard", "Extreme"]):
            y_pos = button_y + i * button_spacing
            rect = pygame.Rect(button_x, y_pos, button_width, button_height)
            hover = rect.collidepoint(mouse_x, mouse_y)
            draw_button(screen, BUTTON_COLOR, difficulty, button_font, TEXT_COLOR, button_x, y_pos, button_width, button_height, hover)

        quit_button_y = button_y + 4 * button_spacing
        draw_button(screen, BUTTON_COLOR, "Press ESC to Quit", button_font, TEXT_COLOR, button_x, quit_button_y, button_width, button_height)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, difficulty in enumerate(["easy", "medium", "hard", "extreme"]):
                    rect = pygame.Rect(button_x, button_y + i * button_spacing, button_width, button_height)
                    if rect.collidepoint(mouse_x, mouse_y):
                        game.difficulty = difficulty
                        return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
