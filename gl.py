import glm
import math
import pygame
import numpy as np
from obj import Obj
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader


class Model(object):
    def __init__(self, filename, texture_name, scale):
        self.model = Obj(filename)
        self.createVertBuffer()
        self.texture_surface = pygame.image.load(texture_name)
        self.texture_data = pygame.image.tostring(self.texture_surface, "RGB", 1)
        self.texture = glGenTextures(1)

        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = scale

    def getMatrix(self, camera_pos, projection, camera_rot):
        i = glm.mat4(1)
        translate = glm.translate(i, glm.vec3(0, 0, 0))
        pitch = glm.rotate(i, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        yaw = glm.rotate(i, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        roll = glm.rotate(i, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, self.scale)
        view = glm.lookAt(camera_pos, self.position, glm.vec3(0, 1, 0))
        return translate * rotate * scale

    def createVertBuffer(self):
        buffer = []

        for face in self.model.faces:
            for i in range(3):
                buffer.append(self.model.vertices[face[i][0] - 1][0])
                buffer.append(self.model.vertices[face[i][0] - 1][1])
                buffer.append(self.model.vertices[face[i][0] - 1][2])
                buffer.append(1)

                buffer.append(self.model.normals[face[i][2] - 1][0])
                buffer.append(self.model.normals[face[i][2] - 1][1])
                buffer.append(self.model.normals[face[i][2] - 1][2])
                buffer.append(0)

                buffer.append(self.model.texcoords[face[i][1] - 1][0])
                buffer.append(self.model.texcoords[face[i][1] - 1][1])
        
        self.vertBuffer = np.array(buffer, dtype=np.float32)

    def renderInScene(self):
        VBO = glGenBuffers(1)
        VAO = glGenVertexArrays(1)

        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertBuffer.nbytes, self.vertBuffer, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(4 * 4))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 4 * 10, ctypes.c_void_p(4 * 8))
        glEnableVertexAttribArray(2)

        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.texture_surface.get_width(), self.texture_surface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, self.texture_data)
        glGenerateMipmap(GL_TEXTURE_2D)

        glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces) * 3)


class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        self.modelList = []
        self.activeModelIndex = 0
        self.camPosition = glm.vec3(0, 0, 0)
        self.camRotation = glm.vec3(0, 0, 0)
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)
        self.pointLight = glm.vec4(0, 0, 0, 0)
        self.angle = 90
        self.viewMatrix = self.getViewMatrix()

        self.__roll = 0
        self.__pitch = 0
        self.__yaw = 0

    def getViewMatrix(self):
        i = glm.mat4(1)
        camTranslate = glm.translate(i, self.camPosition)
        camPitch = glm.rotate(i, glm.radians(self.camRotation.x), glm.vec3(1, 0, 0))
        camYaw = glm.rotate(i, glm.radians(self.camRotation.y), glm.vec3(0, 1, 0))
        camRoll = glm.rotate(i, glm.radians(self.camRotation.z), glm.vec3(0, 0, 1))
        camRotate = camPitch * camYaw * camRoll

        return glm.inverse(camTranslate * camRotate)

    def cameraView(self):
        r = (self.camPosition.x ** 2 + self.camPosition.z ** 2) ** 0.5
        self.camPosition.x = r * math.cos(self.angle * math.pi / 180)
        self.camPosition.z = r * math.sin(self.angle * math.pi / 180)
        self.viewMatrix = glm.lookAt(self.camPosition, self.modelList[self.activeModelIndex].position, glm.vec3(0, 1, 0))

    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def translateCube(self, x, y, z):
        self.cubePos = glm.vec3(x, y, z)

    def roll(self):
        self.__roll += 5

    def pitch(self):
        self.__pitch += 5

    def yaw(self):
        self.__yaw += 5

    def setShaders(self, vertexShader, fragShader):
        if vertexShader is not None or fragShader is not None:
            self.active_shader = compileProgram(
                compileShader(vertexShader, GL_VERTEX_SHADER),
                compileShader(fragShader, GL_FRAGMENT_SHADER)
            )
        else:
            self.active_shader = None
        glUseProgram(self.active_shader)

    def createObjects(self):
        self.VBO = glGenBuffers(1)      # Vertex Buffer Object
        self.EBO = glGenBuffers(1)      # Element Buffer Object
        self.VAO = glGenVertexArrays(1) # Vertex Array Object

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, rectVerts.nbytes, rectVerts, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, rectIndices.nbytes, rectIndices, GL_STATIC_DRAW)
        # Atributo de posicion de vertices
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        # Atributo de color de vertices
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 4 * 6, ctypes.c_void_p(4 * 3))
        glEnableVertexAttribArray(1)

    def render(self):
        glClearColor(0.25, 0.5, 0.5, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"), 1, GL_FALSE, glm.value_ptr( self.viewMatrix ))
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projection"), 1, GL_FALSE, glm.value_ptr( self.projection ))
            glUniform4f(glGetUniformLocation(self.active_shader, "light"), self.pointLight.x, self.pointLight.y, self.pointLight.z, self.pointLight.w)
            glUniform4f(glGetUniformLocation(self.active_shader, "color"), 1, 1, 1, 1)
        
        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"), 1, GL_FALSE, glm.value_ptr(self.modelList[self.activeModelIndex].getMatrix(self.camPosition, self.projection, self.camRotation)))
            self.modelList[self.activeModelIndex].renderInScene()
