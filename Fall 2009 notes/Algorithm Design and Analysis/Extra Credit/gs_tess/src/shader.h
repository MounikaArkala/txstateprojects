#ifndef SHADER_H
#define SHADER_H

#define MAX_SHADER_NAME	64

struct ProgramInfo
{
	unsigned int id;
	char vshader[MAX_SHADER_NAME];
	char gshader[MAX_SHADER_NAME];
	char fshader[MAX_SHADER_NAME];
};
extern std::vector<ProgramInfo> program;

// gs_in: GL_POINTS, GL_LINES, GL_LINES_ADJACENCY_EXT, GL_TRIANGLES, GL_TRIANGLES_ADJACENCY_EXT
// gs_out: GL_POINTS, GL_LINE_STRIP, GL_TRIANGLE_STRIP
// gs_outmax: 1024 vertices on g80
int CreateProgram(const char *vshader, const char *gshader, const char *fshader, GLenum gs_in = GL_TRIANGLES, GLenum gs_out = GL_TRIANGLE_STRIP, GLenum gs_outmax = 3);

void UpdateShaders();
void ShaderStartup();
void ShaderShutdown();

#endif