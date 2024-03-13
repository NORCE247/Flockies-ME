import pygame
from boids import *
import random
from objekt import *

#Scrren setnings
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("FlockiesME")

#Clock
clock = pygame.time.Clock()
FPS = 120

#Boids
antall_boids = 120
boids = [Boids(500 + int(200 * math.cos(math.radians(i))), 400 + int(200 * math.sin(math.radians(i)))) for i in range(0, 360, (360 // antall_boids))]

boida = Boids(500, 400)

#OBJEKT & ATTACKER
objekt = Objekt(500, 400)


attackers = [Attacker(200, 300) for _ in range(1)]


#Stimulation
run = True
while run:
    clock.tick(FPS)

#Background
    screen.fill((0, 51, 102))

#Boids
    for boid in boids:
        boid.move()
        boid.draw(screen)
        boid.__cohesion__(boids)
        boid.__separat__(boids)
        boid.__align__(boids)
        boid._move_from_objekt_(objekt)
        for attacker in attackers:
            boid._move_from_attacker_(attacker)
    
    boids[0].zone(boids, screen)
    
    
#Objekt        
    
    objekt._draw_(screen)

    

#Attacker
    for attacker in attackers:
        attacker._draw_(screen)
        attacker.move()
        attacker.__separat__(attackers)
        attacker.__cohesion__(boids)
        attacker._move_from_objekt_(objekt)
        attacker.__align__(attackers)
    

#Event handler for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()