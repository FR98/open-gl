from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm
import numpy as np


                     # VERTS           COLOR
rectVerts = np.array([ 0.5, 0.5, 0.5,  1,0,0, 
                       0.5,-0.5, 0.5,  0,1,0, 
                      -0.5,-0.5, 0.5,  0,0,1, 
                      -0.5, 0.5, 0.5,  1,1,0,
                       0.5, 0.5,-0.5,  1,0,1,
                       0.5,-0.5,-0.5,  0,1,1,
                      -0.5,-0.5,-0.5,  1,1,1,
                      -0.5, 0.5,-0.5,  0,0,0 ], dtype=np.float32)

rectIndices = np.array([ #front
                         0, 1, 3,
                         1, 2, 3,
                         #left
                         4, 5, 0,
                         5, 1, 0,
                         #back
                         7, 6, 4,
                         6, 5, 4,
                         #right
                         3, 2, 7,
                         2, 6, 7,
                         #top
                         1, 5, 2,
                         5, 6, 2,
                         #bottom
                         4, 0, 7,
                         0, 3, 7], dtype=np.uint32)




class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)

        # Perspective Projection Matrix
        self.projection = glm.perspective(glm.radians(60), self.width / self.height, 0.1, 1000)

        self.cubePos = glm.vec3(0,0,0)


    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def translateCube(self, x, y, z):
        self.cubePos = glm.vec3(x,y,z)


    def setShaders(self, vertexShader, fragShader):

        if vertexShader is not None or fragShader is not None:
            self.active_shader = compileProgram(compileShader(vertexShader, GL_VERTEX_SHADER),
                                                compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

        glUseProgram(self.active_shader)

    def createObjects(self):

        self.VBO = glGenBuffers(1) #Vertex Buffer Object
        self.EBO = glGenBuffers(1) #Element Buffer Object
        self.VAO = glGenVertexArrays(1) #Vertex Array Object

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
        glClearColor(0.2, 0.2, 0.2, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )

        i = glm.mat4(1)
        # Model/Object matrix: translate * rotate * scale
        translate = glm.translate(i, self.cubePos)
        pitch = glm.rotate(i, glm.radians( 0 ), glm.vec3(1,0,0))
        yaw   = glm.rotate(i, glm.radians( 0 ), glm.vec3(0,1,0))
        roll  = glm.rotate(i, glm.radians( 0 ), glm.vec3(0,0,1))
        rotate = pitch * yaw * roll
        scale = glm.scale(i, glm.vec3(1,1,1))
        model = translate * rotate * scale
        
        # View Matrix
        # glm.lookAt( eye, center, up)
        camTranslate = glm.translate(i, glm.vec3( 0, 0, 3))
        camPitch = glm.rotate(i, glm.radians( 0 ), glm.vec3(1,0,0))
        camYaw   = glm.rotate(i, glm.radians( 0 ), glm.vec3(0,1,0))
        camRoll  = glm.rotate(i, glm.radians( 0 ), glm.vec3(0,0,1))
        camRotate = camPitch * camYaw * camRoll
        view = glm.inverse( camTranslate * camRotate )


        if self.active_shader:

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "model"),
                               1, GL_FALSE, glm.value_ptr( model ))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "view"),
                               1, GL_FALSE, glm.value_ptr( view ))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projection"),
                               1, GL_FALSE, glm.value_ptr( self.projection ))


        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
