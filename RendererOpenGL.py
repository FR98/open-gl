import pygame
from pygame.locals import *
from gl import Renderer
import shaders


deltaTime = 0.0
pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)
screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)
r = Renderer(screen)
r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
r.createObjects()
cubeX, cubeZ = 0, 0

isPlaying = True
while isPlaying:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        cubeX -= 2 * deltaTime
    if keys[pygame.K_d]:
        cubeX += 2 * deltaTime
    if keys[pygame.K_w]:
        cubeZ -= 2 * deltaTime
    if keys[pygame.K_s]:
        cubeZ += 2 * deltaTime

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                r.filledMode()
            elif ev.key == pygame.K_2:
                r.wireframeMode
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False

    r.translateCube(cubeX, 0, cubeZ)
    r.render()
    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000
pygame.quit()
