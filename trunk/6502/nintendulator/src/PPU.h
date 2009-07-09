/* Nintendulator - Win32 NES emulator written in C++
 * Copyright (C) 2002-2009 QMT Productions
 *
 * $URL: https://nintendulator.svn.sourceforge.net/svnroot/nintendulator/nintendulator/trunk/src/PPU.h $
 * $Id: PPU.h 996 2009-05-23 02:02:20Z Quietust $
 */

#ifndef PPU_H
#define PPU_H

#define	ACCURATE_SPRITES	/* enable cycle-accurate sprite evaluation logic */

namespace PPU
{
extern FPPURead	ReadHandler[0x10];
extern FPPUWrite	WriteHandler[0x10];
extern int SLEndFrame;
extern int Clockticks;
extern int SLnum;
extern unsigned char *CHRPointer[0x10];
extern BOOL Writable[0x10];

#ifdef	ACCURATE_SPRITES
extern unsigned char Sprite[0x120];
#else	/* !ACCURATE_SPRITES */
extern unsigned char Sprite[0x100];
#endif	/* ACCURATE_SPRITES */

extern unsigned char Palette[0x20];

extern unsigned char Reg2000;
	
extern unsigned char IsRendering, OnScreen;

extern unsigned long VRAMAddr;

extern BOOL IsPAL;
extern unsigned char	VRAM[0x4][0x400];
extern unsigned char	OpenBus[0x400];
extern unsigned short	DrawArray[256*240];

void	GetHandlers (void);
void	PowerOn (void);
void	Reset (void);
int	Save (FILE *);
int	Load (FILE *);
int	MAPINT	IntRead (int, int);
void	MAPINT	IntWrite (int, int, int);
void	Run (void);
void	GetGFXPtr (void);

int	MAPINT	BusRead (int, int);
void	MAPINT	BusWriteCHR (int, int, int);
void	MAPINT	BusWriteNT (int, int, int);
} // namespace PPU
#endif	/* !PPU_H */
