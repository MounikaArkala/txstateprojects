#ifndef FFT_H
#define FFT_H

// 2d
void cdft2d(int, int, int, float **, float *, int *, float *);
void rdft2d(int, int, int, float **, float *, int *, float *);
void rdft2dsort(int, int, int, float **);
void ddct2d(int, int, int, float **, float *, int *, float *);
void ddst2d(int, int, int, float **, float *, int *, float *);

// 1d
void cdft(int, int, float *, int *, float *);
void rdft(int, int, float *, int *, float *);
void ddct(int, int, float *, int *, float *);
void ddst(int, int, float *, int *, float *);
void dfct(int, float *, float *, int *, float *);
void dfst(int, float *, float *, int *, float *);

#endif