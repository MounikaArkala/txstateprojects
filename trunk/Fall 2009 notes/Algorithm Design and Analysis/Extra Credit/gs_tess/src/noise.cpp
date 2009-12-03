#include "main.h"
#include "noise.h"
#include "fft.h"

#pragma warning (disable: 4731)

int t1, t2;
int p3d_time = 10000000;

// matches edge values by averages
void FixEdges(float *height, int dim)
{
	for (int h = 1; h < dim - 1; h++)
	{
		float avg = .5f * (height[h * dim] + height[h * dim + dim - 1]);
		height[h * dim] = avg;
		height[h * dim + dim - 1] = avg;
	}

	for (int w = 1; w < dim - 1; w++)
	{
		float avg = .5f * (height[w] + height[(dim - 1) * dim + w]);
		height[w] = avg;
		height[(dim - 1) * dim + w] = avg;
	}

	// corners
	float avg = .25f * (height[0] + height[dim - 1] + height[(dim - 1) * dim] + height[(dim - 1) * dim + dim - 1]);
	height[0] = avg;
	height[dim - 1] = avg;
	height[(dim - 1) * dim] = avg;
	height[(dim - 1) * dim + dim - 1] = avg;
}

void Normalize(float *height, int dim)
{
	float min = 100000000000.0f;
	float max = -100000000000.0f;
	for (int n = 0; n < dim * dim; n++)
	{
		if (height[n] > max)
			max = height[n];
		if (height[n] < min)
			min = height[n];
	}
	float scale = 1.0f / (max - min);
	for (int n = 0; n < dim * dim; n++)
		height[n] = (height[n] - min) * scale;
}

void Perturb(float *height, int dim, float magnitude, int smoothness)
{
	float maxdist = magnitude * dim;
	int distbias = -maxdist * .5f;

	float *temp = new float [dim * dim];
	float *dh = new float [dim * dim];
	float *dw = new float [dim * dim];
	PerlinBicubic2(dh, dim, 16, max(1, GetBitIndex(dim) - smoothness));
	PerlinBicubic2(dw, dim, 16, max(1, GetBitIndex(dim) - smoothness));
	for (int n = 0; n < dim * dim; n++)
	{
		dh[n] = maxdist * (dh[n] - .0f);
		dw[n] = maxdist * (dw[n] - .0f);
	}

	for (int h = 0; h < dim; h++)
	{
		for (int w = 0; w < dim; w++)
		{
			int dh1, dh2, dw1, dw2;
			float dhr, dwr;
			dh1 = dh[h * dim + w];
			dh2 = dh[h * dim + w] + 1.0f;
			dhr = dh[h * dim + w] - dh1;
			// bias to a zero center after getting remainder to avoid truncation issue
			dh1 += distbias;
			dh2 += distbias;
			dw1 = dw[h * dim + w];
			dw2 = dw[h * dim + w] + 1.0f;
			dwr = dw[h * dim + w] - dw1;
			dw1 += distbias;
			dw2 += distbias;

			//temp[h * dim + w] = height[(((int)dh[h * dim + w] + h) + dim) % dim * dim + ((int)dw[h * dim + w] + w + dim) % dim];
			temp[h * dim + w] = (height[(dh1 + h + dim) % dim * dim + (dw1 + w + dim) % dim] * (1.0f - dhr)
								+ height[(dh2 + h + dim) % dim * dim + (dw1 + w + dim) % dim] * dhr) * (1.0f - dwr)
								+ (height[(dh1 + h + dim) % dim * dim + (dw2 + w + dim) % dim] * (1.0f - dhr)
								+ height[(dh2 + h + dim) % dim * dim + (dw2 + w + dim) % dim] * dhr) * dwr;
		}
	}

	memcpy(height, temp, sizeof(float) * dim * dim);

	delete [] temp;
	delete [] dh;
	delete [] dw;
}

// ripples are too noisy
void Perturb2(float *height, int dim, float magnitude, int smoothness)
{
	float maxdist = magnitude * dim * .5f;

	float *noise = new float [dim * dim];
	PerlinBicubic2(noise, dim, 16, max(1, GetBitIndex(dim) - smoothness));

	float *dmap = new float [dim * dim * 2];
	for (int h = 0; h < dim; h++)
	{
		int h1, h2;
		h1 = (h - 1 + dim) % dim;
		h2 = (h + 1) % dim;
		for (int w = 0; w < dim; w++)
		{
			int w1, w2;
			w1 = (w - 1 + dim) % dim;
			w2 = (w + 1) % dim;

			dmap[(h * dim + w) * 2 + 0] = maxdist * (noise[h2 * dim + w] - noise[h1 * dim + w]);
			dmap[(h * dim + w) * 2 + 1] = maxdist * (noise[h * dim + w2] - noise[h * dim + w1]);
		}
	}

	for (int h = 0; h < dim; h++)
	{
		for (int w = 0; w < dim; w++)
		{
			noise[h * dim + w] = height[(((int)dmap[(h * dim + w) * 2 + 0] + h) + dim) % dim * dim + ((int)dmap[(h * dim + w) * 2 + 1] + w + dim) % dim];
		}
	}

	memcpy(height, noise, sizeof(float) * dim * dim);
	delete [] noise;
}

void PerlinBicubic2(float *out, int outdim, int gridsize, int levels = 1)
{
	memset(out, 0, sizeof(float) * outdim * outdim);

	if (outdim / powf(2, levels) < 1)
	{
		levels = GetBitIndex(outdim);
	}


	float outscale = 1;
	float *upsampled = new float [outdim * outdim];
	for (int i = 0; i < levels; i++)
	{
		float *grid;
		grid = new float [gridsize * gridsize];

		for (int n = 0; n < gridsize * gridsize; n++)
		{
			grid[n] = genrand();
		}

		BicubicFloat(grid, upsampled, gridsize, gridsize, outdim, outdim);
		for (int n = 0; n < outdim * outdim; n++)
		{
			out[n] = outscale * upsampled[n] + out[n] * (1.0f - outscale);
		}

		outscale *= .5f;

		delete [] grid;
		gridsize *= 2.0f;
	}
	delete [] upsampled;


	float min = 100000000, max = 0;
	for (int n = 0; n < outdim * outdim; n++)
	{
		if (out[n] > max)
			max = out[n];
		if (out[n] < min)
			min = out[n];
	}
	float scale = 1.0f / (max - min);
	for (int n = 0; n < outdim * outdim; n++)
	{
		out[n] = (out[n] - min) * scale;
	}
}

// other combinations of d1*c1 + d2*c2 + d3*c3...dn*cn
// can be made faster with spatial partitioning
void Voronoi(float *height, int dim, int count, float bias)
{
	int *p = new int [count * 2];
	std::vector<float> d;
	d.resize(count);

	for (int n = 0; n < count; n++)
	{
		p[n * 2 + 0] = genrand() * dim;
		p[n * 2 + 1] = genrand() * dim;
	}

	for (int h = 0; h < dim; h++)
	{
		for (int w = 0; w < dim; w++)
		{
			for (int n = 0; n < count; n++)
			{
				int dh, dw;
				dh = abs(h - p[n * 2 + 0]);
				if (dh > dim / 2)
					dh = dim - dh;
				dw = abs(w - p[n * 2 + 1]);
				if (dw > dim / 2)
					dw = dim - dw;

				d[n] = dh * dh + dw * dw;
			}
			std::sort(d.begin(), d.end());
			height[h * dim + w] = max(0, -d[0] + d[1]);
		}
	}

	float min = 100000000, max = 0;
	for (int n = 0; n < dim * dim; n++)
	{
		if (height[n] > max)
			max = height[n];
		if (height[n] < min)
			min = height[n];
	}
	float scale = 1.0f / (max - min);
	for (int n = 0; n < dim * dim; n++)
	{
		height[n] = min(1, max(0, (height[n] - min) * scale + bias));
	}

	delete [] p;
}

int Roll(float *height, int dim, int maxdist, int &hx, int &hy)
{
	int x, y, x1, x2, y1, y2;
	float h;
	int i;
	for (i = 0; i < maxdist; i++)
	{
		x1 = (hx - 1 + dim) % dim;
		x2 = (hx + 1) % dim;
		x = hx;
		y = hy;
		y1 = (hy - 1 + dim) % dim;
		y2 = (hy + 1) % dim;

		h = height[x * dim + y];
		if (h > height[x1 * dim + y1])
		{
			h = height[x1 * dim + y1];
			hx = x1;
			hy = y1;
		}
		if (h > height[x1 * dim + y])
		{
			h = height[x1 * dim + y];
			hx = x1;
			hy = y;
		}
		if (h > height[x1 * dim + y2])
		{
			h = height[x1 * dim + y2];
			hx = x1;
			hy = y2;
		}
		if (h > height[x * dim + y1])
		{
			h = height[x * dim + y1];
			hx = x;
			hy = y1;
		}
		if (h > height[x * dim + y2])
		{
			h = height[x * dim + y2];
			hx = x;
			hy = y2;
		}
		if (h > height[x2 * dim + y1])
		{
			h = height[x2 * dim + y1];
			hx = x2;
			hy = y1;
		}
		if (h > height[x2 * dim + y])
		{
			h = height[x2 * dim + y];
			hx = x2;
			hy = y;
		}
		if (h > height[x2 * dim + y2])
		{
			h = height[x2 * dim + y2];
			hx = x2;
			hy = y2;
		}
		if (hx == x && hy == y)
			break;
	}
	return i;
}

void Deposition2(float *out, int dim, int iterations, float scale, int clear)
{
	if (clear)
		memset(out, 0, sizeof(float) * dim * dim);

//	float dropoff = 10.0f / iterations * scale;

	int x, y;
	x = genrand() * dim;
	y = genrand() * dim;
	float d;
	int hx, hy;
	for (int n = 0; n < iterations; n++)
	{
		hx = x;
		hy = y;

		Roll(out, dim, dim * 1.5f, hx, hy);

		//out[hx * dim + hy] += scale * (genrand() * .01f + .99f);
		out[hx * dim + hy] += scale;
		//out[hx * dim + hy] += scale * genrand();
		//out[hx * dim + hy] += scale * (genrand() * .5f + .5f);

		d = genrand();
		if (d < .25f)
		{
			x = (x - 1 + dim) % dim;
		}
		else if (d < .5f)
		{
			x = (x + 1) % dim;
		}
		else if (d < .75f)
		{
			y = (y - 1 + dim) % dim;
		}
		else
		{
			y = (y + 1) % dim;
		}

//		if (n % 10 == 0)
//			scale -= dropoff;
	}
}

void NoiseAdd(float *height, int dim, float strength)
{
	strength *= 2.0f;
	int size = dim * dim;
	for (int n = 0; n < size; n++)
	{
		height[n] += strength * (genrand() - .5f);
	}
}

void Erosion(float *out, int dim, int iterations, float scale, int maxdist, float radiusscale)
{
	int x, y;
	int x1, x2, y1, y2;
	int nx, ny;
	float h, horg;
	float radius, invradius;
	int rmax;
//	float vx, vy;
//	float ax, ay;
	for (int i = 0; i < iterations; i++)
	{
		x = genrand() * dim;
		y = genrand() * dim;
		radius = 2.0f;
		invradius = 1.0f / radius;
		rmax = radius;
//		vx = 0;
//		vy = 0;
		for (int c = 0; c < maxdist; c++)
		{
			x1 = (x - 1 + dim) % dim;
			x2 = (x + 1) % dim;
			y1 = (y - 1 + dim) % dim;
			y2 = (y + 1) % dim;
			nx = x;
			ny = y;
			h = out[x * dim + y];
			horg = h;
			if (h > out[x1 * dim + y1])
			{
				h = out[x1 * dim + y1];
				nx = x1;
				ny = y1;
//				ax = -1;
//				ay = -1;
			}
			if (h > out[x1 * dim + y])
			{
				h = out[x1 * dim + y];
				nx = x1;
				ny = y;
//				ax = -1;
//				ay = 0;
			}
			if (h > out[x1 * dim + y2])
			{
				h = out[x1 * dim + y2];
				nx = x1;
				ny = y2;
//				ax = -1;
//				ay = 1;
			}
			if (h > out[x * dim + y1])
			{
				h = out[x * dim + y1];
				nx = x;
				ny = y1;
//				ax = 0;
//				ay = -1;
			}
			if (h > out[x * dim + y2])
			{
				h = out[x * dim + y2];
				nx = x;
				ny = y2;
//				ax = 0;
//				ay = 1;
			}
			if (h > out[x2 * dim + y1])
			{
				h = out[x2 * dim + y1];
				nx = x2;
				ny = y1;
//				ax = 1;
//				ay = -1;
			}
			if (h > out[x2 * dim + y])
			{
				h = out[x2 * dim + y];
				nx = x2;
				ny = y;
//				ax = 1;
//				ay = 0;
			}
			if (h > out[x2 * dim + y2])
			{
				h = out[x2 * dim + y2];
				nx = x2;
				ny = y2;
//				ax = 1;
//				ay = 1;
			}
			if (x == nx && y == ny) // local minimum
			{
/*				if (abs(vx) >= 1 || abs(vy) >= 1)
				{
					if (vx >= 1)
						nx = x2;
					else if (vx <= -1)
						nx = x1;
					if (vy >= 1)
						ny = y2;
					else if (vy <= -1)
						ny = y1;

					vx *= .5f;
					vy *= .5f;
				}
				else*/
				{
					for (int rx = x - rmax; rx <= x + rmax; rx++)
					{
						int rxw = (rx + dim) % dim;
						for (int ry = y - rmax; ry <= y + rmax; ry++)
						{
							int ryw = (ry + dim) % dim;

							float d = sqrt((float)((x - rx) * (x - rx) + (y - ry) * (y - ry)));
							d = 1.0f - d / radius;
							if (d < 0)
								d = 0;

							out[rxw * dim + ryw] += scale * d * c;
						}
					}

					break;
				}
			}


			for (int rx = x - rmax; rx <= x + rmax; rx++)
			{
				int rxw = (rx + dim) % dim;
				for (int ry = y - rmax; ry <= y + rmax; ry++)
				{
					int ryw = (ry + dim) % dim;

					float d = sqrt((float)((x - rx) * (x - rx) + (y - ry) * (y - ry)));
					d = 1.0f - d * invradius;
					if (d < 0)
						d = 0;

					out[rxw * dim + ryw] -= scale * d;
				}
			}

//			vx += ax * (horg - h);
//			vy += ay * (horg - h);
			x = nx;
			y = ny;
			radius += radiusscale;
			rmax = radius + 1;
			invradius = 1.0f / radius;
		}
	}
}

void Deposition(float *out, int dim, int iterations, float scale, int maxdist)
{
	int x, y;
	int x1, x2, y1, y2;
	int nx, ny;
	float h;
	for (int i = 0; i < iterations; i++)
	{
		x = genrand() * dim;
		y = genrand() * dim;
		for (int c = 0; c < maxdist; c++)
		{
			x1 = (x - 1 + dim) % dim;
			x2 = (x + 1) % dim;
			y1 = (y - 1 + dim) % dim;
			y2 = (y + 1) % dim;
			h = out[x * dim + y];
			if (h > out[x1 * dim + y1])
			{
				h = out[x1 * dim + y1];
				nx = x1;
				ny = y1;
			}
			if (h > out[x1 * dim + y])
			{
				h = out[x1 * dim + y];
				nx = x1;
				ny = y;
			}
			if (h > out[x1 * dim + y2])
			{
				h = out[x1 * dim + y2];
				nx = x1;
				ny = y2;
			}
			if (h > out[x * dim + y1])
			{
				h = out[x * dim + y1];
				nx = x;
				ny = y1;
			}
			if (h > out[x * dim + y2])
			{
				h = out[x * dim + y2];
				nx = x;
				ny = y2;
			}
			if (h > out[x2 * dim + y1])
			{
				h = out[x2 * dim + y1];
				nx = x2;
				ny = y1;
			}
			if (h > out[x2 * dim + y])
			{
				h = out[x2 * dim + y];
				nx = x2;
				ny = y;
			}
			if (h > out[x2 * dim + y2])
			{
				h = out[x2 * dim + y2];
				nx = x2;
				ny = y2;
			}
			if (x == nx && y == ny) // local minimum
			{
				out[x * dim + y] += scale;
				break;
			}
			x = nx;
			y = ny;
		}
	}
}

void NoiseFFT(float *out, int dim, float scale, float h)
{
	float *workarea1, *workarea3;
	int *workarea2;
	workarea1 = new float [dim * 8];
	workarea2 = new int [2 + (int)sqrt(dim + .5)];
	workarea2[0] = 0;
	workarea3 = new float [dim / 2];

	float phase, rad, rcos, rsin;
	float dim2 = dim / 2.0f;
	float x2, y2;

	float **rh;
	rh = new float * [dim];
	for (int n = 0; n < dim; n++)
		rh[n] = new float [dim * 2];
	for (int x = 0; x < dim; x++)
	{
		for (int y = 0; y < dim / 2; y++)
		{
			phase = TWOPI * genrand();
			x2 = (x - dim2);
			y2 = (y - dim2);
			rad = pow(x2 * x2 + y2 * y2, -(h + 1) * .5f);// * gaussian();
			rcos = rad * cos(phase) * scale;
			rsin = rad * sin(phase) * scale;
			rh[x][y * 2 + 0] = rcos;
			rh[x][y * 2 + 1] = rsin;
			rh[x][(dim - y - 1) * 2 + 0] = rcos;
			rh[x][(dim - y - 1) * 2 + 1] = -rsin;
		}
	}

	cdft2d(dim, dim * 2, -1, rh, workarea1, workarea2, workarea3);

	for (int x = 0; x < dim; x++)
	{
		for (int y = 0; y < dim; y++)
		{
			if ((x + y) % 2 == 0)
				out[x * dim + y] = rh[x][y * 2 + 0];
			else
				out[x * dim + y] = -rh[x][y * 2 + 0];
		}
	}

	for (int n = 0; n < dim; n++)
		delete [] rh[n];
	delete [] rh;

	delete [] workarea1;
	delete [] workarea2;
	delete [] workarea3;
}

float DiamondSquareExpand(float *in, int indim, float *out, int outdim, float persistence, float scale)
{
//	memset(out, 0, sizeof(float) * outdim * outdim);

	int stride = (outdim - 1) / (indim - 1);
	int h1, h2, w1, w2;

	for (int h = 0; h < indim; h++)
	{
		for (int w = 0; w < indim; w++)
		{
			out[h * stride * outdim + w * stride] = in[h * indim + w];
		}
	}
	stride /= 2;

	while (stride)
	{
		for (int h = stride; h < outdim - 1; h += stride)
		{
			h1 = h - stride;
			h2 = h + stride;
			for (int w = stride; w < outdim - 1; w += stride)
			{
				w1 = w - stride;
				w2 = w + stride;

				out[h * outdim + w] = scale * (genrand() - .5f) + .25f * (out[h1 * outdim + w1] + out[h1 * outdim + w2] + out[h2 * outdim + w1] + out[h2 * outdim + w2]);

				w += stride;
			}
			h += stride;
		}

		int odd = 0;
		for (int h = 0; h < outdim - 1; h += stride)
		{
			if (h == 0)
				h1 = outdim - 1 - stride;
			else
				h1 = h - stride;
			if (h == outdim - 1)
				h2 = stride;
			else
				h2 = h + stride;

			odd = (odd == 0);
			for (int w = 0; w < outdim - 1; w += stride)
			{
				if (odd && !w)
					w += stride;

				if (w == 0)
					w1 = outdim - 1 - stride;
				else
					w1 = w - stride;
				if (w == outdim - 1)
					w2 = stride;
				else
					w2 = w + stride;

				out[h * outdim + w] = scale * (genrand() - .5f) + .25f * (out[h1 * outdim + w] + out[h2 * outdim + w] + out[h * outdim + w1] + out[h * outdim + w2]);

				// wrap edges
				if (h == 0)
					out[(outdim - 1) * outdim + w] = out[h * outdim + w];
				if (w == 0)
					out[h * outdim + outdim - 1] = out[h * outdim + w];

				w += stride;
			}
		}

		stride /= 2;
		scale *= persistence;
	}

	return scale;
}

// power of 2 + 1
float DiamondSquare(float *height, int dim, float persistence, float scale)
{
//	memset(out, 0, sizeof(float) * outdim * outdim);

	height[0] = .5f;
	height[dim - 1] = .5f;
	height[(dim - 1) * dim] = .5f;
	height[(dim - 1) * dim + dim - 1] = .5f;
	int stride = dim / 2;
	int h1, h2, w1, w2;
	while (stride)
	{
		for (int h = stride; h < dim - 1; h += stride)
		{
			h1 = h - stride;
			h2 = h + stride;
			for (int w = stride; w < dim - 1; w += stride)
			{
				w1 = w - stride;
				w2 = w + stride;

				height[h * dim + w] = scale * (genrand() - .5f) + .25f * (height[h1 * dim + w1] + height[h1 * dim + w2] + height[h2 * dim + w1] + height[h2 * dim + w2]);

				w += stride;
			}
			h += stride;
		}

		int odd = 0;
		for (int h = 0; h < dim - 1; h += stride)
		{
			if (h == 0)
				h1 = dim - 1 - stride;
			else
				h1 = h - stride;
			if (h == dim - 1)
				h2 = stride;
			else
				h2 = h + stride;

			odd = (odd == 0);
			for (int w = 0; w < dim - 1; w += stride)
			{
				if (odd && !w)
					w += stride;

				if (w == 0)
					w1 = dim - 1 - stride;
				else
					w1 = w - stride;
				if (w == dim - 1)
					w2 = stride;
				else
					w2 = w + stride;

				height[h * dim + w] = scale * (genrand() - .5f) + .25f * (height[h1 * dim + w] + height[h2 * dim + w] + height[h * dim + w1] + height[h * dim + w2]);

				// wrap edges
				if (h == 0)
					height[(dim - 1) * dim + w] = height[h * dim + w];
				if (w == 0)
					height[h * dim + dim - 1] = height[h * dim + w];

				w += stride;
			}
		}

		stride /= 2;
		scale *= persistence;
	}

	return scale;
}

// power of 2
float DiamondSquare2(float *height, int dim, float persistence, float scale)
{
//	memset(height, 0, sizeof(float) * dim * dim);
	height[0] = .5f;
	height[dim - 1] = .5f;
	height[(dim - 1) * dim] = .5f;
	height[(dim - 1) * dim + dim - 1] = .5f;
	int stride = dim / 2;
	int h1, h2, w1, w2;
	while (stride)
	{
		for (int h = stride; h < dim; h += stride)
		{
			h1 = (h - stride + dim) % dim;
			h2 = (h + stride) % dim;
			for (int w = stride; w < dim; w += stride)
			{
				w1 = (w - stride + dim) % dim;
				w2 = (w + stride) % dim;
				height[h * dim + w] = scale * (genrand() - .5f) + .25f * (height[h1 * dim + w1] + height[h1 * dim + w2] + height[h2 * dim + w1] + height[h2 * dim + w2]);
				w += stride;
			}
			h += stride;
		}

		int odd = 0;
		for (int h = 0; h < dim; h += stride)
		{
			h1 = (h - stride + dim) % dim;
			h2 = (h + stride) % dim;

			odd = (odd == 0);
			for (int w = 0; w < dim; w += stride)
			{
				if (odd && !w)
					w += stride;

				w1 = (w - stride + dim) % dim;
				w2 = (w + stride) % dim;

				height[h * dim + w] = scale * (genrand() - .5f) + .25f * (height[h1 * dim + w] + height[h2 * dim + w] + height[h * dim + w1] + height[h * dim + w2]);

				// if it needs to wrap, copy over the h == 0 and w == 0 edges to the other edges

				w += stride;
			}
		}

		stride /= 2;
		scale *= persistence;
	}

	return scale;
}

// not checking for < 0
float Perlin1D(float p, const float *grid, const int gridsize, float gridscale, float outscale, const int levels)
{
	float out = 0;

	int h1, h2;
	float hr;
	float sh;
	for (int i = 0; i < levels; i++)
	{
		h1 = (int)(p / gridscale) % gridsize;
		h2 = (h1 + 1) % gridsize;
		hr = (float)p / gridscale - (int)(p / gridscale);
		sh = hr * hr * (3 - 2 * hr);

		out += outscale * (grid[h1] * (1 - sh) + grid[h2] * sh);

		outscale *= .5f;
		gridscale *= .5;
	}


//	delete [] grid;

	return out;
}

// gridsize must be power of 2
// p must be 4 * count elements
// p, out, and grid must be 16-byte aligned
// out is added to, so clear to 0 if needed
void Perlin3DSSEArray(const float *p, float *out, const int count, const float *grid, const int gridsize, float outscale, const int levels = 1)
{
	int i, n;
	int _levels = levels;
	int _count = count;
	int gridsize2 = gridsize * gridsize;
	const float *agrid, *ap, *aout;
	ap = p;
	aout = out;
	agrid = grid;
	__declspec(align(16)) float aconstant[20], aftemp[8];
	__declspec(align(16)) int aiconstant[6];
	__declspec(align(16)) float aoutscale = outscale;
	__declspec(align(16)) float aoutscalestart = outscale;

	aconstant[0] = 1.0f;
	aconstant[1] = 1.0f;
	aconstant[2] = 1.0f;
	aconstant[3] = 1.0f;
	aconstant[4] = 0.5f;
	aconstant[5] = 0.5f;
	aconstant[6] = 0.5f;
	aconstant[7] = 0.5f;
	aconstant[8] = 2.0f;
	aconstant[9] = 2.0f;
	aconstant[10] = 2.0f;
	aconstant[11] = 2.0f;
	aconstant[12] = 3.0f;
	aconstant[13] = 3.0f;
	aconstant[14] = 3.0f;
	aconstant[15] = 3.0f;
	aconstant[16] = gridsize;
	aconstant[17] = gridsize;
	aconstant[18] = gridsize;
	aconstant[19] = gridsize;

	aiconstant[0] = 1;
	aiconstant[1] = 1;
	aiconstant[2] = gridsize - 1;
	aiconstant[3] = gridsize - 1;
	aiconstant[4] = gridsize2;
	aiconstant[5] = gridsize;

	/*float v[3];
	v[0] = (p[0] + 1.0f) * .5f;
	v[1] = (p[1] + 1.0f) * .5f;
	v[2] = (p[2] + 1.0f) * .5f;

	int gridsize2 = gridsize * gridsize;

	int h1, h2, w1, w2, d1, d2;
	float hr, wr, dr;
	float sh, sw, sd;
	for (int i = 0; i < levels; i++)
	{
		h1 = fmod(v[0], 1.0f) * gridsize;
		h2 = (h1 + 1) % gridsize;
		hr = fmod(v[0], 1.0f) * gridsize - h1;
		sh = hr * hr * (3 - 2 * hr);

		w1 = fmod(v[1], 1.0f) * gridsize;
		w2 = (w1 + 1) % gridsize;
		wr = fmod(v[1], 1.0f) * gridsize - w1;
		sw = wr * wr * (3 - 2 * wr);

		d1 = fmod(v[2], 1.0f) * gridsize;
		d2 = (d1 + 1) % gridsize;
		dr = fmod(v[2], 1.0f) * gridsize - d1;
		sd = dr * dr * (3 - 2 * dr);

		out += outscale * (
						((grid[h1 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
						+ (grid[h1 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * (1 - sh)
						+ ((grid[h2 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
						+ (grid[h2 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * sh
						);

		outscale *= .5f;
		v[0] *= 2.0f;
		v[1] *= 2.0f;
		v[2] *= 2.0f;
	}*/


	__asm
	{
		PUSHA
	}

	/*_asm
	{
		RDTSC
		MOV t1, eax
	}*/

	__asm
	{
		MOV n, 0
perlin3dsse_l2:
		MOVAPS xmm7, aconstant		// 1
		MOV eax, ap
		MOV ebx, n
		IMUL ebx, 16
		MOVAPS xmm0, [eax + ebx]
		MOVAPS xmm6, aconstant + 16	// .5
		MOV edi, agrid
		ADDPS xmm0, xmm7
		MOVAPS xmm5, aconstant + 32 // 2
		MULPS xmm0, xmm6			// v = (p + 1) * .5
		MOVQ mm7, aiconstant		// 1
		MOVQ mm6, aiconstant + 8	// gridsize - 1
		MOVQ mm5, aiconstant + 16	// gridsize2, gridsize

		MOV eax, aoutscalestart
		MOV aoutscale, eax

		//XOR eax, eax				// i = 0
		MOV i, 0
perlin3dsse_l1:
		MOVAPS xmm3, aconstant + 48	// 3
		MOVAPS xmm4, aconstant + 64 // gridsize
		MOVAPS xmm7, aconstant		// 1

		// clamp to [0, 1) (assuming original value is [0, 1) multiplied by 2)
		MOVAPS xmm1, xmm0
		CMPPS xmm1, xmm7, 0x5		// not less than 1
		ANDPS xmm1, xmm7
		SUBPS xmm0, xmm1			// subtract 1 if greater than 1
		// scale by gridsize
		MOVAPS xmm1, xmm0
		MULPS xmm1, xmm4

		// truncate to h1 (store in two mmx registers)
		MOVHLPS xmm2, xmm1
		CVTTPS2PI mm0, xmm1
		CVTTPS2PI mm1, xmm2
		// add 1 to get h2
		PSHUFW mm2, mm0, 0xE4
//		PADDD mm2, mm7
//		PSHUFW mm3, mm1, 0xE4
//		PAND mm2, mm6				// mod gridsize
//		PADDD mm3, mm7
//		PAND mm3, mm6				// mod gridsize

		// load truncated (h1)
		CVTPI2PS xmm2, mm1
		PADDD mm2, mm7
		MOVLHPS xmm2, xmm2
		PSHUFW mm3, mm1, 0xE4
		CVTPI2PS xmm2, mm0
		PAND mm2, mm6				// mod gridsize
		// get fraction
		SUBPS xmm1, xmm2
		PADDD mm3, mm7
		// interpolant value (hr * hr * (3 - 2 * hr))
		MOVAPS xmm2, xmm1
		PAND mm3, mm6				// mod gridsize
		MULPS xmm1, xmm1
		PMULLW mm0, mm5				// scale by gridsize2 and gridsize
		MULPS xmm2, xmm5
		PMULLW mm2, mm5				// scale by gridsize2 and gridsize
		SUBPS xmm3, xmm2
		MOVD ebx, mm0
		PSHUFW mm0, mm0, 0x4E		// swap dwords
		MOVAPS xmm2, xmm7			// 1
		MOVD ecx, mm0
		MULPS xmm1, xmm3
		MOVD edx, mm1
		SUBPS xmm2, xmm1			// 1 - interpolant

		/*out += outscale * (
			((grid[h1 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
			+ (grid[h1 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * (1 - sh)
			+ ((grid[h2 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
			+ (grid[h2 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * sh
			);*/

		// get indices
//		PMULLW mm0, mm5				// scale by gridsize2 and gridsize
//		PMULLW mm2, mm5				// scale by gridsize2 and gridsize

//		MOVD ebx, mm0
//		PSHUFW mm0, mm0, 0x4E		// swap dwords
//		MOVD ecx, mm0
//		MOVD edx, mm1

		// h1, w1, d1
		LEA eax, [ebx + ecx]
		ADD eax, edx
		MOV eax, [edi + eax * 4]
		MOV aftemp, eax

		MOVD esi, mm3
		// h1, w1, d2
		LEA eax, [ebx + ecx]
		ADD eax, esi
		MOV eax, [edi + eax * 4]
		MOV aftemp + 16, eax

		PSHUFW mm2, mm2, 0x4E		// swap dwords
		MOVD ecx, mm2
		// h1, w2, d2
		LEA eax, [ebx + ecx]
		ADD eax, esi
		MOV eax, [edi + eax * 4]
		MOV aftemp + 20, eax

		// h1, w2, d1
		LEA eax, [ebx + ecx]
		ADD eax, edx
		MOV eax, [edi + eax * 4]
		MOV aftemp + 4, eax

		PSHUFW mm2, mm2, 0x4E		// swap dwords
		MOVD ebx, mm2
		// h2, w2, d1
		LEA eax, [ebx + ecx]
		ADD eax, edx
		MOV eax, [edi + eax * 4]
		MOV aftemp + 12, eax

		// h2, w2, d2
		LEA eax, [ebx + ecx]
		ADD eax, esi
		MOV eax, [edi + eax * 4]
		MOV aftemp + 28, eax

		MOVD ecx, mm0
		// h2, w1, d2
		LEA eax, [ebx + ecx]
		ADD eax, esi
		MOV eax, [edi + eax * 4]
		MOV aftemp + 24, eax

		// h2, w1, d1
		LEA eax, [ebx + ecx]
		ADD eax, edx
		MOV eax, [edi + eax * 4]
		MOV aftemp + 8, eax

		/*out += outscale * (
			((grid[h1 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
			+ (grid[h1 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * (1 - sh)
			+ ((grid[h2 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
			+ (grid[h2 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * sh
			);*/

		// xmm1 = interpolant, xmm2 = 1 - interpolant
		// put together...
		MOVAPS xmm3, aftemp
		MOVAPS xmm4, aftemp + 16

		// (1-sd) + sd
		SHUFPS xmm5, xmm2, 0xA0			// replicate 1 (from 3rd position)
		MOVHLPS xmm5, xmm5				// replicate 2
		MULPS xmm3, xmm5
		SUBPS xmm7, xmm5
		MULPS xmm4, xmm7
		ADDPS xmm3, xmm4

		// interleave 1 - sw, sw
		SHUFPS xmm4, xmm2, 0x50
		SHUFPS xmm5, xmm1, 0x50
		UNPCKHPS xmm4, xmm5
		MULPS xmm3, xmm4

		// add 1,2 and 3,4
		MOVAPS xmm4, xmm3
		SHUFPS xmm4, xmm4, 0xB1
		ADDPS xmm3, xmm4
		MOVHLPS xmm4, xmm3
		// 1-sh, sh
		MULSS xmm3, xmm2
		MULSS xmm4, xmm1
		// add
		ADDSS xmm3, xmm4
		// scale
		MULSS xmm3, aoutscale
		MOV eax, n
		MOV ebx, aout
		// store
		ADDSS xmm3, [ebx + eax * 4]
		MOVSS [ebx + eax * 4], xmm3


		/*outscale *= .5f;
		v[0] *= 2.0f;
		v[1] *= 2.0f;
		v[2] *= 2.0f;*/
		MOVSS xmm1, aoutscale
		MOVAPS xmm5, aconstant + 32 // 2
		MULSS xmm1, xmm6
		MOVSS aoutscale, xmm1
		MULPS xmm0, xmm5



		MOV eax, i
		ADD eax, 1					// loop i
		CMP eax, _levels
		MOV i, eax
		JNZ perlin3dsse_l1


		MOV eax, n
		ADD eax, 1					// loop n
		CMP eax, _count
		MOV n, eax
		JNZ perlin3dsse_l2
	}


	/*_asm
	{
		RDTSC
		MOV t2, eax
	}
	// timing takes 5 cycles
	if (t2 - t1 < p3d_time)
		p3d_time = t2 - t1;*/

	__asm
	{
		POPA
		EMMS
	}
}

// gridsize must be power of 2
float Perlin3DSSE(const float *p, const float *grid, const int gridsize, float outscale, const int levels = 1)
{
	int i;
	int _levels = levels;
	int gridsize2 = gridsize * gridsize;
	float *agrid;
	//ap = (float*)_aligned_malloc(sizeof(float) * 4, 16);
	//aconstant = (float*)_aligned_malloc(sizeof(float) * 16, 16);
	__declspec(align(16)) float ap[4], aconstant[20], aftemp[8];
	__declspec(align(16)) int aiconstant[6];
	__declspec(align(16)) float aoutscale = outscale;
	agrid = (float*)_aligned_malloc(sizeof(float) * gridsize * gridsize * gridsize, 16);

	memcpy(agrid, grid, sizeof(float) * gridsize * gridsize * gridsize);

	ap[0] = p[0];
	ap[1] = p[1];
	ap[2] = p[2];
	ap[3] = 0;

	aconstant[0] = 1.0f;
	aconstant[1] = 1.0f;
	aconstant[2] = 1.0f;
	aconstant[3] = 1.0f;
	aconstant[4] = 0.5f;
	aconstant[5] = 0.5f;
	aconstant[6] = 0.5f;
	aconstant[7] = 0.5f;
	aconstant[8] = 2.0f;
	aconstant[9] = 2.0f;
	aconstant[10] = 2.0f;
	aconstant[11] = 2.0f;
	aconstant[12] = 3.0f;
	aconstant[13] = 3.0f;
	aconstant[14] = 3.0f;
	aconstant[15] = 3.0f;
	aconstant[16] = gridsize;
	aconstant[17] = gridsize;
	aconstant[18] = gridsize;
	aconstant[19] = gridsize;

	aiconstant[0] = 1;
	aiconstant[1] = 1;
	aiconstant[2] = gridsize - 1;
	aiconstant[3] = gridsize - 1;
	aiconstant[4] = gridsize2;
	aiconstant[5] = gridsize;

	__declspec(align(16)) float aout = 0;

	/*float v[3];
	v[0] = (p[0] + 1.0f) * .5f;
	v[1] = (p[1] + 1.0f) * .5f;
	v[2] = (p[2] + 1.0f) * .5f;

	int gridsize2 = gridsize * gridsize;

	int h1, h2, w1, w2, d1, d2;
	float hr, wr, dr;
	float sh, sw, sd;
	for (int i = 0; i < levels; i++)
	{
		h1 = fmod(v[0], 1.0f) * gridsize;
		h2 = (h1 + 1) % gridsize;
		hr = fmod(v[0], 1.0f) * gridsize - h1;
		sh = hr * hr * (3 - 2 * hr);

		w1 = fmod(v[1], 1.0f) * gridsize;
		w2 = (w1 + 1) % gridsize;
		wr = fmod(v[1], 1.0f) * gridsize - w1;
		sw = wr * wr * (3 - 2 * wr);

		d1 = fmod(v[2], 1.0f) * gridsize;
		d2 = (d1 + 1) % gridsize;
		dr = fmod(v[2], 1.0f) * gridsize - d1;
		sd = dr * dr * (3 - 2 * dr);

		out += outscale * (
						((grid[h1 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
						+ (grid[h1 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * (1 - sh)
						+ ((grid[h2 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
						+ (grid[h2 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * sh
						);

		outscale *= .5f;
		v[0] *= 2.0f;
		v[1] *= 2.0f;
		v[2] *= 2.0f;
	}*/


	__asm
	{
		PUSHA
	}

	_asm
	{
		RDTSC
		MOV t1, eax
	}

	__asm
	{
		MOVAPS xmm7, aconstant		// 1
		MOVAPS xmm0, ap
		MOVAPS xmm6, aconstant + 16	// .5
		MOV edi, agrid
		ADDPS xmm0, xmm7
		MOVAPS xmm5, aconstant + 32 // 2
		MULPS xmm0, xmm6			// v = (p + 1) * .5
		MOVQ mm7, aiconstant		// 1
		MOVQ mm6, aiconstant + 8	// gridsize - 1
		MOVQ mm5, aiconstant + 16	// gridsize2, gridsize

		//XOR eax, eax				// i = 0
		MOV i, 0
perlin3dsse_l1:
		MOVAPS xmm3, aconstant + 48	// 3
		MOVAPS xmm4, aconstant + 64 // gridsize
		MOVAPS xmm7, aconstant		// 1

		// clamp to [0, 1) (assuming original value is [0, 1) multiplied by 2)
		MOVAPS xmm1, xmm0
		CMPPS xmm1, xmm7, 0x5		// not less than 1
		ANDPS xmm1, xmm7
		SUBPS xmm0, xmm1			// subtract 1 if greater than 1
		// scale by gridsize
		MOVAPS xmm1, xmm0
		MULPS xmm1, xmm4

		// truncate to h1 (store in two mmx registers)
		MOVHLPS xmm2, xmm1
		CVTTPS2PI mm0, xmm1
		CVTTPS2PI mm1, xmm2
		// add 1 to get h2
		PSHUFW mm2, mm0, 0xE4
//		PADDD mm2, mm7
//		PSHUFW mm3, mm1, 0xE4
//		PAND mm2, mm6				// mod gridsize
//		PADDD mm3, mm7
//		PAND mm3, mm6				// mod gridsize

		// load truncated (h1)
		CVTPI2PS xmm2, mm1
		PADDD mm2, mm7
		MOVLHPS xmm2, xmm2
		PSHUFW mm3, mm1, 0xE4
		CVTPI2PS xmm2, mm0
		PAND mm2, mm6				// mod gridsize
		// get fraction
		SUBPS xmm1, xmm2
		PADDD mm3, mm7
		// interpolant value (hr * hr * (3 - 2 * hr))
		MOVAPS xmm2, xmm1
		PAND mm3, mm6				// mod gridsize
		MULPS xmm1, xmm1
		PMULLW mm0, mm5				// scale by gridsize2 and gridsize
		MULPS xmm2, xmm5
		PMULLW mm2, mm5				// scale by gridsize2 and gridsize
		SUBPS xmm3, xmm2
		MOVD ebx, mm0
		PSHUFW mm0, mm0, 0x4E		// swap dwords
		MOVAPS xmm2, xmm7			// 1
		MOVD ecx, mm0
		MULPS xmm1, xmm3
		MOVD edx, mm1
		SUBPS xmm2, xmm1			// 1 - interpolant

		/*out += outscale * (
			((grid[h1 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
			+ (grid[h1 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * (1 - sh)
			+ ((grid[h2 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
			+ (grid[h2 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * sh
			);*/

		// get indices
//		PMULLW mm0, mm5				// scale by gridsize2 and gridsize
//		PMULLW mm2, mm5				// scale by gridsize2 and gridsize

//		MOVD ebx, mm0
//		PSHUFW mm0, mm0, 0x4E		// swap dwords
//		MOVD ecx, mm0
//		MOVD edx, mm1

		// h1, w1, d1
		LEA eax, [ebx + ecx]
		ADD eax, edx
		MOV eax, [edi + eax * 4]
		MOV aftemp, eax

		MOVD esi, mm3
		// h1, w1, d2
		LEA eax, [ebx + ecx]
		ADD eax, esi
		MOV eax, [edi + eax * 4]
		MOV aftemp + 16, eax

		PSHUFW mm2, mm2, 0x4E		// swap dwords
		MOVD ecx, mm2
		// h1, w2, d2
		LEA eax, [ebx + ecx]
		ADD eax, esi
		MOV eax, [edi + eax * 4]
		MOV aftemp + 20, eax

		// h1, w2, d1
		LEA eax, [ebx + ecx]
		ADD eax, edx
		MOV eax, [edi + eax * 4]
		MOV aftemp + 4, eax

		PSHUFW mm2, mm2, 0x4E		// swap dwords
		MOVD ebx, mm2
		// h2, w2, d1
		LEA eax, [ebx + ecx]
		ADD eax, edx
		MOV eax, [edi + eax * 4]
		MOV aftemp + 12, eax

		// h2, w2, d2
		LEA eax, [ebx + ecx]
		ADD eax, esi
		MOV eax, [edi + eax * 4]
		MOV aftemp + 28, eax

		MOVD ecx, mm0
		// h2, w1, d2
		LEA eax, [ebx + ecx]
		ADD eax, esi
		MOV eax, [edi + eax * 4]
		MOV aftemp + 24, eax

		// h2, w1, d1
		LEA eax, [ebx + ecx]
		ADD eax, edx
		MOV eax, [edi + eax * 4]
		MOV aftemp + 8, eax

		/*out += outscale * (
			((grid[h1 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
			+ (grid[h1 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * (1 - sh)
			+ ((grid[h2 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
			+ (grid[h2 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * sh
			);*/

		// xmm1 = interpolant, xmm2 = 1 - interpolant
		// put together...
		MOVAPS xmm3, aftemp
		MOVAPS xmm4, aftemp + 16

		// (1-sd) + sd
		SHUFPS xmm5, xmm2, 0xA0			// replicate 1 (from 3rd position)
		MOVHLPS xmm5, xmm5				// replicate 2
		MULPS xmm3, xmm5
		SUBPS xmm7, xmm5
		MULPS xmm4, xmm7
		ADDPS xmm3, xmm4

		// interleave 1 - sw, sw
		SHUFPS xmm4, xmm2, 0x50
		SHUFPS xmm5, xmm1, 0x50
		UNPCKHPS xmm4, xmm5
		MULPS xmm3, xmm4

		// add 1,2 and 3,4
		MOVAPS xmm4, xmm3
		SHUFPS xmm4, xmm4, 0xB1
		ADDPS xmm3, xmm4
		MOVHLPS xmm4, xmm3
		// 1-sh, sh
		MULSS xmm3, xmm2
		MULSS xmm4, xmm1
		// add
		ADDSS xmm3, xmm4
		// scale
		MULSS xmm3, aoutscale
		// store
		ADDSS xmm3, aout
		MOVSS aout, xmm3


		/*outscale *= .5f;
		v[0] *= 2.0f;
		v[1] *= 2.0f;
		v[2] *= 2.0f;*/
		MOVSS xmm1, aoutscale
		MOVAPS xmm5, aconstant + 32 // 2
		MULSS xmm1, xmm6
		MOVSS aoutscale, xmm1
		MULPS xmm0, xmm5



		MOV eax, i
		ADD eax, 1					// loop i
		CMP eax, _levels
		MOV i, eax
		JNZ perlin3dsse_l1
	}


	_asm
	{
		RDTSC
		MOV t2, eax
	}
	// timing takes 5 cycles
	if (t2 - t1 < p3d_time)
		p3d_time = t2 - t1;

	__asm
	{
		POPA
		EMMS
	}


	//_aligned_free(ap);
	//_aligned_free(aconstant);
	_aligned_free(agrid);

	return aout;
}

// modify to run over an array of input values (and then move the grid back inside)
float Perlin3D(const float *p, const float *grid, const int gridsize, float outscale, const int levels = 1)
{
	_asm
	{
		RDTSC
		MOV t1, eax
	}


	float out = 0;

	float v[3];
	v[0] = (p[0] + 1.0f) * .5f;
//	v[0] = fmod(v[0], 1.0f);
	v[1] = (p[1] + 1.0f) * .5f;
//	v[1] = fmod(v[1], 1.0f);
	v[2] = (p[2] + 1.0f) * .5f;
//	v[2] = fmod(v[2], 1.0f);

/*	if (v[0] < -.0001f)
		v[0] += 1.0f;
	if (v[1] < -.0001f)
		v[1] += 1.0f;
	if (v[2] < -.0001f)
		v[2] += 1.0f;*/

	int gridsize2 = gridsize * gridsize;

	int h1, h2, w1, w2, d1, d2;
	float hr, wr, dr;
	float sh, sw, sd;
	for (int i = 0; i < levels; i++)
	{
		h1 = fmod(v[0], 1.0f) * gridsize;
		h2 = (h1 + 1) % gridsize;
		hr = fmod(v[0], 1.0f) * gridsize - h1;
		sh = hr * hr * (3 - 2 * hr);

		w1 = fmod(v[1], 1.0f) * gridsize;
		w2 = (w1 + 1) % gridsize;
		wr = fmod(v[1], 1.0f) * gridsize - w1;
		sw = wr * wr * (3 - 2 * wr);

		d1 = fmod(v[2], 1.0f) * gridsize;
		d2 = (d1 + 1) % gridsize;
		dr = fmod(v[2], 1.0f) * gridsize - d1;
		sd = dr * dr * (3 - 2 * dr);


		out += outscale * (
						((grid[h1 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
						+ (grid[h1 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * (1 - sh)
						+ ((grid[h2 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
						+ (grid[h2 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * sh
						);


		outscale *= .5f;
		v[0] *= 2.0f;
		v[1] *= 2.0f;
		v[2] *= 2.0f;
	}


	_asm
	{
		RDTSC
		MOV t2, eax
	}
	// timing takes 5 cycles
	if (t2 - t1 < p3d_time)
		p3d_time = t2 - t1;


	return out;
}

// 0-1 input
float Perlin3D2(const float *p, const float *grid, const int gridsize, float outscale, const int levels = 1)
{
	float out = 0;

	float v[3];
	v[0] = p[0];
	v[1] = p[1];
	v[2] = p[2];

	int gridsize2 = gridsize * gridsize;

	int h1, h2, w1, w2, d1, d2;
	float hr, wr, dr;
	float sh, sw, sd;
	for (int i = 0; i < levels; i++)
	{
		h1 = fmod(v[0], 1.0f) * gridsize;
		h2 = (h1 + 1) % gridsize;
		hr = fmod(v[0], 1.0f) * gridsize - h1;
		sh = hr * hr * (3 - 2 * hr);

		w1 = fmod(v[1], 1.0f) * gridsize;
		w2 = (w1 + 1) % gridsize;
		wr = fmod(v[1], 1.0f) * gridsize - w1;
		sw = wr * wr * (3 - 2 * wr);

		d1 = fmod(v[2], 1.0f) * gridsize;
		d2 = (d1 + 1) % gridsize;
		dr = fmod(v[2], 1.0f) * gridsize - d1;
		sd = dr * dr * (3 - 2 * dr);


		out += outscale * (
						((grid[h1 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
						+ (grid[h1 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h1 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * (1 - sh)
						+ ((grid[h2 * gridsize2 + w1 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w1 * gridsize + d2] * sd) * (1 - sw)
						+ (grid[h2 * gridsize2 + w2 * gridsize + d1] * (1 - sd) + grid[h2 * gridsize2 + w2 * gridsize + d2] * sd) * sw) * sh
						);


		outscale *= .5f;
		v[0] *= 2.0f;
		v[1] *= 2.0f;
		v[2] *= 2.0f;
	}

	return out;
}

float PerlinBicubic(float *out, int outdim, int gridsize, int levels = 1, float turbulence = 0)
{
	memset(out, 0, sizeof(float) * outdim * outdim);

	if (outdim / powf(2, levels) < 1)
	{
		levels = GetBitIndex(outdim);
	}

	float levelsum = 0;
	for (int n = 1; n <= levels; n++)
	{
		levelsum += 1 / pow(2.0f, n - 1);
	}

	float outscale = 1 / levelsum;

	float *upsampled = new float [outdim * outdim];

	float turbulencescale;
	if (turbulence < .5f)
		turbulencescale = 1.0f / (1 - turbulence);
	else
		turbulencescale = 1.0f / turbulence;

	for (int i = 0; i < levels; i++)
	{
		float *grid;
		grid = new float [gridsize * gridsize];

		for (int n = 0; n < gridsize * gridsize; n++)
		{
			grid[n] = genrand();
		}

		BicubicFloat(grid, upsampled, gridsize, gridsize, outdim, outdim);
		for (int n = 0; n < outdim * outdim; n++)
		{
			out[n] += outscale * fabs(upsampled[n] - turbulence) * turbulencescale;
		}

		outscale *= .5f;

		delete [] grid;
		gridsize *= 2;
	}

	delete [] upsampled;

	return outscale;
}

// new grid each level
float Perlin2(float *out, int outdim, int gridsize, int levels = 1)
{
	memset(out, 0, sizeof(float) * outdim * outdim);

	if (outdim / powf(2, levels) < 1)
	{
		levels = GetBitIndex(outdim);
	}

	float levelsum = 0;
	for (int n = 1; n <= levels; n++)
	{
		levelsum += 1 / pow(2.0f, n - 1);
	}

	float outscale = 1 / levelsum;

	float scale = (float)outdim / gridsize;
	int h1, h2, w1, w2;
	float hr, wr;
	float sh, sw;
	for (int i = 0; i < levels; i++)
	{
		float *grid;
		grid = new float [gridsize * gridsize];

		for (int n = 0; n < gridsize * gridsize; n++)
		{
			grid[n] = genrand();
		}

		if (scale <= 1)
		{
			for (int h = 0; h < outdim; h++)
			{
				h1 = h % gridsize;
				for (int w = 0; w < outdim; w++)
				{
					w1 = w % gridsize;
					out[h * outdim + w] += grid[h1 * gridsize + w1] * outscale;
				}
			}
		}
		else
		{
			for (int h = 0; h < outdim; h++)
			{
				h1 = (int)(h / scale) % gridsize;
				h2 = (h1 + 1) % gridsize;
				hr = (float)h / scale - (int)(h / scale);
				sh = hr * hr * (3 - 2 * hr);

				for (int w = 0; w < outdim; w++)
				{
					w1 = (int)(w / scale) % gridsize;
					w2 = (w1 + 1) % gridsize;
					wr = (float)w / scale - (int)(w / scale);
					sw = wr * wr * (3 - 2 * wr);

					out[h * outdim + w] += outscale * ((grid[h1 * gridsize + w1] * (1 - sw) + grid[h1 * gridsize + w2] * sw) * (1 - sh)
						+ (grid[h2 * gridsize + w1] * (1 - sw) + grid[h2 * gridsize + w2] * sw) * sh);
				}
			}
		}
		outscale *= .5f;
		scale /= 2;

		delete [] grid;
		gridsize *= 2;
	}

	return outscale;
}

// to get rid of the repeating patterns, use a different/larger grid on subsequent levels
// instead of just tiling it
float Perlin(float *out, int outdim, float *grid, int gridsize, int levels = 1)
{
	memset(out, 0, sizeof(float) * outdim * outdim);

/*	float *grid;
	grid = new float [gridsize * gridsize];

	for (int n = 0; n < gridsize * gridsize; n++)
	{
		grid[n] = genrand();
	}*/


	if (outdim / powf(2, levels) < 1)
	{
		levels = GetBitIndex(outdim);
	}

	float levelsum = 0;
	for (int n = 1; n <= levels; n++)
	{
		levelsum += 1 / pow(2.0f, n - 1);
	}

	float outscale = 1 / levelsum;

	float scale = (float)outdim / gridsize;
	int h1, h2, w1, w2;
	float hr, wr;
	float sh, sw;
	for (int i = 0; i < levels; i++)
	{
		if (scale <= 1)
		{
			for (int h = 0; h < outdim; h++)
			{
				h1 = h % gridsize;
				for (int w = 0; w < outdim; w++)
				{
					w1 = w % gridsize;
					out[h * outdim + w] += grid[h1 * gridsize + w1] * outscale;
				}
			}
		}
		else
		{
			for (int h = 0; h < outdim; h++)
			{
				h1 = (int)(h / scale) % gridsize;
				h2 = (h1 + 1) % gridsize;
				hr = (float)h / scale - (int)(h / scale);
				sh = hr * hr * (3 - 2 * hr);

				for (int w = 0; w < outdim; w++)
				{
					w1 = (int)(w / scale) % gridsize;
					w2 = (w1 + 1) % gridsize;
					wr = (float)w / scale - (int)(w / scale);
					sw = wr * wr * (3 - 2 * wr);

					out[h * outdim + w] += outscale * ((grid[h1 * gridsize + w1] * (1 - sw) + grid[h1 * gridsize + w2] * sw) * (1 - sh)
						+ (grid[h2 * gridsize + w1] * (1 - sw) + grid[h2 * gridsize + w2] * sw) * sh);
				}
			}
		}
		outscale *= .5f;
		scale /= 2;
	}


//	delete [] grid;

	return outscale;
}

float Perlin2D(const float x, const float y, const float *grid, const int gridsize, float outscale, const int levels = 1)
{
	float out = 0;

	float x2, y2;
	x2 = (x + 1.0f) * .5f;
	y2 = (y + 1.0f) * .5f;

	int h1, h2, w1, w2;
	float hr, wr;
	float sh, sw;
	for (int i = 0; i < levels; i++)
	{
		h1 = fmod(x2, 1.0f) * gridsize;
		h2 = (h1 + 1) % gridsize;
		hr = fmod(x2, 1.0f) * gridsize - h1;
		sh = hr * hr * (3 - 2 * hr);

		w1 = fmod(y2, 1.0f) * gridsize;
		w2 = (w1 + 1) % gridsize;
		wr = fmod(y2, 1.0f) * gridsize - w1;
		sw = wr * wr * (3 - 2 * wr);

		out += outscale * (
						(grid[h1 * gridsize + w1] * (1 - sw) + grid[h1 * gridsize + w2] * sw) * (1 - sh)
						+ (grid[h2 * gridsize + w1] * (1 - sw) + grid[h2 * gridsize + w2] * sw) * sh
						);


		outscale *= .5f;
		x2 *= 2.0f;
		y2 *= 2.0f;
	}

	return out;
}

// 3 component nearest sample on a 4 component buffer
void Nearest3x4(unsigned char *in, unsigned char *out, int inx, int iny, int outx, int outy)
{
	int xi, yi;
	float scalex, scaley;
	float invscalex, invscaley;
	scalex = (float)outx / inx;
	scaley = (float)outy / iny;
	invscalex = 1.0f / scalex;
	invscaley = 1.0f / scaley;
	for (int x = 0; x < outx; x++)
	{
		xi = x * invscalex;

		for (int y = 0; y < outy; y++)
		{
			yi = y * invscaley;

            out[(x * outy + y) * 4 + 0] = in[(xi * iny + yi) * 4 + 0];
			out[(x * outy + y) * 4 + 1] = in[(xi * iny + yi) * 4 + 1];
			out[(x * outy + y) * 4 + 2] = in[(xi * iny + yi) * 4 + 2];
		}
	}
}

// 3 component interpolation on a 4 component buffer
void Bilinear3x4(unsigned char *in, unsigned char *out, int inx, int iny, int outx, int outy)
{
	int xi, yi;
	int xi2, yi2;
	float xr, yr;
	float scalex, scaley;
	float invscalex, invscaley;
	scalex = (float)outx / inx;
	scaley = (float)outy / iny;
	invscalex = 1.0f / scalex;
	invscaley = 1.0f / scaley;
	for (int x = 0; x < outx; x++)
	{
		xi = x * invscalex;
		xr = (float)x * invscalex - xi;

		xi2 = xi + 1;
		if (xi2 >= inx)
			xi2 -= inx;

		for (int y = 0; y < outy; y++)
		{
			yi = y * invscaley;
			yr = (float)y * invscaley - yi;

			yi2 = yi + 1;
			if (yi2 >= iny)
				yi2 -= iny;

            out[(x * outy + y) * 4 + 0] = (in[(xi * iny + yi) * 4 + 0] * (1 - yr) + in[(xi * iny + yi2) * 4 + 0] * yr) * (1 - xr)
										+ (in[(xi2 * iny + yi) * 4 + 0] * (1 - yr) + in[(xi2 * iny + yi2) * 4 + 0] * yr) * xr;
			out[(x * outy + y) * 4 + 1] = (in[(xi * iny + yi) * 4 + 1] * (1 - yr) + in[(xi * iny + yi2) * 4 + 1] * yr) * (1 - xr)
										+ (in[(xi2 * iny + yi) * 4 + 1] * (1 - yr) + in[(xi2 * iny + yi2) * 4 + 1] * yr) * xr;
			out[(x * outy + y) * 4 + 2] = (in[(xi * iny + yi) * 4 + 2] * (1 - yr) + in[(xi * iny + yi2) * 4 + 2] * yr) * (1 - xr)
										+ (in[(xi2 * iny + yi) * 4 + 2] * (1 - yr) + in[(xi2 * iny + yi2) * 4 + 2] * yr) * xr;
		}
	}
}

void BilinearFloat(float *in, float *out, int inx, int iny, int outx, int outy)
{
	int xi, yi;
	int xi2, yi2;
	float xr, yr;
	float invscalex, invscaley;
	invscalex = (float)inx / outx;
	invscaley = (float)iny / outy;
	for (int x = 0; x < outx; x++)
	{
		xi = x * invscalex;
		xr = (float)x * invscalex - xi;

		xi2 = xi + 1;
		if (xi2 >= inx)
			xi2 -= inx;

		for (int y = 0; y < outy; y++)
		{
			yi = y * invscaley;
			yr = (float)y * invscaley - yi;

			yi2 = yi + 1;
			if (yi2 >= iny)
				yi2 -= iny;

			out[x * outy + y] = (in[xi * iny + yi] * (1.0f - yr) + in[xi * iny + yi2] * yr) * (1.0f - xr)
				+ (in[xi2 * iny + yi] * (1.0f - yr) + in[xi2 * iny + yi2] * yr) * xr;
		}
	}
}

void Bicubic4(unsigned char *in, unsigned char *out, int inx, int iny, int outx, int outy)
{
	float tx2, tx3, tx4;
	float ty2, ty3, ty4;
	float x1, x2, x3, x4;
	float y1, y2, y3, y4;
	float xr, yr;
	float w[16];
	int xi, yi;
	int xi1, xi3, xi4;
	int yi1, yi3, yi4;
	float scalex, scaley;
	float invscalex, invscaley;
	float sum1, sum2, sum3, sum4;
	scalex = (float)outx / inx;
	scaley = (float)outy / iny;
	invscalex = 1.0f / scalex;
	invscaley = 1.0f / scaley;
	for (int x = 0; x < outx; x++)
	{
		xi = x * invscalex;
		xi1 = xi - 1;
		if (xi1 < 0)
			xi1 += inx;
		xi3 = xi + 1;
		if (xi3 >= inx)
			xi3 -= inx;
		xi4 = xi + 2;
		if (xi4 >= inx)
			xi4 -= inx;

		xr = (float)x * invscalex - xi;


		x1 = .16666666666666666666666666666667f * (1.0f - xr) * (1.0f - xr) * (1.0f - xr);
		tx2 = .16666666666666666666666666666667f * (2.0f - xr) * (2.0f - xr) * (2.0f - xr);
		tx3 = .16666666666666666666666666666667f * (3.0f - xr) * (3.0f - xr) * (3.0f - xr);
		tx4 = .16666666666666666666666666666667f * (4.0f - xr) * (4.0f - xr) * (4.0f - xr);
		x2 = tx2
			- 4.0f * x1;
		x3 = tx3
			- 4.0f * tx2
			+ 6.0f * x1;
		x4 = tx4
			- 4.0f * tx3
			+ 6.0f * tx2
			- 4.0f * x1;

		for (int y = 0; y < outy; y++)
		{
			yi = y * invscaley;
			yi1 = yi - 1;
			if (yi1 < 0)
				yi1 += iny;
			yi3 = yi + 1;
			if (yi3 >= iny)
				yi3 -= iny;
			yi4 = yi + 2;
			if (yi4 >= iny)
				yi4 -= iny;

			yr = (float)y * invscaley - yi;


			y1 = .16666666666666666666666666666667f * (1.0f - yr) * (1.0f - yr) * (1.0f - yr);
			ty2 = .16666666666666666666666666666667f * (2.0f - yr) * (2.0f - yr) * (2.0f - yr);
			ty3 = .16666666666666666666666666666667f * (3.0f - yr) * (3.0f - yr) * (3.0f - yr);
			ty4 = .16666666666666666666666666666667f * (4.0f - yr) * (4.0f - yr) * (4.0f - yr);
			y2 = ty2
				- 4.0f * y1;
			y3 = ty3
				- 4.0f * ty2
				+ 6.0f * y1;
			y4 = ty4
				- 4.0f * ty3
				+ 6.0f * ty2
				- 4.0f * y1;

			w[0] = x1 * y1;
			w[1] = x2 * y1;
			w[2] = x3 * y1;
			w[3] = x4 * y1;
			w[4] = x1 * y2;
			w[5] = x2 * y2;
			w[6] = x3 * y2;
			w[7] = x4 * y2;
			w[8] = x1 * y3;
			w[9] = x2 * y3;
			w[10] = x3 * y3;
			w[11] = x4 * y3;
			w[12] = x1 * y4;
			w[13] = x2 * y4;
			w[14] = x3 * y4;
			w[15] = x4 * y4;
			// can reuse the bottom 12 in next for most y
			sum1 = w[0] * in[(xi1 * iny + yi1) * 4 + 0];
			sum2 = w[0] * in[(xi1 * iny + yi1) * 4 + 1];
			sum3 = w[0] * in[(xi1 * iny + yi1) * 4 + 2];
			sum4 = w[0] * in[(xi1 * iny + yi1) * 4 + 3];
			sum1 += w[1] * in[(xi * iny + yi1) * 4 + 0];
			sum2 += w[1] * in[(xi * iny + yi1) * 4 + 1];
			sum3 += w[1] * in[(xi * iny + yi1) * 4 + 2];
			sum4 += w[1] * in[(xi * iny + yi1) * 4 + 3];
			sum1 += w[2] * in[(xi3 * iny + yi1) * 4 + 0];
			sum2 += w[2] * in[(xi3 * iny + yi1) * 4 + 1];
			sum3 += w[2] * in[(xi3 * iny + yi1) * 4 + 2];
			sum4 += w[2] * in[(xi3 * iny + yi1) * 4 + 3];
			sum1 += w[3] * in[(xi4 * iny + yi1) * 4 + 0];
			sum2 += w[3] * in[(xi4 * iny + yi1) * 4 + 1];
			sum3 += w[3] * in[(xi4 * iny + yi1) * 4 + 2];
			sum4 += w[3] * in[(xi4 * iny + yi1) * 4 + 3];
			sum1 += w[4] * in[(xi1 * iny + yi) * 4 + 0];
			sum2 += w[4] * in[(xi1 * iny + yi) * 4 + 1];
			sum3 += w[4] * in[(xi1 * iny + yi) * 4 + 2];
			sum4 += w[4] * in[(xi1 * iny + yi) * 4 + 3];
			sum1 += w[5] * in[(xi * iny + yi) * 4 + 0];
			sum2 += w[5] * in[(xi * iny + yi) * 4 + 1];
			sum3 += w[5] * in[(xi * iny + yi) * 4 + 2];
			sum4 += w[5] * in[(xi * iny + yi) * 4 + 3];
			sum1 += w[6] * in[(xi3 * iny + yi) * 4 + 0];
			sum2 += w[6] * in[(xi3 * iny + yi) * 4 + 1];
			sum3 += w[6] * in[(xi3 * iny + yi) * 4 + 2];
			sum4 += w[6] * in[(xi3 * iny + yi) * 4 + 3];
			sum1 += w[7] * in[(xi4 * iny + yi) * 4 + 0];
			sum2 += w[7] * in[(xi4 * iny + yi) * 4 + 1];
			sum3 += w[7] * in[(xi4 * iny + yi) * 4 + 2];
			sum4 += w[7] * in[(xi4 * iny + yi) * 4 + 3];
			sum1 += w[8] * in[(xi1 * iny + yi3) * 4 + 0];
			sum2 += w[8] * in[(xi1 * iny + yi3) * 4 + 1];
			sum3 += w[8] * in[(xi1 * iny + yi3) * 4 + 2];
			sum4 += w[8] * in[(xi1 * iny + yi3) * 4 + 3];
			sum1 += w[9] * in[(xi * iny + yi3) * 4 + 0];
			sum2 += w[9] * in[(xi * iny + yi3) * 4 + 1];
			sum3 += w[9] * in[(xi * iny + yi3) * 4 + 2];
			sum4 += w[9] * in[(xi * iny + yi3) * 4 + 3];
			sum1 += w[10] * in[(xi3 * iny + yi3) * 4 + 0];
			sum2 += w[10] * in[(xi3 * iny + yi3) * 4 + 1];
			sum3 += w[10] * in[(xi3 * iny + yi3) * 4 + 2];
			sum4 += w[10] * in[(xi3 * iny + yi3) * 4 + 3];
			sum1 += w[11] * in[(xi4 * iny + yi3) * 4 + 0];
			sum2 += w[11] * in[(xi4 * iny + yi3) * 4 + 1];
			sum3 += w[11] * in[(xi4 * iny + yi3) * 4 + 2];
			sum4 += w[11] * in[(xi4 * iny + yi3) * 4 + 3];
			sum1 += w[12] * in[(xi1 * iny + yi4) * 4 + 0];
			sum2 += w[12] * in[(xi1 * iny + yi4) * 4 + 1];
			sum3 += w[12] * in[(xi1 * iny + yi4) * 4 + 2];
			sum4 += w[12] * in[(xi1 * iny + yi4) * 4 + 3];
			sum1 += w[13] * in[(xi * iny + yi4) * 4 + 0];
			sum2 += w[13] * in[(xi * iny + yi4) * 4 + 1];
			sum3 += w[13] * in[(xi * iny + yi4) * 4 + 2];
			sum4 += w[13] * in[(xi * iny + yi4) * 4 + 3];
			sum1 += w[14] * in[(xi3 * iny + yi4) * 4 + 0];
			sum2 += w[14] * in[(xi3 * iny + yi4) * 4 + 1];
			sum3 += w[14] * in[(xi3 * iny + yi4) * 4 + 2];
			sum4 += w[14] * in[(xi3 * iny + yi4) * 4 + 3];
			sum1 += w[15] * in[(xi4 * iny + yi4) * 4 + 0];
			sum2 += w[15] * in[(xi4 * iny + yi4) * 4 + 1];
			sum3 += w[15] * in[(xi4 * iny + yi4) * 4 + 2];
			sum4 += w[15] * in[(xi4 * iny + yi4) * 4 + 3];

			out[(x * outy + y) * 4 + 0] = sum1;
			out[(x * outy + y) * 4 + 1] = sum2;
			out[(x * outy + y) * 4 + 2] = sum3;
			out[(x * outy + y) * 4 + 3] = sum4;
		}
	}
}

void BicubicFloat(float *in, float *out, int inx, int iny, int outx, int outy)
{
	float tx2, tx3, tx4;
	float ty2, ty3, ty4;
	float x1, x2, x3, x4;
	float y1, y2, y3, y4;
	float xr, yr;
	float w[16];
	int xi, yi;
	int xi1, xi3, xi4;
	int yi1, yi3, yi4;
	float scalex, scaley;
	float invscalex, invscaley;
	float sum1;
	scalex = (float)outx / inx;
	scaley = (float)outy / iny;
	invscalex = 1.0f / scalex;
	invscaley = 1.0f / scaley;
	for (int x = 0; x < outx; x++)
	{
		xi = x * invscalex;
		xi1 = xi - 1;
		if (xi1 < 0)
			xi1 += inx;
		xi3 = xi + 1;
		if (xi3 >= inx)
			xi3 -= inx;
		xi4 = xi + 2;
		if (xi4 >= inx)
			xi4 -= inx;

		xr = (float)x * invscalex - xi;


		x1 = .16666666666666666666666666666667f * (1.0f - xr) * (1.0f - xr) * (1.0f - xr);
		tx2 = .16666666666666666666666666666667f * (2.0f - xr) * (2.0f - xr) * (2.0f - xr);
		tx3 = .16666666666666666666666666666667f * (3.0f - xr) * (3.0f - xr) * (3.0f - xr);
		tx4 = .16666666666666666666666666666667f * (4.0f - xr) * (4.0f - xr) * (4.0f - xr);
		x2 = tx2
			- 4.0f * x1;
		x3 = tx3
			- 4.0f * tx2
			+ 6.0f * x1;
		x4 = tx4
			- 4.0f * tx3
			+ 6.0f * tx2
			- 4.0f * x1;

		for (int y = 0; y < outy; y++)
		{
			yi = y * invscaley;
			yi1 = yi - 1;
			if (yi1 < 0)
				yi1 += iny;
			yi3 = yi + 1;
			if (yi3 >= iny)
				yi3 -= iny;
			yi4 = yi + 2;
			if (yi4 >= iny)
				yi4 -= iny;

			yr = (float)y * invscaley - yi;


			y1 = .16666666666666666666666666666667f * (1.0f - yr) * (1.0f - yr) * (1.0f - yr);
			ty2 = .16666666666666666666666666666667f * (2.0f - yr) * (2.0f - yr) * (2.0f - yr);
			ty3 = .16666666666666666666666666666667f * (3.0f - yr) * (3.0f - yr) * (3.0f - yr);
			ty4 = .16666666666666666666666666666667f * (4.0f - yr) * (4.0f - yr) * (4.0f - yr);
			y2 = ty2
				- 4.0f * y1;
			y3 = ty3
				- 4.0f * ty2
				+ 6.0f * y1;
			y4 = ty4
				- 4.0f * ty3
				+ 6.0f * ty2
				- 4.0f * y1;

			w[0] = x1 * y1;
			w[1] = x2 * y1;
			w[2] = x3 * y1;
			w[3] = x4 * y1;
			w[4] = x1 * y2;
			w[5] = x2 * y2;
			w[6] = x3 * y2;
			w[7] = x4 * y2;
			w[8] = x1 * y3;
			w[9] = x2 * y3;
			w[10] = x3 * y3;
			w[11] = x4 * y3;
			w[12] = x1 * y4;
			w[13] = x2 * y4;
			w[14] = x3 * y4;
			w[15] = x4 * y4;
			// can reuse the bottom 12 in next for most y
			sum1 = w[0] * in[xi1 * iny + yi1];
			sum1 += w[1] * in[xi * iny + yi1];
			sum1 += w[2] * in[xi3 * iny + yi1];
			sum1 += w[3] * in[xi4 * iny + yi1];
			sum1 += w[4] * in[xi1 * iny + yi];
			sum1 += w[5] * in[xi * iny + yi];
			sum1 += w[6] * in[xi3 * iny + yi];
			sum1 += w[7] * in[xi4 * iny + yi];
			sum1 += w[8] * in[xi1 * iny + yi3];
			sum1 += w[9] * in[xi * iny + yi3];
			sum1 += w[10] * in[xi3 * iny + yi3];
			sum1 += w[11] * in[xi4 * iny + yi3];
			sum1 += w[12] * in[xi1 * iny + yi4];
			sum1 += w[13] * in[xi * iny + yi4];
			sum1 += w[14] * in[xi3 * iny + yi4];
			sum1 += w[15] * in[xi4 * iny + yi4];

			out[x * outy + y] = sum1;
		}
	}
}