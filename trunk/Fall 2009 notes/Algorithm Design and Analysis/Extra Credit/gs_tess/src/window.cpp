#include "main.h"
#include "window.h"
#include "render.h"

HINSTANCE	hInstance = NULL;
HWND		hWnd = NULL;
HGLRC		hRC = NULL;
HDC			hDC = NULL;

int			fullscreen = false;
int			wsizex = 1024, wsizey = wsizex * .75f, wbitdepth = 32;

float		gamma = 1.0f;

bool		active = true;

DEVMODE dmOriginalScreenSettings;

LRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	switch (uMsg)
	{
		case WM_ACTIVATE:
		{
			if (!HIWORD(wParam))
			{
				active = true;
			}
			else
			{
				active = false;
			}

			return 0;
		}

		case WM_SYSCOMMAND:
		{
			switch (wParam)
			{
				case SC_SCREENSAVE:
				case SC_MONITORPOWER:
				return 0;
			}
			break;
		}

		case WM_CLOSE:
		{
			PostQuitMessage(0);
			return 0;
		}

		case WM_KEYDOWN:
			if (wParam == VK_ESCAPE && lParam >> 30 == 0)
			{
				PostMessage(hWnd, WM_QUIT, 0, 0);
				return 0;
			}
			return 0;
		
		case WM_CHAR:
			return 0;

		case WM_SIZE:
		{
			Resize(LOWORD(lParam), HIWORD(lParam), 0, 0, 60);
			return 0;
		}

		case WM_SETFOCUS:
			ShowCursor(false);
			return 0;

		case WM_KILLFOCUS:
			ShowCursor(true);
			return 0;
	}

	return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

void UpdateGamma(float g)
{
	WORD ramp[3][256];
	for (int i = 0; i < 3; i++)
	{
		for (int n = 0; n < 256; n++)
		{
			ramp[i][n] = pow(n / 255.0f, g) * 65535.0f + .5f;
		}
	}

	SetDeviceGammaRamp(hDC, ramp);
}

void WindowShutdown()
{
	UpdateGamma(1.0f);

	if (fullscreen)
	{
		ChangeDisplaySettings(&dmOriginalScreenSettings, 0);
	}

	if (hRC)
	{
		wglMakeCurrent(NULL, NULL);
		wglDeleteContext(hRC);
		hRC = NULL;
	}
	if (hDC)
		ReleaseDC(hWnd, hDC);
	if (hWnd)
		DestroyWindow(hWnd);
	UnregisterClass("GS Tessellation", hInstance);
}

void WindowStartup()
{
	unsigned int pixelformat;
	PIXELFORMATDESCRIPTOR pfd;
	RECT window;
	DWORD style = WS_OVERLAPPEDWINDOW, exstyle = WS_EX_APPWINDOW | WS_EX_WINDOWEDGE;
	WNDCLASS wc;

	hInstance = GetModuleHandle(NULL);
	memset(&wc, 0, sizeof(WNDCLASS));
	wc.style = CS_HREDRAW | CS_VREDRAW | CS_OWNDC;
	wc.lpfnWndProc = WndProc;
	wc.hInstance = hInstance;
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	wc.lpszClassName = "GS Tessellation";

	RegisterClass(&wc);

	if (fullscreen)
	{
		memset(&dmOriginalScreenSettings, 0, sizeof(DEVMODE));
		dmOriginalScreenSettings.dmSize = sizeof(DEVMODE);
		EnumDisplaySettings(NULL, ENUM_CURRENT_SETTINGS, &dmOriginalScreenSettings);

		DEVMODE dmScreenSettings;
		memset(&dmScreenSettings, 0, sizeof(DEVMODE));
		dmScreenSettings.dmSize = sizeof(DEVMODE);
		dmScreenSettings.dmPelsWidth = wsizex;
		dmScreenSettings.dmPelsHeight = wsizey;
		dmScreenSettings.dmBitsPerPel = wbitdepth;
		dmScreenSettings.dmFields = DM_BITSPERPEL | DM_PELSWIDTH | DM_PELSHEIGHT;
		ChangeDisplaySettings(&dmScreenSettings, CDS_FULLSCREEN);
		exstyle = WS_EX_APPWINDOW;
		style = WS_POPUP;
	}

	window.bottom = wsizey;
	window.top = 0;
	window.left = 0;
	window.right = wsizex;

	AdjustWindowRectEx(&window, style, false, exstyle);
	hWnd = CreateWindowEx(exstyle, "GS Tessellation", "GS Tessellation", style | WS_CLIPSIBLINGS | WS_CLIPCHILDREN, 0, 0, window.right - window.left, window.bottom - window.top, NULL, NULL, hInstance, NULL);
	hDC = GetDC(hWnd);

	memset(&pfd, 0, sizeof(PIXELFORMATDESCRIPTOR));
	pfd.nVersion = 1;
	pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER;
	pfd.iPixelType = PFD_TYPE_RGBA;
	pfd.cColorBits = wbitdepth;
	pfd.cDepthBits = 24;
	pfd.cAlphaBits = 8;
	pfd.cStencilBits = 8;
	pfd.iLayerType = PFD_MAIN_PLANE;

	pixelformat = ChoosePixelFormat(hDC, &pfd);
	SetPixelFormat(hDC, pixelformat, &pfd);
	hRC = wglCreateContext(hDC);
	wglMakeCurrent(hDC, hRC);
	ShowWindow(hWnd, SW_SHOW);

	ShowCursor(true);

	UpdateGamma(gamma);

	Resize(wsizex, wsizey, 0, 0, 45);
}