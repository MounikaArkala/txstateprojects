#ifndef GAME_H
#define GAME_H

#include "model.h"

#include "map.h"
extern Map map;

struct Camera
{
	vector3 pos;
	quaternion rot;
	float pitch, yaw;

	matrix transform, inv_transform;
};

extern Camera camera;

extern float gameframetime;

extern float mousex, mousey;

extern int wireframe;


void GameLoop(float t);
void GameShutdown();
void GameStartup();

#endif