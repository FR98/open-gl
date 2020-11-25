import glm
import pygame
import shaders
from pygame.locals import *
from gl import Renderer, Model


deltaTime = 0.0
pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)

screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)
r = Renderer(screen)
r.camPosition.z = 500
r.camPosition.x = 5

r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
model1 = Model("assets/dilophosaurus/dilophosaurus.obj", "assets/dilophosaurus/skin.bmp", glm.vec3(1, 1, 1))
r.modelList.append(model1)
# model2 = Model("assets/Biplane/OBJ/HiPoly/Biplane.obj", "assets/Biplane/Textures/SidesMap_01.bmp", glm.vec3(0.25, 0.25, 0.25))
# r.modelList.append(model2)
# model3 = Model("assets/Face/model.obj", "assets/Face/model.bmp", glm.vec3(0.25, 0.25, 0.25))
# r.modelList.append(model3)

isPlaying = True
while isPlaying:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        r.camPosition.x += 1 * deltaTime
    if keys[pygame.K_d]:
        r.camPosition.x -= 1 * deltaTime
    if keys[pygame.K_w]:
        r.camPosition.z -= 1 * deltaTime
    if keys[pygame.K_s]:
        r.camPosition.z += 1 * deltaTime

    if keys[pygame.K_r]:
        r.roll()
    if keys[pygame.K_p]:
        r.pitch()
    if keys[pygame.K_y]:
        r.yaw()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isPlaying = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                r.filledMode()
            elif ev.key == pygame.K_2:
                r.wireframeMode()
            elif ev.key == pygame.K_SPACE:
                r.activeModelIndex = (r.activeModelIndex + 1) % len(r.modelList)
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False

    r.render()
    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000
pygame.quit()
