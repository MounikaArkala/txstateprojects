#ifndef TEXTURE_H
#define TEXTURE_H

// texture loading and updating functions


struct TexInfo
{
	char filename[64];
	int width, height;
	int mipmap;
	int refcount;
};

extern unsigned int		*texture;
extern unsigned int		textures;
extern TexInfo			*texinfo;


extern int				anisotropy;


void RemoveTexture(int id);
int CreateTexture(const char *filename, bool clamp, bool duplicate, unsigned int minfilter, unsigned int magfilter);
int CreateTextureFromData(const char *filename, bool bgr, int width, int height, int bpp, unsigned char *data, bool clamp, bool duplicate, bool mip, unsigned int minfilter, unsigned int magfilter);
void TextureStartup();
void TextureShutdown();
void UpdateTextures();

#endif