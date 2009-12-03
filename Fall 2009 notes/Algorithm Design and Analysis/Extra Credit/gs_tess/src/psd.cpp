#include "main.h"
#include "psd.h"
#include "render.h"

int PSD::Load(const char *filename)
{
	if (data)
		Clear();

	FILE *file;
	file = fopen(filename, "rb");
	if (!file)
		return 0;

	PSDHeader header;
	if (!fread(&header, sizeof(PSDHeader), 1, file))
	{
		fclose(file);
		return 0;
	}

	if (header.signature[0] != '8' || header.signature[1] != 'B' || header.signature[2] != 'P' || header.signature[3] != 'S')
	{
		fclose(file);
		return 0;
	}

	channels = REVERSE2(header.channels);
	if (channels > 4)
		channels = 4;
	if (channels == 0)
	{
		fclose(file);
		return 0;
	}

	height = REVERSE4(header.rows);
	width = REVERSE4(header.columns);
	short depth = REVERSE2(header.depth);
	if (depth != 8)
	{
		fclose(file);
		return 0;
	}

	short mode = REVERSE2(header.mode);
	if (mode != 1 && mode != 3 && mode != 7) // grayscale, rgb, multichannel
	{
		fclose(file);
		return 0;
	}

	int temp;
	fread(&temp, 4, 1, file);
	temp = REVERSE4(temp);
	fseek(file, temp, SEEK_CUR); // color mode data (should be empty anyway)
	fread(&temp, 4, 1, file);
	temp = REVERSE4(temp);
	fseek(file, temp, SEEK_CUR); // image resources
	fread(&temp, 4, 1, file);
	temp = REVERSE4(temp);
	fseek(file, temp, SEEK_CUR); // misc (layer and mask info)

	short compression;
	fread(&compression, sizeof(short), 1, file);
	compression = REVERSE2(compression);
	if (compression != 0 && compression != 1) // uncompressed or RLE only
	{
		fclose(file);
		return 0;
	}

	data = new unsigned char [channels * width * height];
	unsigned char *cdata = new unsigned char [width * height];
	if (compression == 0)
	{
		for (int c = 0; c < channels; c++)
		{
			fread(cdata, width * height, 1, file);
			for (int n = 0; n < width * height; n++)
			{
				data[n * channels + c] = cdata[n];
			}
		}
	}
	else // RLE
	{
		int origchannels = REVERSE2(header.channels);
		int rowcount = origchannels * height; // use original (possibly > 4) channels
		short *linelen = new short [rowcount];
		fread(linelen, sizeof(short) * rowcount, 1, file);
		int n;
		for (n = 0; n < rowcount; n++)
		{
			linelen[n] = REVERSE2(linelen[n]);
		}

		char *ctemp = new char [width + 127]; // maximum RLE size is original size + 127?
		for (int c = 0; c < channels; c++)
		{
			for (n = 0; n < height; n++) // read in up to first 4 channels
			{
				fread(ctemp, linelen[c * height + n], 1, file);
				RLEUnpack(ctemp, (char *)&cdata[n * width], linelen[c * height + n]);
			}
			for (n = 0; n < width * height; n++)
			{
				data[n * channels + c] = cdata[n];
			}
		}

		delete [] ctemp;
		delete [] linelen;
	}

	// swap r and b
	if (channels > 2)
	{
		unsigned char btemp;
		for (int n = 0; n < width * height; n++)
		{
			btemp = data[n * channels + 0];
			data[n * channels + 0] = data[n * channels + 2];
			data[n * channels + 2] = btemp;
		}
	}

	// no respectable texture format is complete unless it is stored upside down
	unsigned char *flipdata = new unsigned char [channels * width * height];
	for (int h = 0; h < height; h++)
	{
		for (int w = 0; w < width; w++)
		{
			memcpy(&flipdata[h * width * channels], &data[(height - h - 1) * width * channels], channels * width);
		}
	}
	delete [] data;
	data = flipdata;

	fclose(file);

	return 1;
}

void PSD::Upload2D(int mipmap)
{
	if (data == 0)
		return;

	int internalformat, format;
	if (channels == 1)
	{
		internalformat = GL_LUMINANCE8;
		format = GL_LUMINANCE;
	}
	else if (channels == 2)
	{
		internalformat = GL_LUMINANCE8_ALPHA8;
		format = GL_LUMINANCE_ALPHA;
	}
	else if (channels == 3)
	{
		internalformat = GL_RGB8;
		format = GL_BGR;
	}
	else if (channels == 4)
	{
		internalformat = GL_RGBA8;
		format = GL_BGRA;
	}
	else
		return;

	glTexImage2D(GL_TEXTURE_2D, 0, internalformat, width, height, 0, format, GL_UNSIGNED_BYTE, data);

	if (mipmap)
	{
		int dimx = width, dimy = height;
		unsigned char *level;
		unsigned char *prevlevel;
		prevlevel = new unsigned char [dimx * dimy * channels];
		memcpy(prevlevel, data, dimx * dimy * channels);
		int i, x, y, c;
		for (i = 1;; i++)
		{
			if (dimx <= 1 && dimy <= 1)
				break;
			dimx /= 2;
			dimy /= 2;
			if (dimx == 0)
			{
				level = new unsigned char [1 * dimy * channels];
				for (y = 0; y < dimy - 1; y++)
				{
					for (c = 0; c < channels; c++)
						level[(y) * channels + c] = prevlevel[(y * 2) * channels + c] / 2
							+ prevlevel[(y * 2 + 1) * channels + c] / 2;
				}
				for (c = 0; c < channels; c++)
					level[(y) * channels + c] = prevlevel[(y * 2) * channels + c] / 2
						+ prevlevel[c] / 2;
				glTexImage2D(GL_TEXTURE_2D, i, internalformat, 1, dimy, 0, format, GL_UNSIGNED_BYTE, level);
			}
			else if (dimy == 0)
			{
				level = new unsigned char [dimx * 1 * channels];
				for (x = 0; x < dimx - 1; x++)
				{
					for (c = 0; c < channels; c++)
						level[(x * dimy) * channels + c] = prevlevel[(x * 2 * dimy * 2) * channels + c] / 2
							+ prevlevel[((x * 2 + 1) * dimy * 2) * channels + c] / 2;
				}
				for (c = 0; c < channels; c++)
					level[(x * dimy) * channels + c] = prevlevel[(x * 2 * dimy * 2) * channels + c] / 2
						+ prevlevel[c] / 2;
				glTexImage2D(GL_TEXTURE_2D, i, internalformat, dimx, 1, 0, format, GL_UNSIGNED_BYTE, level);
			}
			else
			{
				level = new unsigned char [dimx * dimy * channels];
				for (x = 0; x < dimx - 1; x++)
				{
					for (y = 0; y < dimy - 1; y++)
					{
						for (c = 0; c < channels; c++)
							level[(x * dimy + y) * channels + c] = prevlevel[(x * 2 * dimy * 2 + y * 2) * channels + c] / 4
								+ prevlevel[((x * 2 + 1) * dimy * 2 + y * 2) * channels + c] / 4
								+ prevlevel[((x * 2 + 1) * dimy * 2 + y * 2 + 1) * channels + c] / 4
								+ prevlevel[(x * 2 * dimy * 2 + y * 2 + 1) * channels + c] / 4;
					}
					for (c = 0; c < channels; c++)
						level[(x * dimy + y) * channels + c] = prevlevel[(x * 2 * dimy * 2 + y * 2) * channels + c] / 4
							+ prevlevel[((x * 2 + 1) * dimy * 2 + y * 2) * channels + c] / 4
							+ prevlevel[((x * 2 + 1) * dimy * 2 + 0) * channels + c] / 4
							+ prevlevel[(x * 2 * dimy * 2 + 0) * channels + c] / 4;
				}
				for (y = 0; y < dimy - 1; y++)
				{
					for (c = 0; c < channels; c++)
						level[(x * dimy + y) * channels + c] = prevlevel[(x * 2 * dimy * 2 + y * 2) * channels + c] / 4
							+ prevlevel[(0 + y * 2) * channels + c] / 4
							+ prevlevel[(0 + y * 2 + 1) * channels + c] / 4
							+ prevlevel[(x * 2 * dimy * 2 + y * 2 + 1) * channels + c] / 4;
				}
				for (c = 0; c < channels; c++)
					level[(x * dimy + y) * channels + c] = prevlevel[(x * 2 * dimy * 2 + y * 2) * channels + c] / 4
						+ prevlevel[(0 + y * 2) * channels + c] / 4
						+ prevlevel[(0) * channels + c] / 4
						+ prevlevel[(x * 2 * dimy * 2 + 0) * channels + c] / 4;
				glTexImage2D(GL_TEXTURE_2D, i, internalformat, dimx, dimy, 0, format, GL_UNSIGNED_BYTE, level);
			}
			delete [] prevlevel;
			prevlevel = level;
		}
		delete [] level;
	}
}