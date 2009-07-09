/* Nintendulator - Win32 NES emulator written in C++
 * Copyright (C) 2002-2009 QMT Productions
 *
 * $URL: https://nintendulator.svn.sourceforge.net/svnroot/nintendulator/nintendulator/trunk/src/States.h $
 * $Id: States.h 996 2009-05-23 02:02:20Z Quietust $
 */

#ifndef STATES_H
#define STATES_H

#define	STATES_VERSION	"0965"
#define	STATES_BETA	"0965"
#define	STATES_PREV	"0960"

namespace States
{
extern TCHAR BaseFilename[MAX_PATH];
extern int SelSlot;

void	Init (void);
void	SetFilename (TCHAR *);
void	SetSlot (int Slot);
int	SaveData (FILE *);
BOOL	LoadData (FILE *, int);
void	SaveState (void);
void	LoadState (void);
} // namespace States
#endif	/* !STATES_H */
