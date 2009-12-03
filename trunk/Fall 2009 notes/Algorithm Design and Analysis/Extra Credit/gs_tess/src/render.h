#ifndef RENDER_H
#define RENDER_H

#pragma comment (lib, "opengl32")
#define GLEW_STATIC
#pragma comment (lib, "glew32s")

#include <glew.h>
#include <wglew.h>
#include "texture.h"
#include "shader.h"
#include "font.h"

extern float fov, znear;//, zfar;

extern matrix mm, mp;


void AddDynamicLight();

void Render(float t);
void StartupRender();
void ShutdownRender();
void Resize(int width, int height, int xoffset, int yoffset, float fov);

#endif