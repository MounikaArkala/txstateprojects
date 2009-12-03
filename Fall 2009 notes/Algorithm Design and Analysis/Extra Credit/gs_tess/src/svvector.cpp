#include "svvector.h"

// doesn't like passing by reference

vector3 svadd(const vector3 a, const vector3 b)
{
	vector3 r;
	r.v[0] = a.v[0] + b.v[0];
	r.v[1] = a.v[1] + b.v[1];
	r.v[2] = a.v[2] + b.v[2];
	return r;
}

vector3 svaddf(const vector3 a, const float b)
{
	vector3 r;
	r.v[0] = a.v[0] + b;
	r.v[1] = a.v[1] + b;
	r.v[2] = a.v[2] + b;
	return r;
}

vector3 svsub(const vector3 a, const vector3 b)
{
	vector3 r;
	r.v[0] = a.v[0] - b.v[0];
	r.v[1] = a.v[1] - b.v[1];
	r.v[2] = a.v[2] - b.v[2];
	return r;
}

vector3 svsubf(const vector3 a, const float b)
{
	vector3 r;
	r.v[0] = a.v[0] - b;
	r.v[1] = a.v[1] - b;
	r.v[2] = a.v[2] - b;
	return r;
}

vector3 svmul(const vector3 a, const vector3 b)
{
	vector3 r;
	r.v[0] = a.v[0] * b.v[0];
	r.v[1] = a.v[1] * b.v[1];
	r.v[2] = a.v[2] * b.v[2];
	return r;
}

vector3 svmulf(const vector3 a, const float b)
{
	vector3 r;
	r.v[0] = a.v[0] * b;
	r.v[1] = a.v[1] * b;
	r.v[2] = a.v[2] * b;
	return r;
}

vector3 svdiv(const vector3 a, const vector3 b)
{
	vector3 r;
	r.v[0] = a.v[0] / b.v[0];
	r.v[1] = a.v[1] / b.v[1];
	r.v[2] = a.v[2] / b.v[2];
	return r;
}

vector3 svdivf(const vector3 a, const float b)
{
	vector3 r;
	r.v[0] = a.v[0] / b;
	r.v[1] = a.v[1] / b;
	r.v[2] = a.v[2] / b;
	return r;
}