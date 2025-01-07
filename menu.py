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

    pygame.draw.rect(screen, button_color, (x + 5, y + 5, width - 10, height - 10))  # inner rectangle
    pygame.draw.rect(screen, border_color, (x, y, width, height), 5)  # outer rectangle
    draw_text(screen, text, font, text_color, x + (width // 2 - font.size(text)[0] // 2), y + (height // 2 - font.get_height() // 2))

def show_instructions(screen):
    font = pygame.font.SysFont('arial', 30)
    BACKGROUND_COLOR = (47, 79, 79)
    TEXT_COLOR = (255, 255, 255)

    instructions = [
        "Welcome to Checkers Game!",
        "Instructions:",
        "",
        "1. Each player takes turns to move their pieces.",
        "2. Capture opponent pieces by jumping over them.",
        "3. Win by capturing all opponent pieces or blocking their moves.",
        "",
        "",
        "Press ESC to go back."
    ]

    while True:
        screen.fill(BACKGROUND_COLOR)
        for i, line in enumerate(instructions):
            draw_text(screen, line, font, TEXT_COLOR, 50, 50 + i * 40)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

def main_menu(game):
    menu_font = pygame.font.SysFont('arial', 60)
    button_font = pygame.font.SysFont('arial', 36)
    BACKGROUND_COLOR = (47, 79, 79)
    BUTTON_COLOR = (210, 180, 140)
    TEXT_COLOR = (255, 255, 255)

    screen = pygame.display.get_surface()

    button_width = 300
    button_height = 80
    button_x = (screen.get_width() - button_width) // 2
    button_y = 215
    button_spacing = 100

    options = ["Play Easy", "Play Medium", "Play Hard", "Play Extreme", "Instructions", "Quit"]

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text(screen, "Checkers Game", menu_font, TEXT_COLOR, 200, 80)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        for i, option in enumerate(options):
            y_pos = button_y + i * button_spacing
            rect = pygame.Rect(button_x, y_pos, button_width, button_height)
            hover = rect.collidepoint(mouse_x, mouse_y)
            draw_button(screen, BUTTON_COLOR, option, button_font, TEXT_COLOR, button_x, y_pos, button_width, button_height, hover)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, option in enumerate(options):
                    rect = pygame.Rect(button_x, button_y + i * button_spacing, button_width, button_height)
                    if rect.collidepoint(mouse_x, mouse_y):
                        if option.startswith("Play"):
                            game.difficulty = option.split()[-1].lower()
                            return
                        elif option == "Instructions":
                            show_instructions(screen)
                        elif option == "Quit":
                            pygame.quit()
                            sys.exit()