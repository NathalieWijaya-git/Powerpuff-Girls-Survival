import pygame
import time
import random
import os
pygame.font.init()
pygame.mixer.init()

# Set up initial screen
WIDTH, HEIGHT = 1000, 620
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Powerpuff Girls Survival")

# Load background image
BG = pygame.image.load("bg.png")
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

# Load start music
START_MUSIC = "Powerpuff Girls BG Audio.MP3"

# Load game music
PLAY_MUSIC = "Powerpuff Girls - Mojo Jojo.mp3"

# Load lose music
LOSE_MUSIC = "Powerpuff Girls - Wafoo.mp3"

# Load character image
CHARACTER1_IMAGE = pygame.image.load("Blossom.webp")
CHARACTER2_IMAGE = pygame.image.load("Bubbles.webp")
CHARACTER3_IMAGE = pygame.image.load("Buttercup.webp")

# High score file
SCORE_FILE = "high_score.txt"

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100
PLAYER_VEL = 5

# Scale the image to the new size
CHARACTER1_IMAGE = pygame.transform.smoothscale(CHARACTER1_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
CHARACTER2_IMAGE = pygame.transform.smoothscale(CHARACTER2_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
CHARACTER3_IMAGE = pygame.transform.smoothscale(CHARACTER3_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Font
FONT = pygame.font.SysFont("arial", 30)
FONT.set_bold(True)

# Fire settings
FIRE_WIDTH, FIRE_HEIGHT = 10, 20
FIRE_VEL = 3

# Character positions
CHARACTER1_RECT = CHARACTER1_IMAGE.get_rect(center=(WIDTH // 4, HEIGHT // 2))
CHARACTER2_RECT = CHARACTER2_IMAGE.get_rect(center=(WIDTH // 2, HEIGHT // 2))
CHARACTER3_RECT = CHARACTER3_IMAGE.get_rect(center=(3 * WIDTH // 4, HEIGHT // 2))

# Play music function
def play_music(file_path, loops=-1, start=0.0):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(loops, start)

# Draw function
def draw(player, elapsed_time, fire2):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "purple")
    WIN.blit(time_text, (10, 10))

    WIN.blit(player['image'], (player['rect'].x, player['rect'].y))

    for fire in fire2:
        pygame.draw.rect(WIN, "orange", fire)

    pygame.display.update()

# Character selection function
def character_selection():
    CS_BG = pygame.image.load("Character Selection BG.jpg")
    CS_BG = pygame.transform.scale(CS_BG, (WIDTH, HEIGHT))

    play_music(START_MUSIC)

    CHARACTER1_RECT = CHARACTER1_IMAGE.get_rect(center=(WIDTH // 4, HEIGHT // 2))
    CHARACTER2_RECT = CHARACTER2_IMAGE.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    CHARACTER3_RECT = CHARACTER3_IMAGE.get_rect(center=(3 * WIDTH // 4, HEIGHT // 2))

    selected_character = None
    run = True

    while run:
        WIN.blit(CS_BG, (0,0))

        # Display character options
        WIN.blit(CHARACTER1_IMAGE, CHARACTER1_RECT)
        WIN.blit(CHARACTER2_IMAGE, CHARACTER2_RECT)
        WIN.blit(CHARACTER3_IMAGE, CHARACTER3_RECT)

        # Display instructions
        text = FONT.render("Click on a character to choose!", 1, "white")
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if CHARACTER1_RECT.collidepoint(event.pos):
                    selected_character = {'image': CHARACTER1_IMAGE, 'rect': pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)}
                    run = False
                elif CHARACTER2_RECT.collidepoint(event.pos):
                    selected_character = {'image': CHARACTER2_IMAGE, 'rect': pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)}
                    run = False
                elif CHARACTER3_RECT.collidepoint(event.pos):
                    selected_character = {'image': CHARACTER3_IMAGE, 'rect': pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)}
                    run = False

        pygame.display.update()

    return selected_character

# High score function
def save_high_score(score):
    """Save the high score to a file."""
    with open(SCORE_FILE, "w") as file:
        file.write(str(score))

def load_high_score():
    """Load the high score from a file."""
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            return float(file.read())
    return 0.0

# Main function
def main():
    # Character selected
    player = character_selection()

    run = True
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    fire_add_increment = 2000
    fire_count = 0
    fire2 = []
    hit = False

    play_music(PLAY_MUSIC)

    # Load high score
    high_score = load_high_score()

    while run:
        fire_count += clock.tick(80)
        elapsed_time = time.time() - start_time

        if fire_count > fire_add_increment:
            for _ in range(3):
                fire_x = random.randint(0, WIDTH - FIRE_WIDTH)
                fire = pygame.Rect(fire_x, -FIRE_HEIGHT, FIRE_WIDTH, FIRE_HEIGHT)
                fire2.append(fire)

            fire_add_increment = max(200, fire_add_increment - 50)
            fire_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player['rect'].x - PLAYER_VEL >= 0:
            player['rect'].x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player['rect'].x + PLAYER_VEL + player['rect'].width <= WIDTH:
            player['rect'].x += PLAYER_VEL

        for fire in fire2[:]:
            fire.y += FIRE_VEL
            if fire.y > HEIGHT:
                fire2.remove(fire)
            elif fire.y + fire.height >= player['rect'].y and fire.colliderect(player['rect']):
                fire2.remove(fire)
                hit = True
                break

        if hit:
            play_music(LOSE_MUSIC)
            score = round(elapsed_time, 2)
            if score > high_score:
                save_high_score(score)
                high_score = score

            pygame.time.delay(500)
            WIN.fill("black")
            lost_text = FONT.render("You Lost :(", 1, "purple")
            current_score_text = FONT.render(f"Score: {round(elapsed_time, 2)}s", True, "purple")
            high_score_text = FONT.render(f"High Score: {high_score}s", 1, "purple")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2 - 50))
            WIN.blit(current_score_text, (WIDTH/2 - current_score_text.get_width()/2, HEIGHT/2 - current_score_text.get_height()/2))
            WIN.blit(high_score_text, (WIDTH/2 - high_score_text.get_width()/2, HEIGHT/2 - high_score_text.get_height()/2 + 50))
            pygame.display.update()
            
            pygame.display.update()

            # Wait for the user to close the game
            wait = True
            while wait:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        wait = False

            break

        draw(player, elapsed_time, fire2)
    
    pygame.quit()

if __name__ == "__main__":
    main()
