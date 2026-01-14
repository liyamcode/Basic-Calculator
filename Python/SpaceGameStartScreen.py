import pygame
import random

pygame.init()

# ------------------ SETUP ------------------
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Menu")

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# ------------------ STAR ------------------
class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        # Start stars anywhere on the screen
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.base_speed = random.uniform(2, 6)  # depth illusion
        self.speed = self.base_speed

    def update(self, launching=False):
        # During launch, increase speed temporarily
        if launching:
            self.speed = self.base_speed * 1.5
        else:
            self.speed = self.base_speed

        self.y += self.speed

        if self.y > HEIGHT:
            self.reset()
            self.y = 0  # start at top when looping

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)


# ------------------ SPACESHIP ------------------
class Ship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 90
        self.speed = 0

    def update(self):
        self.y -= self.speed

    def draw(self, surface):
        # Main body
        pygame.draw.polygon(
            surface,
            (200, 200, 255),
            [
                (self.x, self.y - 40),      # nose
                (self.x - 18, self.y + 20), # left body
                (self.x + 18, self.y + 20), # right body
            ]
        )

        # Wings
        pygame.draw.polygon(
            surface,
            (140, 140, 220),
            [
                (self.x - 18, self.y + 5),
                (self.x - 40, self.y + 25),
                (self.x - 18, self.y + 25),
            ]
        )
        pygame.draw.polygon(
            surface,
            (140, 140, 220),
            [
                (self.x + 18, self.y + 5),
                (self.x + 40, self.y + 25),
                (self.x + 18, self.y + 25),
            ]
        )

        # Cockpit
        pygame.draw.ellipse(
            surface,
            (100, 200, 255),
            (self.x - 6, self.y - 10, 12, 18)
        )

        # Engine glow (only when moving)
        if self.speed > 0:
            glow_len = min(20, self.speed * 2)
            pygame.draw.rect(
                surface,
                (120, 180, 255),
                (self.x - 6, self.y + 22, 12, glow_len)
            )


# ------------------ BUTTON ------------------
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont(None, 50)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (40, 40, 60), self.rect, border_radius=12)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=12)
        txt = self.font.render(self.text, True, WHITE)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


# ------------------ MAIN ------------------
stars = [Star() for _ in range(400)]
ship = Ship()
play_button = Button(WIDTH // 2 - 110, HEIGHT // 2 - 40, 220, 80, "PLAY")

running = True
launching = False
fade_alpha = 0

while running:
    screen.fill(BLACK)

    # Stars
    for star in stars:
        star.update(launching)
        star.draw(screen)

    # Ship
    ship.update()
    ship.draw(screen)

    # Fade overlay and launch acceleration
    if launching:
        ship.speed += 0.6
        fade_alpha = min(255, fade_alpha + 5)

        fade = pygame.Surface((WIDTH, HEIGHT))
        fade.set_alpha(fade_alpha)
        fade.fill(BLACK)
        screen.blit(fade, (0, 0))

        if fade_alpha >= 255:
            running = False  # transition to game here

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not launching and play_button.clicked(event):
            launching = True

    if not launching:
        play_button.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
