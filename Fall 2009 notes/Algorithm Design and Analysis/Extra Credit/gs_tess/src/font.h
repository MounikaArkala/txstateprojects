#ifndef FONT_H
#define FONT_H

extern unsigned int fontbase;

extern unsigned int	fonttex;


void WordWrap(float scale, int width, const std::string &in, std::vector<std::string> &out);

float GetFontWidth(float scale, const char *format, ...);
void PrintScaled(float scale, float x, float y, const char *format, ...);
void Print(float x, float y, const char *format, ...);
void FontDelete();
void BuildFont(const char *widthfile, int tex, unsigned int &base);

#endif