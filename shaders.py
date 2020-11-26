# Los shaders de OpenGL se escriben en un lenguaje de progra llamado GLSL

vertex_shader = """
#version 460

layout (location = 0) in vec4 pos;
layout (location = 1) in vec4 normal;
layout (location = 2) in vec2 texcoords;
layout (location = 3) out vec3 miColor;
layout (location = 4) out vec3 v3Position;
layout (location = 5) out vec3 fnormal;
layout (location = 6) out float ftime;
layout (location = 7) out float intensity;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform vec4 color;
uniform vec4 light;

out vec4 vertexColor;
out vec2 vertexTexcoords;

void main()
{
    float intensity = dot(model * normal, normalize(light - pos));

    gl_Position = projection * view * model * pos;
    vertexColor = color * intensity;
    vertexTexcoords = texcoords;
}
"""


fragment_shader = """
#version 460

layout(location = 0) out vec4 diffuseColor;

in vec4 vertexColor;
in vec2 vertexTexcoords;

uniform sampler2D tex;

void main()
{
    diffuseColor = vertexColor * texture(tex, vertexTexcoords);
}
"""


all_shader = """
#version 460

layout(location = 0) out vec4 diffuseColor;

in vec3 miColor;

void main()
{
    diffuseColor = vec4(miColor, 1);
}
"""

a_shader = """
#version 460

layout(location = 0) out vec4 diffuseColor;

in float intensity;
in vec2 vertexTexcoords;
in vec3 v3Position;
uniform sampler2D tex;
uniform vec4 diffuse;
uniform vec4 ambient;

void main()
{
    float bright = floor(mod(v3Position.x*10.0, 2.0)+0.2) + floor(mod(v3Position.y*1.0, 1.0)+0.5) + floor(mod(v3Position.z*0.0, 10.0)+0.5);
    diffuseColor = mod(bright, 6.0) > 0.8 ? vec4(1.0, 0.0, 0.0, 9.0) : vec4(1.0, 3.0, 2.0, 0.5);
}
"""

b_shader = """
#version 460
layout(location = 0) out vec4 fragColor;
in float intensity;
in vec2 vertexTexcoords;
in vec3 fnormal;
uniform sampler2D tex;
uniform vec4 diffuse;
uniform vec4 ambient;
void main()
{
	fragColor = vec4(fnormal, 1.1);
}
"""

c_shader = """
#version 460
layout(location = 0) out vec4 fragColor;
in float intensity;
in vec2 vertexTexcoords;
in vec3 v3Position;
in float ftime;
in vec3 fnormal;
uniform sampler2D tex;
uniform vec4 diffuse;
uniform vec4 ambient;
void main()
{
	float theta = ftime*20.0;
  
	vec3 dir1 = vec3(cos(theta),0,sin(theta)); 
	vec3 dir2 = vec3(sin(theta),0,cos(theta));
  
	float diffuse1 = pow(dot(fnormal,dir1),2.0);
	float diffuse2 = pow(dot(fnormal,dir2),2.0);
		
	vec3 col1 = diffuse1 * vec3(1,0,0);
	vec3 col2 = diffuse2 * vec3(0,0,1);
    gl_FragColor = vec4(col1 + col2, 1.0);
}
"""
