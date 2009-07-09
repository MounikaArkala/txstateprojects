/* Nintendulator - Win32 NES emulator written in C++
 * Copyright (C) 2002-2009 QMT Productions
 *
 * $URL: https://nintendulator.svn.sourceforge.net/svnroot/nintendulator/nintendulator/trunk/src/c_e_unconnected.cpp $
 * $Id: c_e_unconnected.cpp 996 2009-05-23 02:02:20Z Quietust $
 */

#include "stdafx.h"
#include "Controllers.h"

namespace Controllers
{
void	ExpPort_Unconnected::Frame (unsigned char mode)
{
}
unsigned char	ExpPort_Unconnected::Read1 (void)
{
	return 0;
}
unsigned char	ExpPort_Unconnected::Read2 (void)
{
	return 0;
}
void	ExpPort_Unconnected::Write (unsigned char Val)
{
}
void	ExpPort_Unconnected::Config (HWND hWnd)
{
	MessageBox(hWnd, _T("No configuration necessary!"), _T("Nintendulator"), MB_OK);
}
ExpPort_Unconnected::~ExpPort_Unconnected (void)
{
	free(Data);
	free(MovData);
}
ExpPort_Unconnected::ExpPort_Unconnected (int *buttons)
{
	Type = EXP_UNCONNECTED;
	NumButtons = 0;
	Buttons = buttons;
	DataLen = 0;
	Data = malloc(DataLen);
	MovLen = 0;
	MovData = (unsigned char *)malloc(MovLen);
	ZeroMemory(MovData, MovLen);
}
} // namespace Controllers