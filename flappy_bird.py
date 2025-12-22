"""
NEAT Flappy Bird AI Implementation
==================================

This implementation uses NEAT (NeuroEvolution of Augmenting Topologies) to train
AI agents to play Flappy Bird. The neural networks evolve over generations to
learn optimal timing and decision-making strategies.

Key Features:
- Normalized neural network inputs for better learning
- Optimized fitness function with proper reward/penalty system
- Visual training to watch birds learn in real-time
- Robust error handling and resource management
"""

import pygame
import random
import os
import neat
import time

# Initialize pygame
pygame.init()
pygame.font.init()

# Game constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

# Load game assets with error handling
try:
    BIRD_IMGS = [
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
        pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
    ]
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
    BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
    BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
    STAT_FONT = pygame.font.SysFont("comicsans", 50)
except pygame.error as e:
    print(f"Error loading game assets: {e}")
    print("Make sure the 'imgs' folder contains: bird1.png, bird2.png, bird3.png, pipe.png, base.png, bg.png")
    exit(1)

# Global settings - Visual training mode only
current_generation = 0
SHOW_DEBUG_LINES = True  # Set to False to hide neural network input visualization


class Bird:
    """
    Bird class representing the player/AI agent.
    Handles physics, animation, and collision detection.
    """
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25 
    ROTATION_VELOCITY = 20 
    ANIMATION_TIME = 5 

    def __init__(self, x, y):
        """Initialize bird at given position."""
        self.x = x
        self.y = y
        self.tilt = 0 
        self.tick_count = 0
        self.velocity = 0
        self.height = y
        self.img_count = 0 
        self.img = self.IMGS[0] 

    def jump(self):
        """Make the bird jump (negative velocity = upward movement)."""
        self.velocity = -10.5
        self.tick_count = 0 
        self.height = self.y

    def move(self):
        """Update bird position based on physics."""
        self.tick_count += 1 
        
        # Physics calculation: velocity + gravity acceleration
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count**2

        # Terminal velocity (max fall speed)
        if displacement >= 16:
            displacement = 16
        # Reduce upward movement slightly for balance
        if displacement < 0:
            displacement -= 2
        
        self.y = self.y + displacement

        # Handle bird rotation based on movement direction
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, win):
        """Draw the bird with animation and rotation."""
        self.img_count += 1
        
        # Cycle through bird animation frames
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        # Special case for steep dive
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # Rotate and draw the bird
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        """Get collision mask for pixel-perfect collision detection."""
        return pygame.mask.from_surface(self.img)


class Pipe:
    """
    Pipe class representing obstacles in the game.
    Handles movement, collision detection, and gap positioning.
    """
    GAP = 200  # Gap size between top and bottom pipes
    VEL = 5    # Horizontal movement speed

    def __init__(self, x):
        """Initialize pipe at given x position with random gap height."""
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height()

    def set_height(self):
        """Set random height for the pipe gap."""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP 
    
    def move(self):
        """Move pipe horizontally across the screen."""
        self.x -= self.VEL

    def draw(self, win):
        """Draw both top and bottom pipe segments."""
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        """Check if bird collides with this pipe using pixel-perfect detection."""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        # Calculate offset positions for collision detection
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Check for overlap with either pipe segment
        top_overlap = bird_mask.overlap(top_mask, top_offset)
        bottom_overlap = bird_mask.overlap(bottom_mask, bottom_offset)

        return top_overlap or bottom_overlap


class Base:
    """
    Base class representing the scrolling ground.
    Creates illusion of continuous movement.
    """
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        """Initialize base at given y position."""
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        """Move base segments to create scrolling effect."""
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        
        # Reset positions when segments move off screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    
    def draw(self, win):
        """Draw both base segments."""
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_debug_lines(win, bird, pipes, pipe_ind):
    """
    Draw red debug lines showing neural network inputs for a bird.
    """
    if not SHOW_DEBUG_LINES or not pipes or pipe_ind >= len(pipes):
        return
        
    # Colors for different input lines
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    
    current_pipe = pipes[pipe_ind]
    
    # Input 1: Bird Y position - horizontal line across screen
    pygame.draw.line(win, RED, (0, bird.y), (WINDOW_WIDTH, bird.y), 2)
    
    # Input 2: Distance to pipe gap center
    pipe_center_y = current_pipe.height + current_pipe.GAP / 2
    pygame.draw.line(win, ORANGE, (bird.x, bird.y), (bird.x, pipe_center_y), 3)
    
    # Input 3: Bird velocity - vertical line showing velocity direction
    velocity_end_y = bird.y + (bird.velocity * 10)  # Scale for visibility
    if bird.velocity < 0:  # Going up
        pygame.draw.line(win, YELLOW, (bird.x - 20, bird.y), (bird.x - 20, velocity_end_y), 3)
    else:  # Going down
        pygame.draw.line(win, YELLOW, (bird.x - 20, bird.y), (bird.x - 20, velocity_end_y), 3)
    
    # Input 4: Horizontal distance to pipe
    pygame.draw.line(win, GREEN, (bird.x, bird.y), (current_pipe.x, bird.y), 2)
    
    # Draw pipe gap boundaries for reference
    pygame.draw.line(win, (100, 100, 255), (current_pipe.x, current_pipe.height), 
                     (current_pipe.x + current_pipe.PIPE_TOP.get_width(), current_pipe.height), 2)
    pygame.draw.line(win, (100, 100, 255), (current_pipe.x, current_pipe.height + current_pipe.GAP), 
                     (current_pipe.x + current_pipe.PIPE_TOP.get_width(), current_pipe.height + current_pipe.GAP), 2)


def draw_window(win, birds, pipes, base, score, generation=0, pipe_ind=0):
    """
    Render the complete game window with all elements and debug visualization.
    """
    # Draw background
    win.blit(BG_IMG, (0, 0))

    # Draw pipes
    for pipe in pipes:
        pipe.draw(win)

    # Draw debug lines for each bird (only show for first few birds to avoid clutter)
    if SHOW_DEBUG_LINES and pipes:
        for i, bird in enumerate(birds[:5]):  # Show debug lines for first 5 birds only
            draw_debug_lines(win, bird, pipes, pipe_ind)

    # Draw score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WINDOW_WIDTH - text.get_width() - 10, 10))
    
    # Draw generation and bird count
    gen_text = STAT_FONT.render("Gen: " + str(generation), 1, (255, 255, 255))
    win.blit(gen_text, (10, 10))
    
    bird_text = STAT_FONT.render("Birds: " + str(len(birds)), 1, (255, 255, 255))
    win.blit(bird_text, (10, 60))
    
    # Debug info
    if SHOW_DEBUG_LINES:
        debug_text = pygame.font.Font(None, 24).render("Debug Lines: Red=Y pos, Orange=Gap dist, Yellow=Velocity, Green=Pipe dist", 1, (255, 255, 255))
        win.blit(debug_text, (10, 110))

    # Draw base and birds
    base.draw(win)
    for bird in birds:
        bird.draw(win)
        
    pygame.display.update()


def main(genomes, config):
    """
    Main training function called by NEAT for each generation.
    Handles the complete game simulation and fitness evaluation.
    """
    global current_generation
    current_generation += 1
    
    # Initialize neural networks and birds for each genome
    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 300))  # Start birds higher up
        g.fitness = 0
        ge.append(g)
        
    # Initialize game objects
    base = Base(730)
    pipes = [Pipe(600)]
    
    # Initialize display
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("NEAT Flappy Bird AI - Watch the Birds Learn!")
    clock = pygame.time.Clock()
    score = 0

    # Main game loop
    run = True
    while run and len(birds) > 0:
        clock.tick(30)  # 30 FPS for smooth visual learning
        
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:  # Press 'D' to toggle debug lines
                    global SHOW_DEBUG_LINES
                    SHOW_DEBUG_LINES = not SHOW_DEBUG_LINES
                    print(f"Debug lines: {'ON' if SHOW_DEBUG_LINES else 'OFF'}")

        # Determine which pipe to focus on for AI input
        pipe_ind = 0
        if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
            pipe_ind = 1
            
        # Update each bird and get AI decision
        for x, bird in enumerate(birds):
            bird.move()
            
            # Fitness rewards for survival and good positioning
            ge[x].fitness += 0.1  # Base survival reward
            
            # Bonus for staying near middle (avoid ground/ceiling)
            middle_y = WINDOW_HEIGHT / 2
            distance_from_middle = abs(bird.y - middle_y)
            if distance_from_middle < 100:
                ge[x].fitness += 0.05
            
            # Small bonus for forward progress
            ge[x].fitness += 0.02

            # Prepare normalized inputs for neural network
            bird_y_norm = bird.y / WINDOW_HEIGHT
            pipe_center = pipes[pipe_ind].height + pipes[pipe_ind].GAP / 2
            distance_to_center = (bird.y - pipe_center) / (WINDOW_HEIGHT / 2)
            velocity_norm = bird.velocity / 20.0
            horizontal_distance = (pipes[pipe_ind].x - bird.x) / WINDOW_WIDTH
            
            # Get AI decision
            output = nets[x].activate((bird_y_norm, distance_to_center, velocity_norm, horizontal_distance))
            
            # Jump if output exceeds threshold
            if output[0] > 0.3:
                bird.jump()

        # Handle pipe collision and passing
        add_pipe = False
        removed = []
        birds_to_remove = []

        for pipe in pipes:
            pipe_passed_by_any_bird = False
            
            for x, bird in enumerate(birds):
                # Check collision
                if pipe.collide(bird):
                    ge[x].fitness -= 5  # Collision penalty
                    birds_to_remove.append(x)

                # Check if bird passed pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe_passed_by_any_bird = True
            
            # Mark pipe as passed and trigger new pipe generation
            if pipe_passed_by_any_bird and not pipe.passed:
                    pipe.passed = True
                    add_pipe = True
                
            # Mark pipes for removal when off screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                removed.append(pipe)

        # Remove collided birds
        for x in reversed(birds_to_remove):
            birds.pop(x)
            nets.pop(x)
            ge.pop(x)

        # Move all pipes
        for pipe in pipes:
            pipe.move()
        
        # Add new pipe and reward all surviving birds
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 15  # Big reward for passing pipe
            pipes.append(Pipe(600))

        # Remove off-screen pipes
        for r in removed:
            pipes.remove(r) 

        # Check for boundary collisions (ground/ceiling)
        boundary_removals = []
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                ge[x].fitness -= 10  # Boundary collision penalty
                boundary_removals.append(x)

        # Remove birds that hit boundaries
        for x in reversed(boundary_removals):
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        # Update base and render
        base.move()
        draw_window(win, birds, pipes, base, score, current_generation, pipe_ind)


def run(config_path):
    """
    Initialize and run the NEAT evolution process.
    """
    # Load NEAT configuration
    config = neat.config.Config(
        neat.DefaultGenome, 
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet, 
        neat.DefaultStagnation, 
        config_path
    )
    
    # Create population and add reporters
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    try:
        # Run evolution for 50 generations
        winner = p.run(main, 50)
        print(f"\nTraining completed! Best genome: {winner}")
    finally:
        # Clean up pygame resources
        if pygame.get_init():
            pygame.quit()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)