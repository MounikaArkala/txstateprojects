#ifndef MAP_H
#define MAP_H

struct MapVertex
{
	float p[3];
	float n[3];
};


class Map
{
public:

	MapVertex *vertex;
	unsigned int buffer;

	int vertices;
	unsigned int *index;
	int indices;
	unsigned int indexbuffer;

	int tiledim, simdim;

	float height_scale;
	float width, unitsize;

	Map()
	{
		vertex = 0;
		buffer = 0;

		index = 0;
		indices = 0;
		indexbuffer = 0;
	}
	~Map()
	{
		Clear();
	}
	void Init();
	void Clear();

	void Step(float t);
	void Draw(vector3 cam_pos);

	float GetHeight(float x, float z);
	vector3 GetNormal(float x, float z);
	float Trace(const vector3 &origin, const vector3 &dir, vector3 &hit, const float maxdist);

private:
};

#endif