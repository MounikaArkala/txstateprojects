#ifndef MODEL_H
#define MODEL_H

#include "render.h"


class Model
{
public:

	struct Vertex
	{
		float v[3];
		float n[3];
		float t[2];
	};

	struct Mesh
	{
		float radius;
		float min[3];
		float max[3];
		float center[3]; // center, from min/max
		float center_radius, center_radius2; // radius and squared radius from center point

		int vertices;
		int indices;
		Vertex *vertex;
		unsigned short *index;

		unsigned int buffer;
		unsigned int indexbuffer;

		unsigned int tex;
	};

	Mesh mesh;
	char name[64];

	Model()
	{
		mesh.vertices = 0;
		mesh.indices = 0;
		mesh.vertex = 0;
		mesh.index = 0;
		mesh.buffer = 0;
		mesh.indexbuffer = 0;
		name[0] = 0;
	}
	~Model()
	{
		Clear();
	}
	void Clear() // if using reference counting need to handle case of reloading the model due to out of game changes
	{
		mesh.vertices = 0;
		mesh.indices = 0;
		if (mesh.vertex)
		{
			delete [] mesh.vertex;
			mesh.vertex = 0;
		}
		if (mesh.index)
		{
			delete [] mesh.index;
			mesh.index = 0;
		}
		if (mesh.buffer)
		{
			glDeleteBuffersARB(1, &mesh.buffer);
			mesh.buffer = 0;
		}
		if (mesh.indexbuffer)
		{
			glDeleteBuffersARB(1, &mesh.indexbuffer);
			mesh.indexbuffer = 0;
		}
	}

	int Load(const char *filename);

private:
};

extern std::vector<Model*> model;

int LoadModel(const char *filename);

void ModelStartup(); // launch monitor thread
void UpdateModels(); // process outside updates

#endif