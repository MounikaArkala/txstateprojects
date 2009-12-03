#ifndef PSD_H
#define PSD_H

// matching pop at bottom
#pragma pack(push)
#pragma pack(2)

struct PSDHeader
{
	char signature[4];
	short version;
	char reserved[6];
	short channels;
	int rows;
	int columns;
	short depth;
	short mode;
};

#pragma pack(pop)

class PSD
{
public:
	unsigned char *data;
	int width, height, channels;

	PSD()
	{
		data = 0;
		channels = 0;
	}
	~PSD()
	{
		Clear();
	}
	int Load(const char *filename);
	void Upload2D(int mipmap);
	void Clear()
	{
		if (data)
			delete [] data;
		data = 0;
		channels = 0;
	}
private:
};

#endif