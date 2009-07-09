/* Nintendulator - Win32 NES emulator written in C++
 * Copyright (C) 2002-2009 QMT Productions
 *
 * $URL: https://nintendulator.svn.sourceforge.net/svnroot/nintendulator/nintendulator/trunk/src/States.cpp $
 * $Id: States.cpp 996 2009-05-23 02:02:20Z Quietust $
 */

#include "stdafx.h"
#include "Nintendulator.h"
#include "resource.h"
#include "MapperInterface.h"
#include "NES.h"
#include "States.h"
#include "CPU.h"
#include "PPU.h"
#include "APU.h"
#include "Movie.h"
#include "Controllers.h"
#include "GFX.h"
#include "Genie.h"

namespace States
{
	TCHAR BaseFilename[MAX_PATH];
	int SelSlot;

//extern FILE *movie;

void	Init (void)
{
	SelSlot = 0;
}

void	SetFilename (TCHAR *Filename)
{
	// all we need is the base filename
	_tsplitpath(Filename, NULL, NULL, BaseFilename, NULL);
}

void	SetSlot (int Slot)
{
	TCHAR tpchr[MAX_PATH];
	FILE *tmp;
	SelSlot = Slot;
	_stprintf(tpchr, _T("%s\\States\\%s.ns%i"), DataPath, BaseFilename, SelSlot);
	tmp = _tfopen(tpchr, _T("rb"));
	if (tmp)
	{
		fclose(tmp);
		PrintTitlebar(_T("State Selected: %i (occupied)"), Slot);
	}
	else	PrintTitlebar(_T("State Selected: %i (empty)"), Slot);
}

int	SaveData (FILE *out)
{
	int flen = 0, clen;
	{
		fwrite("CPUS", 1, 4, out);	flen += 4;
		fwrite(&clen, 4, 1, out);	flen += 4;
		clen = CPU::Save(out);
		fseek(out, -clen - 4, SEEK_CUR);
		fwrite(&clen, 4, 1, out);
		fseek(out, clen, SEEK_CUR);	flen += clen;
	}
	{
		fwrite("PPUS", 1, 4, out);	flen += 4;
		fwrite(&clen, 4, 1, out);	flen += 4;
		clen = PPU::Save(out);
		fseek(out, -clen - 4, SEEK_CUR);
		fwrite(&clen, 4, 1, out);
		fseek(out, clen, SEEK_CUR);	flen += clen;
	}
	{
		fwrite("APUS", 1, 4, out);	flen += 4;
		fwrite(&clen, 4, 1, out);	flen += 4;
		clen = APU::Save(out);
		fseek(out, -clen - 4, SEEK_CUR);
		fwrite(&clen, 4, 1, out);
		fseek(out, clen, SEEK_CUR);	flen += clen;
	}
	{
		fwrite("CONT", 1, 4, out);	flen += 4;
		fwrite(&clen, 4, 1, out);	flen += 4;
		clen = Controllers::Save(out);
		fseek(out, -clen - 4, SEEK_CUR);
		fwrite(&clen, 4, 1, out);
		fseek(out, clen, SEEK_CUR);	flen += clen;
	}
	if (Genie::CodeStat & 1)
	{
		fwrite("GENI", 1, 4, out);	flen += 4;
		fwrite(&clen, 4, 1, out);	flen += 4;
		clen = Genie::Save(out);
		fseek(out, -clen - 4, SEEK_CUR);
		fwrite(&clen, 4, 1, out);
		fseek(out, clen, SEEK_CUR);	flen += clen;
	}
	{
		for (clen = sizeof(NES::PRG_RAM) - 1; clen >= 0; clen--)
			if (NES::PRG_RAM[clen >> 12][clen & 0xFFF])
				break;
		if (clen >= 0)
		{
			clen++;
			fwrite("NPRA", 1, 4, out);		flen += 4;
			fwrite(&clen, 4, 1, out);		flen += 4;
			fwrite(NES::PRG_RAM, 1, clen, out);	flen += clen;	//	PRAM	uint8[...]	PRG_RAM data
		}
	}
	{
		for (clen = sizeof(NES::CHR_RAM) - 1; clen >= 0; clen--)
			if (NES::CHR_RAM[clen >> 10][clen & 0x3FF])
				break;
		if (clen >= 0)
		{
			clen++;
			fwrite("NCRA", 1, 4, out);		flen += 4;
			fwrite(&clen, 4, 1, out);		flen += 4;
			fwrite(NES::CHR_RAM, 1, clen, out);	flen += clen;	//	CRAM	uint8[...]	CHR_RAM data
		}
	}
	if (RI.ROMType == ROM_FDS)
	{
		fwrite("DISK", 1, 4, out);	flen += 4;
		fwrite(&clen, 4, 1, out);	flen += 4;
		clen = NES::FDSSave(out);
		fseek(out, -clen - 4, SEEK_CUR);
		fwrite(&clen, 4, 1, out);
		fseek(out, clen, SEEK_CUR);	flen += clen;
	}
	{
		if ((MI) && (MI->SaveLoad))
			clen = MI->SaveLoad(STATE_SIZE, 0, NULL);
		else	clen = 0;
		if (clen)
		{
			unsigned char *tpmi = (unsigned char *)malloc(clen);
			MI->SaveLoad(STATE_SAVE, 0, tpmi);
			fwrite("MAPR", 1, 4, out);	flen += 4;
			fwrite(&clen, 4, 1, out);	flen += 4;
			fwrite(tpmi, 1, clen, out);	flen += clen;	//	CUST	uint8[...]	Custom mapper data
			free(tpmi);
		}
	}
	if (Movie::Mode)	// save state when recording, reviewing, OR playing
	{
		fwrite("NMOV", 1, 4, out);	flen += 4;
		fwrite(&clen, 4, 1, out);	flen += 4;
		clen = Movie::Save(out);
		fseek(out, -clen - 4, SEEK_CUR);
		fwrite(&clen, 4, 1, out);
		fseek(out, clen, SEEK_CUR);	flen += clen;
	}
	return flen;
}

void	SaveState (void)
{
	TCHAR tps[MAX_PATH];
	int flen;
	FILE *out;

	if (Genie::CodeStat & 0x80)
	{
		PrintTitlebar(_T("Cannot save state at the Game Genie code entry screen!"));
		return;
	}

	_stprintf(tps, _T("%s\\States\\%s.ns%i"), DataPath, BaseFilename, SelSlot);
	out = _tfopen(tps, _T("w+b"));
	flen = 0;

	fwrite("NSS\x1A", 1, 4, out);
	fwrite(STATES_VERSION, 1, 4, out);
	fwrite(&flen, 4, 1, out);
	if (Movie::Mode)	// save NREC during playback as well
		fwrite("NREC", 1, 4, out);
	else	fwrite("NSAV", 1, 4, out);

	flen = SaveData(out);

	// Write final filesize
	fseek(out, 8, SEEK_SET);
	fwrite(&flen, 4, 1, out);
	fclose(out);

	PrintTitlebar(_T("State saved: %i"), SelSlot);
	Movie::ShowFrame();
}

BOOL	LoadData (FILE *in, int flen)
{
	char csig[4];
	int clen;
	BOOL SSOK = TRUE;
	fread(&csig, 1, 4, in);	flen -= 4;
	fread(&clen, 4, 1, in);	flen -= 4;
	while (flen > 0)
	{
		flen -= clen;
		if (!memcmp(csig, "CPUS", 4))
			clen -= CPU::Load(in);
		else if (!memcmp(csig, "PPUS", 4))
			clen -= PPU::Load(in);
		else if (!memcmp(csig, "APUS", 4))
			clen -= APU::Load(in);
		else if (!memcmp(csig, "CONT", 4))
			clen -= Controllers::Load(in);
		else if (!memcmp(csig, "GENI", 4))
			clen -= Genie::Load(in);
		else if (!memcmp(csig, "NPRA", 4))
		{
			memset(NES::PRG_RAM, 0, sizeof(NES::PRG_RAM));
			fread(NES::PRG_RAM, 1, clen, in);	clen = 0;
		}
		else if (!memcmp(csig, "NCRA", 4))
		{
			memset(NES::CHR_RAM, 0, sizeof(NES::CHR_RAM));
			fread(NES::CHR_RAM, 1, clen, in);	clen = 0;
		}
		else if (!memcmp(csig, "DISK", 4))
		{
			if (RI.ROMType == ROM_FDS)
				clen -= NES::FDSLoad(in);
			else	EI.DbgOut(_T("Error - DISK save block found for non-FDS game!"));
		}
		else if (!memcmp(csig, "MAPR", 4))
		{
			if ((MI) && (MI->SaveLoad))
			{
				int len = MI->SaveLoad(STATE_SIZE, 0, NULL);
				unsigned char *tpmi = (unsigned char *)malloc(len);
				fread(tpmi, 1, len, in);		//	CUST	uint8[...]	Custom mapper data
				MI->SaveLoad(STATE_LOAD, 0, tpmi);
				free(tpmi);
				clen -= len;
			}
		}
		else if (!memcmp(csig, "NMOV", 4))
			clen -= Movie::Load(in);
		if (clen != 0)
		{
			SSOK = FALSE;			// too much, or too little
			fseek(in, clen, SEEK_CUR);	// seek back to the block boundary
		}
		if (flen > 0)
		{
			fread(&csig, 1, 4, in);	flen -= 4;
			fread(&clen, 4, 1, in);	flen -= 4;
		}
	}
	return SSOK;
}

void	LoadState (void)
{
	TCHAR tps[MAX_PATH];
	char tpc[5];
	FILE *in;
	int flen;

	_stprintf(tps, _T("%s\\States\\%s.ns%i"), DataPath, BaseFilename, SelSlot);
	in = _tfopen(tps, _T("rb"));
	if (!in)
	{
		PrintTitlebar(_T("No such save state: %i"), SelSlot);
		return;
	}

	fread(tpc, 1, 4, in);
	if (memcmp(tpc, "NSS\x1a", 4))
	{
		fclose(in);
		PrintTitlebar(_T("Not a valid savestate file: %i"), SelSlot);
		return;
	}
	fread(tpc, 1, 4, in);
	if ((memcmp(tpc, STATES_VERSION, 4)) && (memcmp(tpc, STATES_BETA,4)) && (memcmp(tpc, STATES_PREV, 4)))
	{
		fclose(in);
		tpc[4] = 0;
		PrintTitlebar(_T("Incorrect savestate version (%hs): %i"), tpc, SelSlot);
		return;
	}
	fread(&flen, 4, 1, in);
	fread(tpc, 1, 4, in);

	if (!memcmp(tpc, "NMOV", 4))
	{
		fclose(in);
		PrintTitlebar(_T("Selected savestate (%i) is a movie file - cannot load!"), SelSlot);
		return;
	}
	else if (!memcmp(tpc, "NREC", 4))
	{
		// Movie savestate, can always load these
	}
	else if (!memcmp(tpc, "NSAV", 4))
	{
		// Non-movie savestate, can NOT load these while a movie is open
		if (Movie::Mode)
		{
			fclose(in);
			PrintTitlebar(_T("Selected savestate (%i) does not contain movie data!"), SelSlot);
			return;
		}
	}
	else
	{
		fclose(in);
		tpc[4] = 0;
		PrintTitlebar(_T("Selected savestate (%i) has unknown type! (%hs)"), SelSlot, tpc);
		return;
	}

	fseek(in, 16, SEEK_SET);
	NES::Reset(RESET_SOFT);

	if (Movie::Mode & MOV_REVIEW)		// If the user is reviewing an existing movie
		Movie::Mode = MOV_RECORD;	// then resume recording once they LOAD state

	NES::GameGenie = FALSE;			// If the savestate uses it, it'll turn back on shortly
	CheckMenuItem(hMenu, ID_CPU_GAMEGENIE, MF_UNCHECKED);

	if (LoadData(in, flen))
		PrintTitlebar(_T("State loaded: %i"), SelSlot);
	else	PrintTitlebar(_T("State loaded with errors: %i"), SelSlot);
	Movie::ShowFrame();
	fclose(in);
}
} // namespace States