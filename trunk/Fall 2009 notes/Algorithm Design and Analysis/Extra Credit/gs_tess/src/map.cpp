#include "main.h"
#include "map.h"
#include "render.h"
#include "fft.h"
#include "noise.h"

#include "game.h"


float Map::Trace(const vector3 &origin, const vector3 &dir, vector3 &hit, const float maxdist)
{
	// clamp to map bounds
	float start[3];
	start[0] = origin.x;
	start[1] = origin.y;
	start[2] = origin.z;

	float bound = tiledim * unitsize;

	float xoff1, xoff2, zoff1, zoff2;
	xoff1 = -start[0];
	xoff2 = start[0] - bound;
	zoff1 = -start[2];
	zoff2 = start[2] - bound;

	if (xoff1 > 0 && xoff1 >= xoff2 && xoff1 >= zoff1 && xoff1 >= zoff2)
	{
		// needs to be pointing the right way
		if (dir.v[0] <= 0)
			return -1;
		float d = xoff1 / dir.v[0];
		start[0] += xoff1;
		start[1] += d * dir.v[1];
		start[2] += d * dir.v[2];
		if (start[2] < 0 || start[2] > bound)
			return -1;
	}
	else if (xoff2 > 0 && xoff2 >= xoff1 && xoff2 >= zoff1 && xoff2 >= zoff2)
	{
		// needs to be pointing the right way
		if (dir.v[0] >= 0)
			return -1;
		float d = -xoff2 / dir.v[0];
		start[0] -= xoff2;
		start[1] += d * dir.v[1];
		start[2] += d * dir.v[2];
		if (start[2] < 0 || start[2] > bound)
			return -1;
	}
	else if (zoff1 > 0 && zoff1 >= xoff1 && zoff1 >= xoff2 && zoff1 >= zoff2)
	{
		// needs to be pointing the right way
		if (dir.v[2] <= 0)
			return -1;
		float d = zoff1 / dir.v[2];
		start[0] += d * dir.v[0];
		start[1] += d * dir.v[1];
		start[2] += zoff1;
		if (start[0] < 0 || start[0] > bound)
			return -1;
	}
	else if (zoff2 > 0 && zoff2 >= xoff1 && zoff2 >= xoff2 && zoff2 >= zoff1)
	{
		// needs to be pointing the right way
		if (dir.v[2] >= 0)
			return -1;
		float d = -zoff2 / dir.v[2];
		start[0] += d * dir.v[0];
		start[1] += d * dir.v[1];
		start[2] -= zoff2;
		if (start[0] < 0 || start[0] > bound)
			return -1;
	}

	float len = sqrt(dir.v[0] * dir.v[0] + dir.v[1] * dir.v[1] + dir.v[2] * dir.v[2]);
	if (len <= 0)
		return -1;

	float stepsize = .1f;
	float dist = 0;
	float testpt[3];
	while (dist <= maxdist)
	{
		testpt[0] = start[0] + dir.v[0] * dist;
		testpt[1] = start[1] + dir.v[1] * dist;
		testpt[2] = start[2] + dir.v[2] * dist;

		// out of bounds
		if (testpt[0] < 0 || testpt[0] > bound || testpt[2] < 0 || testpt[2] > bound)
			return -1;

		float h = GetHeight(testpt[0], testpt[2]);
		if (h >= testpt[1])
		{
			if (dist == 0)
				return -1;
			hit.v[0] = testpt[0];
			hit.v[1] = testpt[1];
			hit.v[2] = testpt[2];
			return dist;
		}

		dist += stepsize;
	}

	// out of range
	return -1;
}

float Map::GetHeight(float x, float z)
{
	if (x < 0)
		x = 0;
	else if (x >= width)
		x = width - .001f;

	if (z < 0)
		z = 0;
	else if (z >= width)
		z = width - .001f;

	// repeat
	/*x = fmod(x, width);
	if (x < 0)
		x += width;
	z = fmod(z, width);
	if (z < 0)
		z += width;*/


	int x1, x2, z1, z2;
	float xr, zr;
	x1 = x / unitsize;
	x2 = x1 + 1;
	if (x2 > tiledim - 1)
		x2 = tiledim - 1;
	xr = (x - x1 * unitsize) / unitsize;

	z1 = z / unitsize;
	z2 = z1 + 1;
	if (z2 > tiledim - 1)
		z2 = tiledim - 1;
	zr = (z - z1 * unitsize) / unitsize;


	// need two frame samples, because we're interpolating
	float h;
	if (zr > xr)
	{
		float hx1z2;

		hx1z2 = vertex[z2 * tiledim + x1].p[1];
		h = hx1z2 + (vertex[z2 * tiledim + x2].p[1] - hx1z2) * xr + (vertex[z1 * tiledim + x1].p[1] - hx1z2) * (1.0f - zr);
	}
	else
	{
		float hx2z1;

		hx2z1 = vertex[z1 * tiledim + x2].p[1];
		h = hx2z1 + (vertex[z1 * tiledim + x1].p[1] - hx2z1) * (1.0f - xr) + (vertex[z2 * tiledim + x2].p[1] - hx2z1) * zr;
	}

	return h;
}

vector3 Map::GetNormal(float x, float z)
{
	if (x < 0)
		x = 0;
	else if (x >= width)
		x = width - .001f;

	if (z < 0)
		z = 0;
	else if (z >= width)
		z = width - .001f;

	// repeat
	/*x = fmod(x, width);
	if (x < 0)
		x += width;
	z = fmod(z, width);
	if (z < 0)
		z += width;*/


	int x1, x2, z1, z2;
	float xr, zr;
	x1 = x / unitsize;
	x2 = x1 + 1;
	if (x2 > tiledim - 1)
		x2 = tiledim - 1;
	xr = (x - x1 * unitsize) / unitsize;

	z1 = z / unitsize;
	z2 = z1 + 1;
	if (z2 > tiledim - 1)
		z2 = tiledim - 1;
	zr = (z - z1 * unitsize) / unitsize;


	// need two frame samples, because we're interpolating
	// this is probably more exact that what we're doing in the vertex shader
	vector3 normal, tangent, binormal;
	if (zr > xr)
	{
		float hx1z2;

		hx1z2 = vertex[z2 * tiledim + x1].p[1];
		tangent.v[0] = unitsize;
		tangent.v[1] = (vertex[z2 * tiledim + x2].p[1] - hx1z2);
		tangent.v[2] = 0;
		binormal.v[0] = 0;
		binormal.v[1] = (hx1z2 - vertex[z1 * tiledim + x1].p[1]);
		binormal.v[2] = unitsize;

		tangent.normalize();
		binormal.normalize();
		normal = Cross(binormal, tangent);
		normal.normalize();
	}
	else
	{
		float hx2z1;

		hx2z1 = vertex[z1 * tiledim + x2].p[1];
		tangent.v[0] = unitsize;
		tangent.v[1] = (hx2z1 - vertex[z1 * tiledim + x1].p[1]);
		tangent.v[2] = 0;
		binormal.v[0] = 0;
		binormal.v[1] = (vertex[z2 * tiledim + x2].p[1] - hx2z1);
		binormal.v[2] = unitsize;

		tangent.normalize();
		binormal.normalize();
		normal = Cross(binormal, tangent);
		normal.normalize();
	}

	return normal;
}

void Map::Step(float t)
{
}

void Map::Draw(vector3 cam_pos)
{
	if (wireframe)
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

	static int ground_tex = CreateTexture("mid_grass1", false, false, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR);

	// subdivision levels
	//int verts_out = ((1 << subd_upper) + 2) * (1 << subd_upper);
// for now we'll just use this until things get straightened out
	int verts_out = 80;

	static int map_program = CreateProgram("map", "map", "map", GL_TRIANGLES, GL_TRIANGLE_STRIP, verts_out);
	glUseProgram(program[map_program].id);

	glUniform1f(glGetUniformLocation(program[map_program].id, "subd_max"), 2.99f);

	int position = glGetAttribLocation(program[map_program].id, "position_in");
	int normal = glGetAttribLocation(program[map_program].id, "normal_in");

	// ground texture
	glActiveTexture(GL_TEXTURE0 + glGetUniformLocation(program[map_program].id, "ground_tex"));
	glBindTexture(GL_TEXTURE_2D, texture[ground_tex]);
	glActiveTexture(GL_TEXTURE0);

	// light direction
	vector3 light_dir(-1, 4, -1);
	light_dir.normalize();
	glUniform3f(glGetUniformLocation(program[map_program].id, "light_dir"), light_dir.x, light_dir.y, light_dir.z);

	// indices
	glBindBufferARB(GL_ELEMENT_ARRAY_BUFFER_ARB, indexbuffer);

	// vertex data
	glBindBufferARB(GL_ARRAY_BUFFER_ARB, buffer);
	glVertexAttribPointer(position, 3, GL_FLOAT, false, sizeof(MapVertex), (void*)offsetof(MapVertex, p));
	glEnableVertexAttribArray(position);
	glVertexAttribPointer(normal, 3, GL_FLOAT, false, sizeof(MapVertex), (void*)offsetof(MapVertex, n));
	glEnableVertexAttribArray(normal);

	//for (int x = -1; x <= 1; x++)
	//{
	//	for (int y = -1; y <= 1; y++)
	//	{
			//vector3 offset = VectorSet(x * width, 0, y * width);
			vector3 offset(0, 0, 0);

			// offset
			glUniform3f(glGetUniformLocation(program[map_program].id, "position_offset"), offset.x, offset.y, offset.z);

			// draw
			glDrawRangeElementsEXT(GL_TRIANGLE_STRIP, 0, vertices - 1, indices, GL_UNSIGNED_INT, 0);
	//	}
	//}

	glDisableVertexAttribArray(position);
	glDisableVertexAttribArray(normal);


	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
}

void Map::Init()
{
	tiledim = 33;
	simdim = tiledim - 1;

	width = 256;
	unitsize = width / (tiledim - 1);

	height_scale = 5;


	vertices = tiledim * tiledim;

	// indices
	indices = (tiledim - 1) * tiledim * 2 + (tiledim - 1) * 2;
	index = new unsigned int [indices];
	int p = 0;
	// left to right is usually faster
	for (int h = 0; h < tiledim - 1; h++)
	{
		int w;
		for (w = 0; w < tiledim; w++)
		{
			index[p++] = (h + 0) * tiledim + w;
			index[p++] = (h + 1) * tiledim + w;
		}
		if (h < simdim * 2)
		{
			index[p++] = (h + 1) * tiledim + w - 1;
			index[p++] = (h + 1) * tiledim + 0;
		}
	}
	glGenBuffers(1, &indexbuffer);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indexbuffer);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(unsigned int) * indices, index, GL_STATIC_DRAW);


	// vertices
	// the filtering doesn't seem to be quite perfect...we shouldn't have to do FixEdges, and FixEdges causes artifacts
	// in edge normals (strips of normals biased the same direction)
	float *heightpow2 = new float [simdim * simdim];
	NoiseFFT(heightpow2, simdim, 1.0f, 1.5f);
	float *heighttemp = new float [tiledim * tiledim];
	//BicubicFloat(heightpow2, heighttemp, simdim, simdim, tiledim, tiledim);
	BilinearFloat(heightpow2, heighttemp, simdim, simdim, tiledim, tiledim);
	FixEdges(heighttemp, tiledim);
	delete [] heightpow2;

	vertex = new MapVertex [tiledim * tiledim];

	// fill arrays
	for (int h = 0; h < tiledim; h++)
	{
		for (int w = 0; w < tiledim; w++)
		{
			vertex[h * tiledim + w].p[0] = w * unitsize;
			vertex[h * tiledim + w].p[2] = h * unitsize;
			vertex[h * tiledim + w].p[1] = heighttemp[h * tiledim + w] * height_scale;
		}
	}
	delete [] heighttemp;

	float invlen;
	for (int h = 0; h < tiledim; h++)
	{
		int h2 = h + 1;
		if (h2 >= tiledim)
			h2 = 1;
		for (int w = 0; w < tiledim; w++)
		{
			int w2 = w + 1;
			if (w2 >= tiledim)
				w2 = 1;

			vertex[h * tiledim + w].n[0] = (vertex[h * tiledim + w].p[1] - vertex[h * tiledim + w2].p[1]) * unitsize;
			vertex[h * tiledim + w].n[1] = 1.0f;
			vertex[h * tiledim + w].n[2] = (vertex[h * tiledim + w].p[1] - vertex[h2 * tiledim + w].p[1]) * unitsize;

			// assume y = 1
			invlen = 1.0f / sqrt(vertex[h * tiledim + w].n[0] * vertex[h * tiledim + w].n[0] + vertex[h * tiledim + w].n[2] * vertex[h * tiledim + w].n[2] + 1.0f);
			vertex[h * tiledim + w].n[0] *= invlen;
			vertex[h * tiledim + w].n[1] *= invlen;
			vertex[h * tiledim + w].n[2] *= invlen;
		}
	}

	// upload
	glGenBuffers(1, &buffer);
	glBindBuffer(GL_ARRAY_BUFFER, buffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(MapVertex) * vertices, vertex, GL_STATIC_DRAW);
}

void Map::Clear()
{
	if (vertex)
		delete [] vertex;
	vertex = 0;
	vertices = 0;

	if (buffer)
		glDeleteBuffers(1, &buffer);
	buffer = 0;

	if (index)
		delete [] index;
	index = 0;
	indices = 0;

	if (indexbuffer)
		glDeleteBuffers(1, &indexbuffer);
	indexbuffer = 0;
}