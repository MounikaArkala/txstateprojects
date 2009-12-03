#ifndef NOISE_H
#define NOISE_H

extern int p3d_time;

// matches edge values by averages
void FixEdges(float *height, int dim);

// normalize to [0-1]
void Normalize(float *height, int dim);

void Voronoi(float *height, int dim, int count, float bias);
// produces normalized results
void PerlinBicubic2(float *out, int outdim, int gridsize, int levels);
// max peturb distance is dim * magnitude, smoothness of 0 = normal and higher values are more smooth
void Perturb(float *height, int dim, float magnitude, int smoothness);

// add per pixel randomness
void NoiseAdd(float *height, int dim, float strength);

void Erosion(float *out, int dim, int iterations, float scale, int maxdist, float radiuscale);
// random terrain buildup at local minimum
void Deposition(float *out, int dim, int iterations, float scale, int maxdist);
// focuses around a point, so it produces something more like a mountain range or islands, but similar to above
void Deposition2(float *out, int dim, int iterations, float scale, int clear);

// h = 1.5 is a good value
void NoiseFFT(float *out, int dim, float scale, float h = 1.5f);

// power of 2
float DiamondSquare2(float *height, int dim, float persistence, float scale);
// power of 2 + 1
float DiamondSquare(float *height, int dim, float persistence, float scale);
float DiamondSquareExpand(float *in, int indim, float *out, int outdim, float persistence, float scale);


float Perlin1D(float p, const float *grid, const int gridsize, float gridscale, float outscale, const int levels);

float Perlin3DSSE(const float *p, const float *grid, const int gridsize, float outscale, const int levels);
// gridsize must be power of 2
// p must be 4 * count elements
// p, out, and grid must be 16-byte aligned
// out is added to, so clear to 0 if needed
void Perlin3DSSEArray(const float *p, float *out, const int count, const float *grid, const int gridsize, float outscale, const int levels);
// -1 to 1 input
float Perlin3D(const float *p, const float *grid, const int gridsize, float outscale, const int levels);
// 0 to 1 input
float Perlin3D2(const float *p, const float *grid, const int gridsize, float outscale, const int levels);

float PerlinBicubic(float *out, int outdim, int gridsize, int levels, float turbulence);
// one grid
float Perlin(float *out, int outdim, float *grid, int gridsize, int levels);
// new grid each level
float Perlin2(float *out, int outdim, int gridsize, int levels);
// single point, s-curve
float Perlin2D(const float x, const float y, const float *grid, const int gridsize, float outscale, const int levels);


// 3 component nearest sample on a 4 component buffer
void Nearest3x4(unsigned char *in, unsigned char *out, int inx, int iny, int outx, int outy);

// 3 component interpolation on a 4 component buffer
void Bilinear3x4(unsigned char *in, unsigned char *out, int inx, int iny, int outx, int outy);
void BilinearFloat(float *in, float *out, int inx, int iny, int outx, int outy);

void Bicubic4(unsigned char *in, unsigned char *out, int inx, int iny, int outx, int outy);
void BicubicFloat(float *in, float *out, int inx, int iny, int outx, int outy);

#endif