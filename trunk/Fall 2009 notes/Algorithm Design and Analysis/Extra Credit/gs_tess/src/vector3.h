#ifndef VECTOR3_H
#define VECTOR3_H

// 3-component vector class, quaternion class, and helper functions

#include <math.h>

#define PI					3.1415926535f
#define TWOPI				6.283185307f
#define PIOVER180			0.0174532925f
#define RAD2DEG				57.2957795131f

class vector3
{
private:
public:
	union
	{
		float v[3];
		struct
		{
			float x, y, z;
		};
	};

	vector3()
	{
	}
	vector3 (const float *p)
	{
		v[0] = p[0];
		v[1] = p[1];
		v[2] = p[2];
	}
	vector3(const float a, const float b, const float c)
	{
		v[0] = a; v[1] = b; v[2] = c;
	}
	vector3(const vector3 &a, const vector3 &b)
	{
		v[0] = a.v[0] - b.v[0];
		v[1] = a.v[1] - b.v[1];
		v[2] = a.v[2] - b.v[2];
	}
	// negate
	vector3 operator - () const
	{
		return vector3(-v[0], -v[1], -v[2]);
	}
	void operator += (const vector3 &param)
	{
		v[0] += param.v[0];
		v[1] += param.v[1];
		v[2] += param.v[2];
	}
	void operator += (const float param)
	{
		v[0] += param;
		v[1] += param;
		v[2] += param;
	}
	void operator -= (const vector3 &param)
	{
		v[0] -= param.v[0];
		v[1] -= param.v[1];
		v[2] -= param.v[2];
	}
	void operator -= (const float param)
	{
		v[0] -= param;
		v[1] -= param;
		v[2] -= param;
	}
	void operator *= (const vector3 &param)
	{
		v[0] *= param.v[0];
		v[1] *= param.v[1];
		v[2] *= param.v[2];
	}
	void operator *= (const float param)
	{
		v[0] *= param;
		v[1] *= param;
		v[2] *= param;
	}
	void operator /= (const vector3 &param)
	{
		v[0] /= param.v[0];
		v[1] /= param.v[1];
		v[2] /= param.v[2];
	}
	void operator /= (const float param)
	{
		float ftemp = 1 / param;
		v[0] *= ftemp;
		v[1] *= ftemp;
		v[2] *= ftemp;
	}
	vector3& normalize()
	{
		float invlen = 1 / sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
		v[0] *= invlen;
		v[1] *= invlen;
		v[2] *= invlen;
		return *this;
	}
	vector3& zeronormalize()
	{
		float invlen = sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
		if (invlen == 0)
			return *this;
		invlen = 1 / invlen;
		v[0] *= invlen;
		v[1] *= invlen;
		v[2] *= invlen;
		return *this;
	}
	void clamp(const float lower, const float upper)
	{
		if (v[0] > upper) v[0] = upper; else if (v[0] < lower) v[0] = lower;
		if (v[1] > upper) v[1] = upper; else if (v[1] < lower) v[1] = lower;
		if (v[2] > upper) v[2] = upper; else if (v[2] < lower) v[2] = lower;
	}
	float length() const
	{
		return sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
	}
	float length2() const
	{
		return v[0] * v[0] + v[1] * v[1] + v[2] * v[2];
	}
	bool operator == (vector3 param) const
	{
		if (v[0] == param.v[0] && v[1] == param.v[1] && v[2] == param.v[2])
			return 1;
		return 0;
	}
	bool operator != (vector3 param) const
	{
		if (v[0] != param.v[0] || v[1] != param.v[1] || v[2] != param.v[2])
			return 1;
		return 0;
	}
	void set(const float p1, const float p2, const float p3)
	{
		v[0] = p1; v[1] = p2; v[2] = p3;
	}
};

// *
inline vector3 operator * (const vector3 &a, const vector3 &b)
{
	return vector3(a.v[0] * b.v[0], a.v[1] * b.v[1], a.v[2] * b.v[2]);
}

inline vector3 operator * (const float param, const vector3 &v)
{
	return vector3(v.v[0] * param, v.v[1] * param, v.v[2] * param);
}

inline vector3 operator * (const vector3 &v, const float param)
{
	return vector3(v.v[0] * param, v.v[1] * param, v.v[2] * param);
}

// /
inline vector3 operator / (const vector3 &a, const vector3 &b)
{
	return vector3(a.v[0] / b.v[0], a.v[1] / b.v[1], a.v[2] / b.v[2]);
}

inline vector3 operator / (const float param, const vector3 &v)
{
	return vector3(param / v.v[0], param / v.v[1], param / v.v[2]);
}

inline vector3 operator / (const vector3 &v, const float param)
{
	float invparam = 1.0f / param;
	return vector3(v.v[0] * invparam, v.v[1] * invparam, v.v[2] * invparam);
}

// -
inline vector3 operator - (const vector3 &a, const vector3 &b)
{
	return vector3(a.v[0] - b.v[0], a.v[1] - b.v[1], a.v[2] - b.v[2]);
}

inline vector3 operator - (const float param, const vector3 &v)
{
	return vector3(param - v.v[0], param - v.v[1], param - v.v[2]);
}

inline vector3 operator - (const vector3 &v, const float param)
{
	return vector3(v.v[0] - param, v.v[1] - param, v.v[2] - param);
}

// +
inline vector3 operator + (const vector3 &a, const vector3 &b)
{
	return vector3(a.v[0] + b.v[0], a.v[1] + b.v[1], a.v[2] + b.v[2]);
}

inline vector3 operator + (const float param, const vector3 &v)
{
	return vector3(param + v.v[0], param + v.v[1], param + v.v[2]);
}

inline vector3 operator + (const vector3 &v, const float param)
{
	return vector3(v.v[0] + param, v.v[1] + param, v.v[2] + param);
}

inline vector3 VectorSet(const float a, const float b, const float c)
{
	return vector3(a, b, c);
}

inline bool operator < (const vector3 &p1, const vector3 &p2)
{
	if (p1.v[0] < p2.v[0])
		return true;
	else if (p1.v[0] > p2.v[0])
		return false;

	if (p1.v[1] < p2.v[1])
		return true;
	else if (p1.v[1] > p2.v[1])
		return false;

	if (p1.v[2] < p2.v[2])
		return true;
	else if (p1.v[2] > p2.v[2])
		return false;

	return false;
}

extern void MxM(float *m1, float *m2, float *r);
extern float Dot(const vector3&, const vector3&);
extern vector3 Cross(const vector3&, const vector3&);
extern vector3 Average(const vector3&, const vector3&);
extern vector3 NormalVec(vector3 a);
extern vector3 ZeroNormalVec(vector3 a);


class quaternion
{
private:
public:
	float x, y, z, w;
	quaternion()
	{
	}
	// removed normalization of axis and xyzw from set
	quaternion(vector3 axis, float radians)
	{
		radians *= .5f;
		w = cosf(radians);
		float sr = sinf(radians);
		x = axis.v[0] * sr;
		y = axis.v[1] * sr;
		z = axis.v[2] * sr;
	}
	void Set(vector3 axis, float radians)
	{
		radians *= .5f;
		w = cosf(radians);
		float sr = sinf(radians);
		x = axis.v[0] * sr;
		y = axis.v[1] * sr;
		z = axis.v[2] * sr;
	}
	quaternion(const float *a, float radians)
	{
		radians *= .5f;
		w = cosf(radians);
		float sr = sinf(radians);
		x = a[0] * sr;
		y = a[1] * sr;
		z = a[2] * sr;
	}
	void Set(const float *a, float radians)
	{
		radians *= .5f;
		w = cosf(radians);
		float sr = sinf(radians);
		x = a[0] * sr;
		y = a[1] * sr;
		z = a[2] * sr;
	}

	quaternion operator * (quaternion param)
	{
		vector3 v1, v2, vp;
		quaternion qp;

		v1.v[0] = x; v1.v[1] = y; v1.v[2] = z;
		v2.v[0] = param.x; v2.v[1] = param.y; v2.v[2] = param.z;
		qp.w = w * param.w - Dot(v1, v2);
		vp = v2 * w + v1 * param.w - Cross(v1, v2);
		qp.x = vp.v[0];
		qp.y = vp.v[1];
		qp.z = vp.v[2];
		return qp;
	}
	void operator *= (const quaternion param)
	{
		float vp[3];

		vp[0] = param.x * w + x * param.w - (y * param.z - z * param.y);
		vp[1] = param.y * w + y * param.w - (z * param.x - x * param.z);
		vp[2] = param.z * w + z * param.w - (x * param.y - y * param.x);

		w = w * param.w - (x * param.x + y * param.y + z * param.z);

		x = vp[0];
		y = vp[1];
		z = vp[2];
	}
	void Matrix(float *m)
	{
		float x2, y2, z2, xx, yy, zz, xy, yz, xz, wx, wy, wz;
		x2 = x + x;
		y2 = y + y;
		z2 = z + z;
		xx = x * x2;
		yy = y * y2;
		zz = z * z2;
		xy = x * y2;
		yz = y * z2;
		xz = z * x2;
		wx = w * x2;
		wy = w * y2;
		wz = w * z2;
		m[0] = 1 - (yy + zz);
		m[1] = xy + wz;
		m[2] = xz - wy;
		m[3] = 0;
		m[4] = xy - wz;
		m[5] = 1 - (xx + zz);
		m[6] = yz + wx;
		m[7] = 0;
		m[8] = xz + wy;
		m[9] = yz - wx;
		m[10] = 1 - (xx + yy);
		m[11] = 0;
		m[12] = 0;
		m[13] = 0;
		m[14] = 0;
		m[15] = 1;
	}
	void Matrix4x3(float *m)
	{
		float x2, y2, z2, xx, yy, zz, xy, yz, xz, wx, wy, wz;
		x2 = x + x;
		y2 = y + y;
		z2 = z + z;
		xx = x * x2;
		yy = y * y2;
		zz = z * z2;
		xy = x * y2;
		yz = y * z2;
		xz = z * x2;
		wx = w * x2;
		wy = w * y2;
		wz = w * z2;
		m[0] = 1 - (yy + zz);
		m[1] = xy + wz;
		m[2] = xz - wy;
		m[3] = 0;
		m[4] = xy - wz;
		m[5] = 1 - (xx + zz);
		m[6] = yz + wx;
		m[7] = 0;
		m[8] = xz + wy;
		m[9] = yz - wx;
		m[10] = 1 - (xx + yy);
		m[11] = 0;
//		m[12] = 0;
//		m[13] = 0;
//		m[14] = 0;
//		m[15] = 1;
	}
	quaternion Slerp(quaternion q, float c)
	{
		float omega, cosfomega, sinfomega, k1, k2;
		quaternion q2, q3;
		cosfomega = x * q.x + y * q.y + z * q.z + w * q.w;
		if (cosfomega < 0)
		{
			cosfomega = -cosfomega;
			q2.x = -q.x;
			q2.y = -q.y;
			q2.z = -q.z;
			q2.w = -q.w;
		}
		else
			q2 = q;

		if (1 - cosfomega > .000001f)
		{
			omega = acosf(cosfomega);
			sinfomega = sinf(omega);
			k1 = sinf((1 - c) * omega) / sinfomega;
			k2 = sinf(c * omega) / sinfomega;
		}
		else
		{
			k1 = 1 - c;
			k2 = c;
		}

		q3.x = x * k1 + q2.x * k2;
		q3.y = y * k1 + q2.y * k2;
		q3.z = z * k1 + q2.z * k2;
		q3.w = w * k1 + q2.w * k2;

		return q3;
	}

	quaternion& conjugate()
	{
		x *= -1;
		y *= -1;
		z *= -1;
		return *this;
	}

	bool operator == (const quaternion &p)
	{
		return (x == p.x && y == p.y && z == p.z && w == p.w);
	}
	bool operator != (const quaternion &p)
	{
		return (x != p.x || y != p.y || z != p.z || w != p.w);
	}
};

#endif