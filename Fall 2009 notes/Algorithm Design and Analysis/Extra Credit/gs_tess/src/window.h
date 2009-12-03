#ifndef WINDOW_H
#define WINDOW_H

extern HINSTANCE	hInstance;
extern HWND			hWnd;
extern HGLRC		hRC;
extern HDC			hDC;

extern int fullscreen;
extern int wsizex, wsizey, wbitdepth;
extern float gamma;

extern bool active;

void WindowShutdown();
void WindowStartup();
void UpdateGamma(float g);

#endif