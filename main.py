import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
GRID_SIZE = 4  # 4x4 grid (16 cards)
CARD_SIZE = SCREEN_WIDTH // GRID_SIZE
MARGIN = 5

# Colors
BACKGROUND_COLOR = (50, 168, 82)
CARD_COLOR = (245, 245, 245)
HIGHLIGHT_COLOR = (255, 255, 153)
TEXT_COLOR = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Card Game")

# Load font
font = pygame.font.Font(None, 48)

# Initialize cards and game state
cards = list(range(GRID_SIZE ** 2 // 2)) * 2
random.shuffle(cards)
revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
first_card = None  # Stores the first card clicked for matching
matches_found = 0

# Utility functions
def draw_cards():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * CARD_SIZE + MARGIN, row * CARD_SIZE + MARGIN
            card_rect = pygame.Rect(x, y, CARD_SIZE - 2 * MARGIN, CARD_SIZE - 2 * MARGIN)
            
            # Check if card should be revealed
            if revealed[row][col]:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, card_rect)
                text_surface = font.render(str(cards[row * GRID_SIZE + col]), True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=card_rect.center)
                screen.blit(text_surface, text_rect)
            else:
                pygame.draw.rect(screen, CARD_COLOR, card_rect)

def get_card_at_pos(pos):
    x, y = pos
    row, col = y // CARD_SIZE, x // CARD_SIZE
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        return row, col
    return None

# Main game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    draw_cards()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            card_pos = get_card_at_pos(pos)
            
            if card_pos and not revealed[card_pos[0]][card_pos[1]]:
                row, col = card_pos
                revealed[row][col] = True
                
                if first_card is None:
                    first_card = (row, col)
                else:
                    # Check for match
                    first_row, first_col = first_card
                    if cards[first_row * GRID_SIZE + first_col] == cards[row * GRID_SIZE + col]:
                        matches_found += 1
                        if matches_found == GRID_SIZE ** 2 // 2:
                            print("You matched all pairs! Game over.")
                            pygame.time.wait(2000)
                            pygame.quit()
                            sys.exit()
                    else:
                        pygame.display.flip()
                        pygame.time.wait(1000)
                        revealed[first_row][first_col] = False
                        revealed[row][col] = False
                    first_card = None
