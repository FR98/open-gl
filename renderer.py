import glm
import pygame
import shaders
from pygame.locals import *
from gl import Renderer, Model


deltaTime = 0.0
all_shaders = [eval("shaders." + shader_name) for shader_name in dir(shaders) if not shader_name.startswith("__") and shader_name != "vertex_shader"]
actual_shader_index = 0
pygame.init()
clock = pygame.time.Clock()
screenSize = (960, 540)

screen = pygame.display.set_mode(screenSize, DOUBLEBUF | OPENGL)
r = Renderer(screen)
r.camPosition.z = 3
r.pointLight.x = 10

r.setShaders(shaders.vertex_shader, shaders.fragment_shader)
model1 = Model("assets/beriev/BerievA50.obj", "assets/beriev/Beriev_2048.bmp", glm.vec3(0.01, 0.01, 0.01))
r.modelList.append(model1)

model2 = Model("assets/sign/Stool.obj", "assets/Face/model.bmp", glm.vec3(0.025, 0.025, 0.025))
r.modelList.append(model2)

model3 = Model("assets/sign/objSign.obj", "assets/Face/model.bmp", glm.vec3(0.25, 0.25, 0.25))
r.modelList.append(model3)

model3 = Model("assets/f16/F-16D.obj", "assets/f16/Albedo.bmp", glm.vec3(0.25, 0.25, 0.25))
r.modelList.append(model3)

isPlaying = True
while isPlaying:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        r.angle -= 75 * deltaTime
    if keys[pygame.K_d]:
        r.angle += 75 * deltaTime
    if keys[pygame.K_w]:
        r.camPosition.y -= 10 * deltaTime
    if keys[pygame.K_s]:
        r.camPosition.y += 10 * deltaTime

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
            elif ev.key == pygame.K_5:
                actual_shader_index = (actual_shader_index + 1) % len(all_shaders)
                r.setShaders(shaders.vertex_shader, all_shaders[actual_shader_index])
            elif ev.key == pygame.K_ESCAPE:
                isPlaying = False
        elif ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.MOUSEBUTTONUP:
            if ev.button == 4:
                if r.camPosition.z >= 0:
                    r.camPosition.z -= 10 * deltaTime
            if ev.button == 5:
                if r.camPosition.z <= 100:
                    r.camPosition.z += 10 * deltaTime

    r.cameraView()
    r.render()
    pygame.display.flip()
    clock.tick(60)
    deltaTime = clock.get_time() / 1000
pygame.quit()
