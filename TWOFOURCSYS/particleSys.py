import pygame
import random
import math
from dataclasses import dataclass
from typing import List

@dataclass
class Particle:
    """Immutable particle data structure for type safety and clarity."""
    position: pygame.Vector2
    velocity: pygame.Vector2
    gravity: float
    radius_divisor: float
    color: tuple

def generate(amount: int, shake: int, grav1: float, grav2: float, dir1: float, dir2: float, mul1: int, mul2: int, radiDiv: float, color: tuple, pos: tuple = (960, 528)) -> List[Particle]:
    """Generate a batch of particles.
    
    Args:
        amount: Number of particles to generate
        shake: Random offset range from center position
        grav1, grav2: Gravity range (min, max)
        dir1, dir2: Direction angle range (degrees)
        mul1, mul2: Velocity multiplier range
        radiDiv: Radius divisor for rendering
        color: RGB color tuple
        pos: Center position (x, y)
    
    Returns:
        List of Particle objects
    """
    particles = []
    for _ in range(amount):
        angle = random.uniform(dir1, dir2)
        multi = random.uniform(mul1, mul2)
        gravity = random.uniform(grav1, grav2)
        
        position = pygame.Vector2(
            pos[0] + random.randint(-shake, shake),
            pos[1] + random.randint(-shake, shake)
        )
        velocity = pygame.Vector2(
            math.sin(angle * math.pi / 180) * multi,
            math.cos(angle * math.pi / 180) * multi
        )
        
        particles.append(Particle(
            position=position,
            velocity=velocity,
            gravity=gravity,
            radius_divisor=radiDiv,
            color=color
        ))
    return particles

def process(particles: List[Particle], scr: pygame.Surface, fadetime: float = 1, deltatime: float = 1) -> List[Particle]:
    """Update and render all particles. SAFE list filtering during iteration.
    
    Args:
        particles: List of particles to process
        scr: Surface to draw particles on
        fadetime: Fade/lifetime multiplier
        deltatime: Delta time for physics
    
    Returns:
        Updated particle list (filtered to remove dead particles)
    """
    alive_particles = []
    
    for particle in particles:
        # Render particle
        radius = abs(particle.gravity) * 100 / particle.radius_divisor
        if radius >= 0.2:  # Only render if visible
            pygame.draw.circle(scr, particle.color, particle.position, radius)
            
            # Update physics
            particle.position += particle.velocity * fadetime * deltatime
            particle.velocity += pygame.Vector2(0, particle.gravity * fadetime * deltatime)
            particle.radius_divisor += fadetime * deltatime
            
            # Keep particle if still visible
            alive_particles.append(particle)
    
    return alive_particles

# Test code
pygame.init()
if __name__ == "__main__":
    screen = pygame.display.set_mode((960, 528))
    clock = pygame.time.Clock()
    mainParticles = []

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    mainParticles += generate(10, 45, 2, 3, 0, 360, 10, 100, 0.5, (0, 255, 255))
                    print(f"Particles: {len(mainParticles)}")
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        mainParticles = process(mainParticles, screen)
        pygame.display.update()
        clock.tick(120)
