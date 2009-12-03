// texture loading and updating functions

#pragma warning (disable: 4018)

#define WIN32_LEAN_AND_MEAN
#define _WIN32_WINNT 0x500 // for readdirectorychangesw
#include <windows.h>
#include <gl.h>
#include <stdio.h>
#include "nv_dds.h"
#include "psd.h"
#include "texture.h"


unsigned int			*texture = NULL;
unsigned int			textures = 0;
TexInfo					*texinfo = NULL;

int						anisotropy = 16;

using namespace nv_dds;

std::vector<int> textureupdatelist;
int textureupdatelistlock = 0;
DWORD WINAPI TextureUpdateCheckThread(void *lpParameter);

void RemoveTexture(int id)
{
}

int CreateTexture(const char *filename, bool clamp, bool duplicate, unsigned int minfilter, unsigned int magfilter)
{
	if (!filename)
	{
//		return -1;
		return CreateTexture("default", false, false, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR);
	}

	if (duplicate == false)
	{
		for (int n = 0; n < textures; n++)
		{
			if (_stricmp(filename, texinfo[n].filename) == 0)
			{
				texinfo[n].refcount++;
				return n;
			}
		}
	}


	char fullname[256];
	PSD psdimage;
	CDDSImage image;
	int psd = 0;
	sprintf(fullname, "textures\\%s.psd", filename);
	if (psdimage.Load(fullname))
	{
		psd = 1;
	}
	else
	{
		sprintf(fullname, "textures\\%s.dds", filename);

		if (!image.load(fullname))
		{
	//		return -1;
			return CreateTexture("default", false, false, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR);
		}
	}


	texture = (unsigned int*)realloc(texture, sizeof(unsigned int) * (textures + 1));
	texinfo = (TexInfo*)realloc(texinfo, sizeof(TexInfo) * (textures + 1));


	int mipmap = 0;
	if (minfilter == GL_NEAREST_MIPMAP_NEAREST || minfilter == GL_LINEAR_MIPMAP_NEAREST || minfilter == GL_NEAREST_MIPMAP_LINEAR || minfilter == GL_LINEAR_MIPMAP_LINEAR)
		mipmap = 1;


	glGenTextures(1, &texture[textures]);
	glBindTexture(GL_TEXTURE_2D, texture[textures]);
	if (psd)
	{
		psdimage.Upload2D(mipmap);
	}
	else
	{
		image.upload_texture2D();
	}
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minfilter);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magfilter);
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, anisotropy);

	if (clamp)
	{
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
	}

	strcpy(texinfo[textures].filename, filename);
	if (psd)
	{
		texinfo[textures].width = psdimage.width;
		texinfo[textures].height = psdimage.height;
	}
	else
	{
		texinfo[textures].width = image.get_width();
		texinfo[textures].height = image.get_height();
	}
	texinfo[textures].mipmap = mipmap;
	texinfo[textures].refcount = 1;

	psdimage.Clear();
	image.clear();

	textures++;

	return textures - 1;
}

int CreateTextureFromData(const char *filename, bool bgr, int width, int height, int bpp, unsigned char *data, bool clamp, bool duplicate, bool mip, unsigned int minfilter, unsigned int magfilter)
{
	if (!filename)
		return -1;

	if (duplicate == false)
	{
		for (int n = 0; n < textures; n++)
		{
			if (_stricmp(filename, texinfo[n].filename) == 0)
				return n;
		}
	}

	texture = (unsigned int*)realloc(texture, sizeof(unsigned int) * (textures + 1));
	texinfo = (TexInfo*)realloc(texinfo, sizeof(TexInfo) * (textures + 1));

	if (width < 1 || height < 1)
		return -1;

	int type, bytespp, size;
	if (bgr)
	{
		if (bpp == 24)
			type = GL_BGR;
		else if (bpp == 32)
			type = GL_BGRA;
		else
			type = GL_LUMINANCE;
	}
	else
	{
		if (bpp == 24)
			type = GL_RGB;
		else if (bpp == 32)
			type = GL_RGBA;
		else
			type = GL_LUMINANCE;
	}
	bytespp = bpp / 8;
	int internalformat;
	if (bytespp == 3)
		internalformat = GL_RGB8;
	else if (bytespp == 4)
		internalformat = GL_RGBA8;
	else
		internalformat = GL_LUMINANCE8;
	size = width * height * bytespp;

//	texinfo[textures].memory = 0;

	glGenTextures(1, &texture[textures]);
	glBindTexture(GL_TEXTURE_2D, texture[textures]);
	int dimx = width, dimy = height;
	unsigned char *level;
	unsigned char *prevlevel;
	glTexImage2D(GL_TEXTURE_2D, 0, internalformat, dimx, dimy, 0, type, GL_UNSIGNED_BYTE, data);
//	texturememory += dimx * dimy * bytespp;
//	texinfo[textures].memory += dimx * dimy * bytespp;
	if (mip)
	{
		prevlevel = new unsigned char [dimx * dimy * bytespp];
		memcpy(prevlevel, data, dimx * dimy * bytespp);
		int i, x, y, c;
		for (i = 1;; i++)
		{
			if (dimx <= 1 && dimy <= 1)
				break;
			dimx /= 2;
			dimy /= 2;
			if (dimx == 0)
			{
				level = new unsigned char [1 * dimy * bytespp];
				for (y = 0; y < dimy - 1; y++)
				{
					for (c = 0; c < bytespp; c++)
						level[(y) * bytespp + c] = prevlevel[(y * 2) * bytespp + c] / 2
							+ prevlevel[(y * 2 + 1) * bytespp + c] / 2;
				}
				for (c = 0; c < bytespp; c++)
					level[(y) * bytespp + c] = prevlevel[(y * 2) * bytespp + c] / 2
						+ prevlevel[c] / 2;
				glTexImage2D(GL_TEXTURE_2D, i, internalformat, 1, dimy, 0, type, GL_UNSIGNED_BYTE, level);
//				texturememory += 1 * dimy * bytespp;
//				texinfo[textures].memory += 1 * dimy * bytespp;
			}
			else if (dimy == 0)
			{
				level = new unsigned char [dimx * 1 * bytespp];
				for (x = 0; x < dimx - 1; x++)
				{
					for (c = 0; c < bytespp; c++)
						level[(x * dimy) * bytespp + c] = prevlevel[(x * 2 * dimy * 2) * bytespp + c] / 2
							+ prevlevel[((x * 2 + 1) * dimy * 2) * bytespp + c] / 2;
				}
				for (c = 0; c < bytespp; c++)
					level[(x * dimy) * bytespp + c] = prevlevel[(x * 2 * dimy * 2) * bytespp + c] / 2
						+ prevlevel[c] / 2;
				glTexImage2D(GL_TEXTURE_2D, i, internalformat, dimx, 1, 0, type, GL_UNSIGNED_BYTE, level);
//				texturememory += dimx * 1 * bytespp;
//				texinfo[textures].memory += dimx * 1 * bytespp;
			}
			else
			{
				level = new unsigned char [dimx * dimy * bytespp];
				for (x = 0; x < dimx - 1; x++)
				{
					for (y = 0; y < dimy - 1; y++)
					{
						for (c = 0; c < bytespp; c++)
							level[(x * dimy + y) * bytespp + c] = prevlevel[(x * 2 * dimy * 2 + y * 2) * bytespp + c] / 4
								+ prevlevel[((x * 2 + 1) * dimy * 2 + y * 2) * bytespp + c] / 4
								+ prevlevel[((x * 2 + 1) * dimy * 2 + y * 2 + 1) * bytespp + c] / 4
								+ prevlevel[(x * 2 * dimy * 2 + y * 2 + 1) * bytespp + c] / 4;
					}
					for (c = 0; c < bytespp; c++)
						level[(x * dimy + y) * bytespp + c] = prevlevel[(x * 2 * dimy * 2 + y * 2) * bytespp + c] / 4
							+ prevlevel[((x * 2 + 1) * dimy * 2 + y * 2) * bytespp + c] / 4
							+ prevlevel[((x * 2 + 1) * dimy * 2 + 0) * bytespp + c] / 4
							+ prevlevel[(x * 2 * dimy * 2 + 0) * bytespp + c] / 4;
				}
				for (y = 0; y < dimy - 1; y++)
				{
					for (c = 0; c < bytespp; c++)
						level[(x * dimy + y) * bytespp + c] = prevlevel[(x * 2 * dimy * 2 + y * 2) * bytespp + c] / 4
							+ prevlevel[(0 + y * 2) * bytespp + c] / 4
							+ prevlevel[(0 + y * 2 + 1) * bytespp + c] / 4
							+ prevlevel[(x * 2 * dimy * 2 + y * 2 + 1) * bytespp + c] / 4;
				}
				for (c = 0; c < bytespp; c++)
					level[(x * dimy + y) * bytespp + c] = prevlevel[(x * 2 * dimy * 2 + y * 2) * bytespp + c] / 4
						+ prevlevel[(0 + y * 2) * bytespp + c] / 4
						+ prevlevel[(0) * bytespp + c] / 4
						+ prevlevel[(x * 2 * dimy * 2 + 0) * bytespp + c] / 4;
				glTexImage2D(GL_TEXTURE_2D, i, internalformat, dimx, dimy, 0, type, GL_UNSIGNED_BYTE, level);
//				texturememory += dimx * dimy * bytespp;
//				texinfo[textures].memory += dimx * dimy * bytespp;
			}
			delete [] prevlevel;
			prevlevel = level;
		}
		delete [] level;
	}
/*	if (mip)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST);
	else
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);*/
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, minfilter);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, magfilter);
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY_EXT, anisotropy);

	if (clamp)
	{
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
	}

	strcpy(texinfo[textures].filename, filename);
	texinfo[textures].width = width;
	texinfo[textures].height = height;
	texinfo[textures].mipmap = mip;

	textures++;

	return textures - 1;
}

void TextureUpdate(const char *filename, int n)
{
	glBindTexture(GL_TEXTURE_2D, texture[n]);

	char fullname[256];
	PSD psdimage;
	CDDSImage image;
	int psd = 0;
	sprintf(fullname, "textures\\%s.psd", filename);
	if (psdimage.Load(fullname))
	{
		psdimage.Upload2D(texinfo[n].mipmap);
	}
	else
	{
		sprintf(fullname, "textures\\%s.dds", filename);

		if (image.load(fullname))
		{
			image.upload_texture2D();
		}
	}
}

void TextureStartup()
{
	float max_anisotropy, anisotropy_level = anisotropy;
	glGetFloatv(GL_MAX_TEXTURE_MAX_ANISOTROPY_EXT, &max_anisotropy);
	if (max_anisotropy > anisotropy_level)
		anisotropy = anisotropy_level;
	else
		anisotropy = max_anisotropy;


	DWORD threadid;
	HANDLE pt = CreateThread(0, 0, TextureUpdateCheckThread, 0, 0, &threadid);
	SetThreadPriority(pt, -1);
	CloseHandle(pt);
}

void TextureShutdown()
{
	if (texture)
	{
		glDeleteTextures(textures, texture);
		free(texture);
		texture = 0;
		free(texinfo);
		texinfo = 0;
		textures = 0;
	}
}

DWORD WINAPI TextureUpdateCheckThread(void *lpParameter)
{
	HANDLE hDir = CreateFile(
		"textures\\",
		GENERIC_READ,
		FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
		NULL,
		OPEN_EXISTING,
		FILE_FLAG_BACKUP_SEMANTICS,
		NULL
	);

	if (hDir == INVALID_HANDLE_VALUE)
		return 0;

	unsigned char *fnbuffer[10000];
	while (1) // could check for a terminate signal...
	{
		FILE_NOTIFY_INFORMATION *fn = (FILE_NOTIFY_INFORMATION *)fnbuffer;
		int bytesreturned = 0;
		if (ReadDirectoryChangesW(hDir, (void *)fnbuffer, 10000, true, FILE_NOTIFY_CHANGE_LAST_WRITE | FILE_NOTIFY_CHANGE_FILE_NAME, (LPDWORD)&bytesreturned, 0, 0))
		{
			while (textureupdatelistlock == 1) // wait until we have access
			{
				Sleep(0);
			}
			textureupdatelistlock = 1;

			while (1)
			{
				if (fn->Action == FILE_ACTION_ADDED || fn->Action == FILE_ACTION_MODIFIED || fn->Action == FILE_ACTION_RENAMED_NEW_NAME)
				{
					char *name;
					name = new char [fn->FileNameLength / 2 + 1];
					wcstombs(name, fn->FileName, fn->FileNameLength / 2 + 1);

					for (int n = 0; n < fn->FileNameLength / 2; n++)
					{
						if (name[n] == '.') // remove extension
						{
							name[n] = 0;
							break;
						}
					}

					for (int n = 0; n < textures; n++)
					{
						if (_stricmp(name, texinfo[n].filename) == 0)
						{
							// check for duplicates (seems to create two modified events)
							int i;
							for (i = 0; i < textureupdatelist.size(); i++)
							{
								if (textureupdatelist[i] == n)
									break;
							}
							if (i >= textureupdatelist.size())
								textureupdatelist.push_back(n);
							break;
						}
					}

					delete [] name;
				}

				if (fn->NextEntryOffset == 0)
					break;
				fn = (FILE_NOTIFY_INFORMATION *)(((unsigned char *)fn) + fn->NextEntryOffset);
			}

			textureupdatelistlock = 0;
		}
		else // nothing happened
		{
			Sleep(10);
		}
	}

	CloseHandle(hDir);

	return 1;
}

void UpdateTextures()
{
	if (textureupdatelistlock == 1)
		return;

	textureupdatelistlock = 1;
	for (int n = 0; n < textureupdatelist.size(); n++)
	{
		TextureUpdate(texinfo[textureupdatelist[n]].filename, textureupdatelist[n]);
	}
	textureupdatelist.clear();
	textureupdatelistlock = 0;
}