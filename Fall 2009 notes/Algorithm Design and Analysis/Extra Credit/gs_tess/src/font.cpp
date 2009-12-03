#include "main.h"
#include "render.h"
#include "window.h"

unsigned int fontbase;
unsigned char fontwidth[256];

unsigned int			fonttex = 0;

void WordWrap(float scale, int width, const std::string &in, std::vector<std::string> &out)
{
	std::string temp;
	std::string::const_iterator start = in.begin();
	std::string::const_iterator last = in.begin();
	for (std::string::const_iterator it = in.begin(); it != in.end(); ++it)
	{
		if ((*it) == ' ')
		{
			temp.clear();
			temp.insert(temp.begin(), start, it);
			int twidth = GetFontWidth(scale, "%s", temp.c_str()) + .5f;
			if (twidth > width)
			{
				temp.clear();
				temp.insert(temp.begin(), start, last);
				out.push_back(temp);
				start = last + 1;
			}
			last = it;
		}
	}
	if (start < in.end())
	{
		temp.clear();
		temp.insert(temp.begin(), start, in.end());
		out.push_back(temp);
	}
}

float GetFontWidth(float scale, const char *format, ...)
{
	if (!strlen(format))
		return 0;

	char text[512];
	va_list valist;

	va_start(valist, format);
	    vsprintf(text, format, valist);
	va_end(valist);

	int len = strlen(text);
	float width = 0;
	int n;
	for (n = 0; n < len; n++)
	{
		width += fontwidth[text[n] - 32] * scale + .5f;
	}
	//width += fontwidth[text[n - 1] - 32] * scale + .5f;

	return width;
}

void PrintScaled(float scale, float x, float y, const char *format, ...)
{
	if (!strlen(format))
		return;

	char text[512];
	va_list valist;

	va_start(valist, format);
	    vsprintf(text, format, valist);
	va_end(valist);

	glPushMatrix();
	glTranslatef(x - fontwidth[text[0] - 32] / 2 * scale, y, 0);
	glListBase(fontbase - 32);
	glScalef(scale, scale, scale);
	glCallLists(strlen(text), GL_UNSIGNED_BYTE, text);
	glPopMatrix();
}

void Print(float x, float y, const char *format, ...)
{
	if (!strlen(format))
		return;

	char text[512];
	va_list valist;

	va_start(valist, format);
	    vsprintf(text, format, valist);
	va_end(valist);

	glPushMatrix();
	glTranslatef(x - fontwidth[text[0] - 32] / 2, y, 0);
	glListBase(fontbase - 32);
	glCallLists(strlen(text), GL_UNSIGNED_BYTE, text);
	glPopMatrix();
}

void FontDelete()
{
	glDeleteLists(fontbase, 256);
}

void BuildFont(const char *fontwidthfile, int tex, unsigned int &base)
{
	FILE *file;
	file = fopen(fontwidthfile, "rb");
	fread(fontwidth, 256, 1, file);
	fclose(file);

	base = glGenLists(256);
	for (int n = 0; n < 256; n++)
	{
		float cx = (float)(n % 16) / 16;
		float cy = 1 - (float)(n / 16) / 16;

		glNewList(base + n, GL_COMPILE);
			glTranslatef(fontwidth[n] / 2, 0, 0);
			glBegin(GL_QUADS);
				glTexCoord2f(cx, cy - 0.0625);
				glVertex2f(0, 0);
				glTexCoord2f(cx + 0.0625, cy - 0.0625);
				glVertex2f(16 * 2, 0);
				glTexCoord2f(cx + 0.0625, cy - 0.001 * 0);
				glVertex2f(16 * 2, 16 * 2);
				glTexCoord2f(cx , cy - 0.001 * 0);
				glVertex2f(0, 16 * 2);
			glEnd();
			glTranslatef(fontwidth[n] / 2 + 1, 0, 0);
		glEndList();
	}
}