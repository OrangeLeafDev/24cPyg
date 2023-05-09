import pygame, random, math

def generate(amount, shake, grav1, grav2, dir1, dir2, mul1, mul2, radiDiv, color, pos=(960, 528)):
    particles = []
    for _ in range(amount):
        angle = random.uniform(dir1, dir2)
        multi = random.uniform(mul1, mul2)
        particles.append([pygame.Vector2(pos[0]+random.randint(-shake,shake), pos[1]+random.randint(-shake,shake)), pygame.Vector2(math.sin(angle*math.pi/180)*multi,math.cos(angle*math.pi/180)*multi), random.uniform(grav1, grav2), radiDiv, color])
    return particles
def process(particles, scr, fadetime=1, deltatime=1):
    for particle in particles:
        pygame.draw.circle(scr,particle[4], particle[0], math.fabs(particle[2])*100/particle[3])
        particle[0] += particle[1] * fadetime * deltatime
        particle[1] += pygame.Vector2(0,particle[2] * fadetime *  deltatime) 
        particle[3] += fadetime * deltatime
        if math.fabs(particle[2])*100/particle[3] < 0.2:
            del particles[particles.index(particle)]
    return particles
# sourcery skip: merge-nested-ifs
pygame.init()
if __name__ == "__main__":
    screen = pygame.display.set_mode((960, 528))

    mainParticles = []

    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    mainParticles += generate(0, 45, 2, 3)
                    print(len(mainParticles))
        mainParticles = process(mainParticles, screen)
        print(len(mainParticles))
        pygame.display.update()
        pygame.time.Clock().tick(120)