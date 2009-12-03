#include "matrix.h"
#include "vector3.h"

const char LogTable256[] = 
{
  0, 0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3,
  4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
  5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
  5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
  6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
  6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
  6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
  6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6,
  7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
  7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
  7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
  7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
  7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
  7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
  7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
  7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
};
// returns the log base 2, or the position of the highest bit set
int GetBitIndex(unsigned int v)
{
	register unsigned int t, tt; // temporaries

	if (tt = v >> 16)
	{
	  return (t = v >> 24) ? 24 + LogTable256[t] : 16 + LogTable256[tt & 0xFF];
	}
	else 
	{
	  return (t = v >> 8) ? 8 + LogTable256[t] : LogTable256[v];
	}
}

// does not do the translation portion
matrix LookAt(vector3 from, vector3 to, vector3 up)
{
	matrix m;
	m.identity();
	if (from == to)
		return m;

	vector3 f, s, u;
	f = (to - from).normalize();
	s = Cross(f, up).normalize();
	u = Cross(s, f);//.normalize();

	m.m[0] = s.v[0];
	m.m[1] = s.v[1];
	m.m[2] = s.v[2];

	m.m[4] = u.v[0];
	m.m[5] = u.v[1];
	m.m[6] = u.v[2];

	m.m[8] = -f.v[0];
	m.m[9] = -f.v[1];
	m.m[10] = -f.v[2];

	return m;
}

// PackBits - PSD files
void RLEUnpack(char *in, char *out, int inlen)
{
	int i = 0;
	int o = 0;
	while (i < inlen)
	{
		if (in[i] < 0)
		{
			for (int n = 0; n < -in[i] + 1; n++)
			{
				out[o] = in[i + 1];
				o++;
			}
			i += 2;
		}
		else
		{
			for (int n = 0; n < in[i] + 1; n++)
			{
				out[o] = in[i + n + 1];
				o++;
			}
			i += in[i] + 2;
		}
	}
}