#include "main.h"
#include "vis.h"
#include "render.h"
#include "window.h"
#include "game.h"

void Vis()
{
/*	float aspect = (float)wsizex / (float)wsizey;

	CleaveData cd;
	Plane p[5];

	float invlen;
	float t = 1 / (tan(fov * PIOVER180 * .5f) * aspect);
	float t2 = 1 / tan(fov * PIOVER180 * .5f);
	// left = camera.forward.v + camera.right.v * 1 / (tan(fov * PIOVER180 * .5f) * (float)wsizex / (float)wsizey)
	p[0].n[0] = camera.forward.v[0] + camera.right.v[0] * t;
	p[0].n[1] = camera.forward.v[1] + camera.right.v[1] * t;
	p[0].n[2] = camera.forward.v[2] + camera.right.v[2] * t;
	invlen = 1 / sqrt(p[0].n[0] * p[0].n[0] + p[0].n[1] * p[0].n[1] + p[0].n[2] * p[0].n[2]);
	p[0].n[0] *= invlen;
	p[0].n[1] *= invlen;
	p[0].n[2] *= invlen;
	p[0].d = camera.pos.v[0] * p[0].n[0] + camera.pos.v[1] * p[0].n[1] + camera.pos.v[2] * p[0].n[2];
	cd.AddPlane(p[0]);
	// right = camera.forward.v - camera.right.v * 1 / (tan(fov * PIOVER180 * .5f) * (float)wsizex / (float)wsizey)
	p[1].n[0] = camera.forward.v[0] - camera.right.v[0] * t;
	p[1].n[1] = camera.forward.v[1] - camera.right.v[1] * t;
	p[1].n[2] = camera.forward.v[2] - camera.right.v[2] * t;
	invlen = 1 / sqrt(p[1].n[0] * p[1].n[0] + p[1].n[1] * p[1].n[1] + p[1].n[2] * p[1].n[2]);
	p[1].n[0] *= invlen;
	p[1].n[1] *= invlen;
	p[1].n[2] *= invlen;
	p[1].d = camera.pos.v[0] * p[1].n[0] + camera.pos.v[1] * p[1].n[1] + camera.pos.v[2] * p[1].n[2];
	cd.AddPlane(p[1]);
	// bottom = camera.forward.v + camera.up.v * 1 / tan(fov * PIOVER180 * .5f)
	p[2].n[0] = camera.forward.v[0] + camera.up.v[0] * t2;
	p[2].n[1] = camera.forward.v[1] + camera.up.v[1] * t2;
	p[2].n[2] = camera.forward.v[2] + camera.up.v[2] * t2;
	invlen = 1 / sqrt(p[2].n[0] * p[2].n[0] + p[2].n[1] * p[2].n[1] + p[2].n[2] * p[2].n[2]);
	p[2].n[0] *= invlen;
	p[2].n[1] *= invlen;
	p[2].n[2] *= invlen;
	p[2].d = camera.pos.v[0] * p[2].n[0] + camera.pos.v[1] * p[2].n[1] + camera.pos.v[2] * p[2].n[2];
	cd.AddPlane(p[2]);
	// top = camera.forward.v - camera.up.v * 1 / tan(fov * PIOVER180 * .5f)
	p[3].n[0] = camera.forward.v[0] - camera.up.v[0] * t2;
	p[3].n[1] = camera.forward.v[1] - camera.up.v[1] * t2;
	p[3].n[2] = camera.forward.v[2] - camera.up.v[2] * t2;
	invlen = 1 / sqrt(p[3].n[0] * p[3].n[0] + p[3].n[1] * p[3].n[1] + p[3].n[2] * p[3].n[2]);
	p[3].n[0] *= invlen;
	p[3].n[1] *= invlen;
	p[3].n[2] *= invlen;
	p[3].d = camera.pos.v[0] * p[3].n[0] + camera.pos.v[1] * p[3].n[1] + camera.pos.v[2] * p[3].n[2];
	cd.AddPlane(p[3]);
	// back plane = camera.forward.v
	p[4].n[0] = camera.forward.v[0];
	p[4].n[1] = camera.forward.v[1];
	p[4].n[2] = camera.forward.v[2];
	invlen = 1 / sqrt(p[4].n[0] * p[4].n[0] + p[4].n[1] * p[4].n[1] + p[4].n[2] * p[4].n[2]);
	p[4].n[0] *= invlen;
	p[4].n[1] *= invlen;
	p[4].n[2] *= invlen;
	p[4].d = camera.pos.v[0] * p[4].n[0] + camera.pos.v[1] * p[4].n[1] + camera.pos.v[2] * p[4].n[2];
	cd.AddPlane(p[4]);

*/

	// do planets
	/*for (int n = 0; n < planets; n++)
	{
		if (cd.IsOutside2(planet[n].offset, planet[n].planetradius * 1.1f) != -1)
		{
			planet[n].visible = 0;
			continue;
		}
		planet[n].visible = 1;
	}*/
}