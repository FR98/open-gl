# Los shaders de OpenGL se escriben en un lenguaje de progra llamado GLSL

vertex_shader = """
#version 460

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 cColor;

out vec3 miColor;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(position.x, position.y, position.z, 1.0);
    miColor = cColor;
}
"""


fragment_shader ="""
#version 460

layout(location = 0) out vec4 fragColor;

in vec3 miColor;

void main()
{
    fragColor = vec4(miColor, 1);
}
"""