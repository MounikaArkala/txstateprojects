#ifndef SVVECTOR_H
#define SVVECTOR_H

#include "vector3.h"

vector3 svadd(vector3 a, vector3 b);
vector3 svaddf(vector3 a, float b);
vector3 svsub(vector3 a, vector3 b);
vector3 svsubf(vector3 a, float b);
vector3 svmul(vector3 a, vector3 b);
vector3 svmulf(vector3 a, float b);
vector3 svdiv(vector3 a, vector3 b);
vector3 svdivf(vector3 a, float b);

#endif