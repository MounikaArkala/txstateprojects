#include <windows.h>
#include <stdio.h>
#include "debug_util.h"
#include "window.h"

bool gConsoleAllocated = false;
HANDLE gConsoleOut = 0;

void _DebugPrint(const char *format, ...)
{
	// allocate the console if it doesn't exist already
	// we don't really care about unallocating it, but the function is FreeConsole()
	if (!gConsoleAllocated)
	{
		gConsoleAllocated = true;

		if (AllocConsole())
		{
			gConsoleOut = GetStdHandle(STD_OUTPUT_HANDLE);
			SetForegroundWindow(hWnd); // put the main window on top
		}
	}

	if (format == 0 || format[0] == 0)
		return;

	// assemble the output string
	char text[1024];
	va_list valist;

	va_start(valist, format);
	    vsprintf(text, format, valist);
	va_end(valist);

	// output to debugger
	OutputDebugString(text);
	// output to console (not supplying characters written pointer...)
	if (gConsoleOut)
		WriteConsole(gConsoleOut, text, strlen(text), 0, 0);
}