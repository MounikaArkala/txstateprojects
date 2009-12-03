#include "main.h"
#include "render.h"
#include "window.h"
#include "vis.h"
#include "game.h"


float znear = 0.50f;//, zfar = 2000000;
float fov = 45;

matrix mm, mp;

float clearcolor[4] = {0, 0, 0, 0};


void Render2DOverlays()
{
	glUseProgram(0);

	// overlays section
	glDisable(GL_DEPTH_TEST);
	glDisable(GL_CULL_FACE);
	glDepthMask(0);

	// clip coordinates
	glMatrixMode(GL_PROJECTION);
	glPushMatrix();
	glLoadIdentity();
	glMatrixMode(GL_MODELVIEW);
	glPushMatrix();
	glLoadIdentity();

	glDisable(GL_TEXTURE_2D);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	glEnable(GL_BLEND);



	glDisable(GL_BLEND);

	glMatrixMode(GL_PROJECTION);
	glPopMatrix();
	glMatrixMode(GL_MODELVIEW);
	glPopMatrix();


	// window coordinates for text
	glPushMatrix();
	glLoadIdentity();
	RECT window;
	GetClientRect(hWnd, &window);
	glMatrixMode(GL_PROJECTION);
	glPushMatrix();
	glLoadIdentity();
	glOrtho(0, window.right, 0, window.bottom, -1, 1);
	glMatrixMode(GL_MODELVIEW);


	// mouse cursor
	glDisable(GL_TEXTURE_2D);
	glPointSize(5);
	glBegin(GL_POINTS);
	glColor4f(.5f, .5f, 1.0f, 1.0f);
	glVertex3f(mousex, mousey, 0);
	glEnd();


	glAlphaFunc(GL_GREATER, .25f);
	glEnable(GL_ALPHA_TEST);
	// premultipled
	glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA);
	glEnable(GL_BLEND);

	glEnable(GL_TEXTURE_2D);
	glColor4f(1, 1, 1, 1);
	glBindTexture(GL_TEXTURE_2D, texture[fonttex]);

	glColor4f(1, 0, 0, 1);
	PrintScaled(.75f, 0, wsizey - 32 * 0.75f * 1, "FPS: %.1f", averagefps);
	PrintScaled(.75f, 0, wsizey - 32 * 0.75f * 2, "E: toggle wireframe");

	glColor4f(1, 1, 1, 1);

	glDisable(GL_ALPHA_TEST);
	glDisable(GL_BLEND);


	// end window coordinates
	glMatrixMode(GL_PROJECTION);
	glPopMatrix();
	glMatrixMode(GL_MODELVIEW);
	glPopMatrix();


	glDepthMask(1);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_CULL_FACE);
}

void RenderStart()
{
	// check for changes to the original files and update if needed
	UpdateModels();
	UpdateShaders();
	UpdateTextures();

	// for accurate timing...
	glFinish();
	SwapBuffers(hDC);

	// ATI + fragment.position + pointsize or linewidth > 1
	glPointSize(1);
	glLineWidth(1);

	glEnable(GL_DEPTH_TEST);
	glDepthFunc(GL_LEQUAL);
	glEnable(GL_CULL_FACE);

	glClearColor(clearcolor[0], clearcolor[1], clearcolor[2], clearcolor[3]);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	// infinite clip plane
	float p[4][4];
	p[1][0] = p[2][0] = p[3][0] = p[0][1] = p[2][1] = p[3][1] = p[0][2] = p[1][2] = p[0][3] = p[1][3] = p[3][3] = 0;
	p[0][0] = (1 / tan((float)fov * .5f * PIOVER180)) / ((float)wsizex / (float)wsizey);
	p[1][1] = (1 / tan((float)fov * .5f * PIOVER180));
	p[3][2] = (float)-2 * znear; // near clip
	p[2][2] = p[2][3] = -1;
	glMatrixMode(GL_PROJECTION);
	glLoadMatrixf((float *)p);

	glMatrixMode(GL_MODELVIEW);
	glLoadMatrixf(camera.inv_transform.m);

	glGetFloatv(GL_MODELVIEW_MATRIX, mm.m);
	glGetFloatv(GL_PROJECTION_MATRIX, mp.m);
}

void Render(float t)
{
	RenderStart();

	map.Draw(camera.pos);

	Render2DOverlays();
}

void StartupRender()
{
	glewInit();

	TextureStartup();

	ShaderStartup();


	fonttex = CreateTexture("font", true, false, GL_NEAREST, GL_LINEAR);
	BuildFont("font", fonttex, fontbase);
}

void ShutdownRender()
{
	ShaderShutdown();

	TextureShutdown();
}

void Resize(int width, int height, int xoffset, int yoffset, float fov)
{
	if (height <= 0)
		height = 1;
	if (width <= 0)
		width = 1;

	wsizex = width;
	wsizey = height;

	glViewport(xoffset, yoffset, width, height);
}