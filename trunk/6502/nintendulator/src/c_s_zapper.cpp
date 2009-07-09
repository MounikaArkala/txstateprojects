/* Nintendulator - Win32 NES emulator written in C++
 * Copyright (C) 2002-2009 QMT Productions
 *
 * $URL: https://nintendulator.svn.sourceforge.net/svnroot/nintendulator/nintendulator/trunk/src/c_s_zapper.cpp $
 * $Id: c_s_zapper.cpp 996 2009-05-23 02:02:20Z Quietust $
 */

#include "stdafx.h"
#include "Nintendulator.h"
#include "resource.h"
#include "Movie.h"
#include "Controllers.h"
#include "MapperInterface.h"
#include "PPU.h"
#include "GFX.h"

namespace Controllers
{
#include <pshpack1.h>
struct StdPort_Zapper_State
{
	unsigned char PosX;
	unsigned char PosY;
	unsigned char Button;
};
#include <poppack.h>
#define State ((StdPort_Zapper_State *)Data)

void	StdPort_Zapper::Frame (unsigned char mode)
{
	POINT pos;
	if (mode & MOV_PLAY)
	{
		State->PosX = MovData[0];
		State->PosY = MovData[1];
		State->Button = MovData[2];
		GFX::SetCursorPos(State->PosX, State->PosY);
	}
	else
	{
		GFX::GetCursorPos(&pos);
		State->PosX = pos.x;
		State->PosY = pos.y;
		if ((State->PosX < 0) || (State->PosX > 255) || (State->PosY < 0) || (State->PosY > 239))
			State->PosX = State->PosY = 255;	// if it's off-screen, push it to the bottom
		State->Button = IsPressed(Buttons[0]);
	}
	if (mode & MOV_RECORD)
	{
		MovData[0] = State->PosX;
		MovData[1] = State->PosY;
		MovData[2] = State->Button;
	}
}

unsigned char	StdPort_Zapper::Read (void)
{
	int x = State->PosX, y = State->PosY, z = State->Button;
	int WhiteCount = 0;
	unsigned char Bits = 0x00;
	int X, Y;

	if (z)
		Bits |= 0x10;

	if ((x < 0) || (x >= 256) || (y < 0) || (y >= 240))
		return Bits | 0x08;

	if (PPU::IsRendering && PPU::OnScreen)
		for (Y = y - 8; Y < y + 8; Y++)
		{
			if (Y < 0)
				Y = 0;
			if (Y < PPU::SLnum - 32)
				continue;
			if (Y >= PPU::SLnum)
				break;
			for (X = x - 8; X < x + 8; X++)
			{
				if (X < 0)
					X = 0;
				if (X > 255)
					break;
				if (GFX::ZapperHit(PPU::DrawArray[Y * 256 + X]))
					WhiteCount++;
			}
		}
	if (WhiteCount < 64)
		Bits |= 0x08;
	return Bits;
}
void	StdPort_Zapper::Write (unsigned char Val)
{
}
static	INT_PTR	CALLBACK	ConfigProc (HWND hDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	int dlgLists[1] = {IDC_CONT_D0};
	int dlgButtons[1] = {IDC_CONT_K0};
	StdPort *Cont;
	if (uMsg == WM_INITDIALOG)
	{
		SetWindowLongPtr(hDlg, GWL_USERDATA, lParam);
		Cont = (StdPort *)lParam;
	}
	else	Cont = (StdPort *)GetWindowLongPtr(hDlg, GWL_USERDATA);
	ParseConfigMessages(hDlg, 1, dlgLists, dlgButtons, Cont ? Cont->Buttons : NULL, uMsg, wParam, lParam);
	return FALSE;
}
void	StdPort_Zapper::Config (HWND hWnd)
{
	DialogBoxParam(hInst, (LPCTSTR)IDD_STDPORT_ZAPPER, hWnd, ConfigProc, (LPARAM)this);
}
StdPort_Zapper::~StdPort_Zapper (void)
{
	free(Data);
	free(MovData);
}
StdPort_Zapper::StdPort_Zapper (int *buttons)
{
	Type = STD_ZAPPER;
	NumButtons = 1;
	Buttons = buttons;
	DataLen = sizeof(*State);
	Data = malloc(DataLen);
	MovLen = 3;
	MovData = (unsigned char *)malloc(MovLen);
	ZeroMemory(MovData, MovLen);
	State->PosX = 0;
	State->PosY = 0;
	State->Button = 0;
	GFX::SetFrameskip(-2);
}
} // namespace Controllers