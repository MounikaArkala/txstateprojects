/* Nintendulator - Win32 NES emulator written in C++
 * Copyright (C) 2002-2009 QMT Productions
 *
 * Based on NinthStar, a portable Win32 NES Emulator written in C++
 * Copyright (C) 2000  David de Regt
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * $URL: https://nintendulator.svn.sourceforge.net/svnroot/nintendulator/nintendulator/trunk/src/Nintendulator.h $
 * $Id: Nintendulator.h 996 2009-05-23 02:02:20Z Quietust $
 */

#ifndef NINTENDULATOR_H
#define NINTENDULATOR_H

#define	ENABLE_DEBUGGER
/*#define	CPU_BENCHMARK */

extern	HINSTANCE	hInst;	/* current instance */
extern	HWND		hMainWnd;	/* main window */
extern	HMENU		hMenu;	/* main window menu */
extern	HACCEL		hAccelTable;	/* accelerators */

extern	BOOL		MaskKeyboard;	/* mask keyboard accelerators (for when Family Basic Keyboard is active) */
extern	HWND		hDebug;		/* Debug Info window */
extern	BOOL		dbgVisible;	/* whether or not the Debug window is open */

extern	int		SizeMult;	/* window size multiplier */
extern	TCHAR		ProgPath[MAX_PATH];	/* program path */
extern	TCHAR		DataPath[MAX_PATH];	/* data path */

extern	TCHAR		Path_ROM[MAX_PATH];
extern	TCHAR		Path_NMV[MAX_PATH];
extern	TCHAR		Path_AVI[MAX_PATH];
extern	TCHAR		Path_PAL[MAX_PATH];

extern	void		SetWindowClientArea (HWND hWnd, int w, int h);
extern	BOOL		ProcessMessages	(void);

extern	TCHAR		TitlebarBuffer[256];
extern	int		TitlebarDelay;
extern	void		UpdateTitlebar (void);
extern	void	__cdecl	PrintTitlebar (TCHAR *Text, ...);
extern	void		AddDebug (TCHAR *txt);

// Shortcut macros for use in savestate code
#define	writeByte(val) { register unsigned char _val = val; fwrite(&_val, 1, 1, out); clen++; }
#define	writeWord(val) { register unsigned short _val = val; fwrite(&_val, 2, 1, out); clen += 2; }
#define	writeLong(val) { register unsigned long _val = val; fwrite(&_val, 4, 1, out); clen += 4; }
#define	writeArray(val,len) { register int _len = len; fwrite(val, 1, _len, out); clen += _len; }

#define	readByte(val) { register unsigned char _val; fread(&_val, 1, 1, in); val = _val; clen++; }
#define	readWord(val) { register unsigned short _val; fread(&_val, 2, 1, in); val = _val; clen += 2; }
#define	readLong(val) { register unsigned long _val; fread(&_val, 4, 1, in); val = _val; clen += 4; }
#define	readArray(val,len) { register int _len = len; fread(val, 1, _len, in); clen += _len; }
#define	readArraySkip(val,inlen,outlen) { register int readLen = min(inlen, outlen); fread(val, 1, readLen, in); if (inlen > readLen) fseek(in, inlen - readLen, SEEK_CUR); if (outlen > readLen) ZeroMemory((unsigned char *)val + readLen, outlen - readLen); clen += inlen; }

#endif	/* !NINTENDULATOR_H */
