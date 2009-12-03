#include "main.h"
#include "input.h"
#include "game.h"
#include "vis.h"
#include "render.h"
#include "window.h"

Map map;

Camera camera;
float mousespeed = .1f;

float gameframetime = 0;

float mousex = wsizex / 2, mousey = wsizey / 2;
float cursorspeed = 1.0f;
vector3 mousevec(0, 0, 0);

int wireframe = 1;


vector3 WindowCoordToVector(float x, float y)
{
	vector3 rayvec;
	rayvec.set((x / wsizex * 2 - 1) * 1 * tan(fov * PIOVER180 * .5f) * ((float)wsizex / wsizey), (y / wsizey * 2 - 1) * 1 * tan(fov * PIOVER180 * .5f), -1);
	rayvec.normalize();
	rayvec = camera.transform.dirmult(rayvec);

	return rayvec;
}

void GameLoop(float t)
{
	gameframetime = t;

	map.Step(t);


////// camera
	Camera oldcam = camera;

	if (!input.GetState("freelook"))
	{
		camera.yaw += mousespeed * input.GetState("lookyaw");
		camera.pitch += mousespeed * input.GetState("lookpitch");
	}
	else
	{
		mousex += cursorspeed * input.GetState("cursorx");
		mousey += cursorspeed * input.GetState("cursory");
		if (mousex < 0)
			mousex = 0;
		else if (mousex > wsizex)
			mousex = wsizex;
		if (mousey < 0)
			mousey = 0;
		else if (mousey > wsizey)
			mousey = wsizey;
	}

	camera.rot = quaternion(VectorSet(1, 0, 0), camera.pitch * PIOVER180)
				* quaternion(VectorSet(0, 1, 0), camera.yaw * PIOVER180);

	camera.rot.Matrix4x3(camera.transform.m);

	// camera position
	float speed = 10;
	float move = input.GetState("move");
	float strafe = input.GetState("strafe");
	float vertical = input.GetState("vertical");
	vector3 movevec = camera.transform.zvec();
	vector3 strafevec = camera.transform.xvec();
	camera.pos += gameframetime * speed * (-move * movevec + strafe * strafevec + vertical * vector3(0, 1, 0));

	camera.transform.m[12] = camera.pos.v[0];
	camera.transform.m[13] = camera.pos.v[1];
	camera.transform.m[14] = camera.pos.v[2];
	camera.transform.m[15] = 1;

	// camera inverse
	camera.inv_transform = camera.transform;
	camera.inv_transform.inverse();

	mousevec = WindowCoordToVector(mousex, mousey);

	if (input.GetState("wireframe"))
	{
		wireframe ^= 1;
	}
//////


	// iterate particles
//	UpdateParticles(gameframetime);

	// check object visibility
	Vis();
}

void GameShutdown()
{
}

void GameStartup()
{
	// launch the monitor thread for updating materials/models in real time
	ModelStartup();

	// default model and material to 0 slot
	LoadModel("default");

	sgenrand(119);

	map.Init();

	camera.pos.set(0, 10, 0);
	camera.rot.Set(VectorSet(0, 1, 0), 0);
	camera.pitch = -20;
	camera.yaw = 225;
	camera.transform.identity();
	camera.inv_transform.identity();



	//gamestate.AddBuilding(0, 0, 0);
}