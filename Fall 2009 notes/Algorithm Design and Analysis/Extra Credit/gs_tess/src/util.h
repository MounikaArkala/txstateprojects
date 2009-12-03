#ifndef UTIL_H
#define UTIL_H

// endian conversion
#define	REVERSE4(type)	(((type >> 24) & 0x000000ff) | \
						((type >> 8) & 0x0000ff00) | \
						((type << 8) & 0x00ff0000) | \
						((type << 24) & 0xff000000) )
#define	REVERSE2(type)	(((type >> 8) & 0x00ff) | \
						((type << 8) & 0xff00) )

// returns the log base 2, or the position of the highest bit set
inline int GetBitIndex(unsigned int v);

// does not do the translation portion
matrix LookAt(vector3 from, vector3 to, vector3 up);

// PackBits
void RLEUnpack(char *in, char *out, int inlen);

#endif