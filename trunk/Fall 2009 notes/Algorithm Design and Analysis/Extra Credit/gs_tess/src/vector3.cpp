// 3-component vector class and helper math functions

#include "vector3.h"

extern void MxM(float *m1, float *m2, float *r)
{
	r[0] = m1[0] * m2[0] + m1[4] * m2[1] + m1[8] * m2[2] + m1[12] * m2[3];
	r[1] = m1[1] * m2[0] + m1[5] * m2[1] + m1[9] * m2[2] + m1[13] * m2[3];
	r[2] = m1[2] * m2[0] + m1[6] * m2[1] + m1[10] * m2[2] + m1[14] * m2[3];
	r[3] = m1[3] * m2[0] + m1[7] * m2[1] + m1[11] * m2[2] + m1[15] * m2[3];
	r[4] = m1[0] * m2[4] + m1[4] * m2[5] + m1[8] * m2[6] + m1[12] * m2[7];
	r[5] = m1[1] * m2[4] + m1[5] * m2[5] + m1[9] * m2[6] + m1[13] * m2[7];
	r[6] = m1[2] * m2[4] + m1[6] * m2[5] + m1[10] * m2[6] + m1[14] * m2[7];
	r[7] = m1[3] * m2[4] + m1[7] * m2[5] + m1[11] * m2[6] + m1[15] * m2[7];
	r[8] = m1[0] * m2[8] + m1[4] * m2[9] + m1[8] * m2[10] + m1[12] * m2[11];
	r[9] = m1[1] * m2[8] + m1[5] * m2[9] + m1[9] * m2[10] + m1[13] * m2[11];
	r[10] = m1[2] * m2[8] + m1[6] * m2[9] + m1[10] * m2[10] + m1[14] * m2[11];
	r[11] = m1[3] * m2[8] + m1[7] * m2[9] + m1[11] * m2[10] + m1[15] * m2[11];
	r[12] = m1[0] * m2[12] + m1[4] * m2[13] + m1[8] * m2[14] + m1[12] * m2[15];
	r[13] = m1[1] * m2[12] + m1[5] * m2[13] + m1[9] * m2[14] + m1[13] * m2[15];
	r[14] = m1[2] * m2[12] + m1[6] * m2[13] + m1[10] * m2[14] + m1[14] * m2[15];
	r[15] = m1[3] * m2[12] + m1[7] * m2[13] + m1[11] * m2[14] + m1[15] * m2[15];
}

extern float Dot(const vector3 &a, const vector3 &b)
{
	return a.v[0] * b.v[0] + a.v[1] * b.v[1] + a.v[2] * b.v[2];
}

extern vector3 Cross(const vector3 &a, const vector3 &b)
{
	vector3 r;
	r.v[0] = a.v[1] * b.v[2] - a.v[2] * b.v[1];
	r.v[1] = a.v[2] * b.v[0] - a.v[0] * b.v[2];
	r.v[2] = a.v[0] * b.v[1] - a.v[1] * b.v[0];
	return r;
}

extern vector3 Average(const vector3 &a, const vector3 &b)
{
	vector3 r;
	r.v[0] = (a.v[0] + b.v[0]) * .5f;
	r.v[1] = (a.v[1] + b.v[1]) * .5f;
	r.v[2] = (a.v[2] + b.v[2]) * .5f;
	return r;
}

extern vector3 NormalVec(vector3 a)
{
	float invlen = 1 / sqrt(a.v[0] * a.v[0] + a.v[1] * a.v[1] + a.v[2] * a.v[2]);
	a.v[0] *= invlen;
	a.v[1] *= invlen;
	a.v[2] *= invlen;
	return a;
}

extern vector3 ZeroNormalVec(vector3 a)
{
	float invlen = sqrt(a.v[0] * a.v[0] + a.v[1] * a.v[1] + a.v[2] * a.v[2]);
	if (invlen == 0)
		return a;
	invlen = 1 / invlen;
	a.v[0] *= invlen;
	a.v[1] *= invlen;
	a.v[2] *= invlen;
	return a;
}