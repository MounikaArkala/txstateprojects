#include <time.h>
#include "main.h"
#include "render.h"
#include "window.h"
#include "input.h"
#include "main.h"
#include "game.h"

// framerate tracking
Timer		timer;
float		frametime = 0.02f;
float		elapsedtime = 0;

float		averagefps = 0;
float		fps[FPS_FRAMES];


float		game_rate = 1.0f / 100;
float		game_time = 0;

void ReadConfig(char *filename)
{
	FILE *file = fopen(filename, "rt");
	if (!file)
	{
		gamma = 1.0f;
		fullscreen = 0;
		wsizex = 1024;
		wsizey = wsizex * .75f;
		anisotropy = 4;
	}
	else
	{
		fscanf(file, "gamma %f\n", &gamma);
		fscanf(file, "fullscreen %d\n", &fullscreen);
		fscanf(file, "resolution %dx%d\n", &wsizex, &wsizey);
		fscanf(file, "anisotropy %d\n", &anisotropy);

		if (gamma < 0 || gamma > 10)
			gamma = 1.0f;
		if (fullscreen < 0 || fullscreen > 1)
			fullscreen = 0;
		if (wsizex < 1 || wsizex > 100000)
			wsizex = 1024;
		if (wsizey < 1 || wsizey > 100000)
			wsizey = wsizex * .75f;
		if (anisotropy < 1)
			anisotropy = 1;

		fclose(file);
	}


	input.BindInput("w", "move", 1);
	input.BindInput("s", "move", -1);
	input.BindInput("a", "strafe", -1);
	input.BindInput("d", "strafe", 1);
	input.BindInput("lcontrol", "vertical", -1);
	input.BindInput("space", "vertical", 1);
	input.BindInput("mousex", "lookyaw", 1);
	input.BindInput("mousey", "lookpitch", 1);

	input.BindInput("mousex", "cursorx", -1);
	input.BindInput("mousey", "cursory", 1);

	input.BindInput("mouse0", "select", 1, 0);
	input.BindInput("mouse1", "action", 1, 0);
	input.BindInput("mouse2", "freelook", 1);

	input.BindInput("e", "wireframe", 1, 0);
}

void WriteConfig(char *filename)
{
	FILE *file = fopen(filename, "wt");
	if (file)
	{
		fprintf(file, "gamma %f\n", gamma);
		fprintf(file, "fullscreen %d\n", fullscreen);
		fprintf(file, "resolution %dx%d\n", wsizex, wsizey);
		fprintf(file, "anisotropy %d\n", anisotropy);

		fclose(file);
	}
}

void Shutdown()
{
	GameShutdown();

	input.Shutdown();

	ShutdownRender();

	WindowShutdown();
}

void Startup()
{
	WindowStartup();

	input.Startup();

	StartupRender();

	GameStartup();
}

int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	timer.init();

	sgenrand(time(NULL));

	hInstance = hInst;
	MSG msg;

	memset(fps, 0, sizeof(float) * FPS_FRAMES);

	ReadConfig("config.ini");

	Startup();

	timer.init();

	while (1)
	{
		if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))
		{
			if (msg.message==WM_QUIT)
			{
				break;
			}
			else
			{
				TranslateMessage(&msg);
				DispatchMessage(&msg);
			}
		}
		else
		{
			if (active)
			{
				Render(frametime);

				frametime = timer.frametime();
				elapsedtime = timer.getelapsed();

				for (int n = 0; n < FPS_FRAMES - 1; n++)
					fps[n] = fps[n + 1];
				fps[FPS_FRAMES - 1] = 1.0f / frametime;
				averagefps = 0;
				for (int n = 0; n < FPS_FRAMES; n++)
					averagefps += fps[n];
				averagefps /= FPS_FRAMES;

				input.Update();

				GameLoop(frametime);
			}
		}
	}

	WriteConfig("config.ini");

	Shutdown();

	return (msg.wParam);
}