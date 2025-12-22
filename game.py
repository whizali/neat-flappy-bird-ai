"""
Human-Playable Flappy Bird Game
===============================

A complete Flappy Bird implementation designed for human players with:
- Intuitive controls (UP arrow or SPACE to jump)
- Professional UI/UX with menus and animations
- Score tracking and high score system
- Smooth gameplay with proper physics
- Game states: Menu → Playing → Game Over → Restart
"""

import pygame
import random
import os
import json
import math
import time

# Initialize pygame
pygame.init()
pygame.font.init()
pygame.mixer.init()

# Game constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3

# Load game assets
try:
    BIRD_IMGS = [
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
    ]
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
    BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
    BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
except pygame.error:
    print("Warning: Could not load image assets. Using colored rectangles instead.")
    # Create placeholder colored rectangles
    BIRD_IMGS = [pygame.Surface((50, 35)) for _ in range(3)]
    for i, surf in enumerate(BIRD_IMGS):
        surf.fill((255, 255 - i*50, 0))  # Orange to red gradient
    
    PIPE_IMG = pygame.Surface((80, 500))
    PIPE_IMG.fill(GREEN)
    
    BASE_IMG = pygame.Surface((WINDOW_WIDTH, 100))
    BASE_IMG.fill((139, 69, 19))  # Brown
    
    BG_IMG = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    BG_IMG.fill((135, 206, 235))  # Sky blue

# Fonts
TITLE_FONT = pygame.font.Font(None, 72)
LARGE_FONT = pygame.font.Font(None, 48)
MEDIUM_FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)

# High score file
HIGH_SCORE_FILE = "high_score.json"


class Bird:
    """Enhanced Bird class for human gameplay with smooth animations."""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.8
        self.jump_strength = -12
        self.max_velocity = 10
        self.rotation = 0
        self.img_count = 0
        self.img = BIRD_IMGS[0]
        
    def jump(self):
        """Make the bird jump with smooth physics."""
        self.velocity = self.jump_strength
        
    def update(self):
        """Update bird physics and animation."""
        # Apply gravity
        self.velocity += self.gravity
        if self.velocity > self.max_velocity:
            self.velocity = self.max_velocity
            
        # Update position
        self.y += self.velocity
        
        # Update rotation based on velocity
        if self.velocity < 0:
            self.rotation = min(25, -self.velocity * 2)
        else:
            self.rotation = max(-90, -self.velocity * 3)
            
        # Update animation
        self.img_count += 1
        if self.img_count >= 15:  # Slower animation for smoother look
            self.img_count = 0
            
        frame = (self.img_count // 5) % 3
        self.img = BIRD_IMGS[frame]
        
    def draw(self, screen):
        """Draw the bird with rotation."""
        rotated_img = pygame.transform.rotate(self.img, self.rotation)
        rect = rotated_img.get_rect(center=(self.x, self.y))
        screen.blit(rotated_img, rect)
        
    def get_rect(self):
        """Get collision rectangle."""
        return pygame.Rect(self.x - 25, self.y - 17, 50, 35)


class Pipe:
    """Enhanced Pipe class with better collision detection."""
    
    def __init__(self, x):
        self.x = x
        self.gap_size = 200
        self.width = 80
        self.speed = 4
        
        # Random gap position
        self.gap_y = random.randint(150, WINDOW_HEIGHT - 250)
        self.top_height = self.gap_y
        self.bottom_y = self.gap_y + self.gap_size
        self.bottom_height = WINDOW_HEIGHT - self.bottom_y
        
        self.passed = False
        
    def update(self):
        """Move pipe to the left."""
        self.x -= self.speed
        
    def draw(self, screen):
        """Draw both pipe segments."""
        # Top pipe
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        screen.blit(pygame.transform.scale(PIPE_IMG, (self.width, self.top_height)), top_rect)
        
        # Bottom pipe
        bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, self.bottom_height)
        flipped_pipe = pygame.transform.flip(PIPE_IMG, False, True)
        screen.blit(pygame.transform.scale(flipped_pipe, (self.width, self.bottom_height)), bottom_rect)
        
    def collides_with(self, bird):
        """Check collision with bird."""
        bird_rect = bird.get_rect()
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_pipe_rect = pygame.Rect(self.x, self.bottom_y, self.width, self.bottom_height)
        
        return bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect)
        
    def is_off_screen(self):
        """Check if pipe is completely off screen."""
        return self.x + self.width < 0


class Game:
    """Main game class handling all game logic and UI."""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird - Human Player")
        self.clock = pygame.time.Clock()
        
        self.state = MENU
        self.bird = Bird(150, WINDOW_HEIGHT // 2)
        self.pipes = []
        self.base_x = 0
        self.score = 0
        self.high_score = self.load_high_score()
        
        # Animation variables
        self.menu_bounce = 0
        self.flash_timer = 0
        
        # Game timing
        self.pipe_timer = 0
        self.pipe_frequency = 90  # frames between pipes
        
    def load_high_score(self):
        """Load high score from file."""
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
            
    def save_high_score(self):
        """Save high score to file."""
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except Exception as e:
            print(f"Could not save high score: {e}")
            
    def reset_game(self):
        """Reset game to initial state."""
        self.bird = Bird(150, WINDOW_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.pipe_timer = 0
        self.state = PLAYING
        
    def handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if self.state == MENU:
                    if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_RETURN]:
                        self.reset_game()
                        
                elif self.state == PLAYING:
                    if event.key in [pygame.K_SPACE, pygame.K_UP]:
                        self.bird.jump()
                    elif event.key == pygame.K_p:
                        self.state = PAUSED
                        
                elif self.state == PAUSED:
                    if event.key == pygame.K_p:
                        self.state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = MENU
                        
                elif self.state == GAME_OVER:
                    if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_RETURN]:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = MENU
                        
        return True
        
    def update_game(self):
        """Update game logic."""
        if self.state == PLAYING:
            # Update bird
            self.bird.update()
            
            # Check ground/ceiling collision
            if self.bird.y <= 0 or self.bird.y >= WINDOW_HEIGHT - 100:
                self.game_over()
                return
                
            # Update pipes
            self.pipe_timer += 1
            if self.pipe_timer >= self.pipe_frequency:
                self.pipes.append(Pipe(WINDOW_WIDTH))
                self.pipe_timer = 0
                
            # Update existing pipes
            for pipe in self.pipes[:]:
                pipe.update()
                
                # Check collision
                if pipe.collides_with(self.bird):
                    self.game_over()
                    return
                    
                # Check scoring
                if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                    
                # Remove off-screen pipes
                if pipe.is_off_screen():
                    self.pipes.remove(pipe)
                    
            # Update base animation
            self.base_x -= 4
            if self.base_x <= -WINDOW_WIDTH:
                self.base_x = 0
                
        elif self.state == MENU:
            # Menu animations
            self.menu_bounce += 0.1
            
    def game_over(self):
        """Handle game over logic."""
        self.state = GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            
    def draw_background(self):
        """Draw scrolling background."""
        self.screen.blit(BG_IMG, (0, 0))
        
    def draw_base(self):
        """Draw scrolling base."""
        self.screen.blit(BASE_IMG, (self.base_x, WINDOW_HEIGHT - 100))
        self.screen.blit(BASE_IMG, (self.base_x + WINDOW_WIDTH, WINDOW_HEIGHT - 100))
        
    def draw_text_centered(self, text, font, color, y):
        """Draw centered text."""
        text_surface = font.render(text, True, color)
        x = (WINDOW_WIDTH - text_surface.get_width()) // 2
        self.screen.blit(text_surface, (x, y))
        
    def draw_text_with_shadow(self, text, font, color, shadow_color, x, y, offset=2):
        """Draw text with shadow effect."""
        shadow = font.render(text, True, shadow_color)
        text_surface = font.render(text, True, color)
        self.screen.blit(shadow, (x + offset, y + offset))
        self.screen.blit(text_surface, (x, y))
        
    def draw_menu(self):
        """Draw main menu."""
        self.draw_background()
        self.draw_base()
        
        # Animated title
        bounce_offset = math.sin(self.menu_bounce) * 10
        title_y = 200 + bounce_offset
        self.draw_text_with_shadow("FLAPPY BIRD", TITLE_FONT, YELLOW, DARK_GRAY, 
                                 (WINDOW_WIDTH - TITLE_FONT.size("FLAPPY BIRD")[0]) // 2, title_y)
        
        # Instructions
        self.draw_text_centered("Press SPACE or ↑ to Start", MEDIUM_FONT, WHITE, 350)
        self.draw_text_centered("Use SPACE or UP to Fly", SMALL_FONT, GRAY, 400)
        self.draw_text_centered("Press P to Pause", SMALL_FONT, GRAY, 430)
        
        # High score
        if self.high_score > 0:
            self.draw_text_centered(f"High Score: {self.high_score}", MEDIUM_FONT, GREEN, 500)
            
        # Animated bird
        demo_bird = Bird(300, 300 + bounce_offset)
        demo_bird.img_count = int(time.time() * 10) % 15
        demo_bird.draw(self.screen)
        
    def draw_playing(self):
        """Draw playing state."""
        self.draw_background()
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
            
        self.draw_base()
        self.bird.draw(self.screen)
        
        # Draw score
        self.draw_text_with_shadow(str(self.score), LARGE_FONT, WHITE, BLACK, 
                                 WINDOW_WIDTH // 2 - 20, 50)
        
    def draw_paused(self):
        """Draw paused state."""
        self.draw_playing()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        self.draw_text_centered("PAUSED", LARGE_FONT, WHITE, 300)
        self.draw_text_centered("Press P to Resume", MEDIUM_FONT, GRAY, 350)
        self.draw_text_centered("Press ESC for Menu", MEDIUM_FONT, GRAY, 380)
        
    def draw_game_over(self):
        """Draw game over state."""
        self.draw_playing()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Game over panel
        panel_rect = pygame.Rect(100, 250, 400, 300)
        pygame.draw.rect(self.screen, WHITE, panel_rect)
        pygame.draw.rect(self.screen, BLACK, panel_rect, 3)
        
        # Game over text
        self.draw_text_centered("GAME OVER", LARGE_FONT, RED, 280)
        
        # Score display
        self.draw_text_centered(f"Score: {self.score}", MEDIUM_FONT, BLACK, 330)
        
        # High score
        if self.score == self.high_score and self.score > 0:
            self.draw_text_centered("NEW HIGH SCORE!", MEDIUM_FONT, GREEN, 360)
        else:
            self.draw_text_centered(f"Best: {self.high_score}", MEDIUM_FONT, GRAY, 360)
            
        # Instructions
        self.draw_text_centered("Press SPACE to Play Again", SMALL_FONT, BLUE, 450)
        self.draw_text_centered("Press ESC for Menu", SMALL_FONT, GRAY, 480)
        
    def draw(self):
        """Main drawing function."""
        if self.state == MENU:
            self.draw_menu()
        elif self.state == PLAYING:
            self.draw_playing()
        elif self.state == PAUSED:
            self.draw_paused()
        elif self.state == GAME_OVER:
            self.draw_game_over()
            
        pygame.display.flip()
        
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            running = self.handle_events()
            self.update_game()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()


if __name__ == "__main__":
    print("Starting Human-Playable Flappy Bird!")
    print("Controls:")
    print("  SPACE or UP Arrow: Jump/Fly")
    print("  P: Pause/Resume")
    print("  ESC: Return to menu")
    print("\nGood luck!")
    
    game = Game()
    game.run()
