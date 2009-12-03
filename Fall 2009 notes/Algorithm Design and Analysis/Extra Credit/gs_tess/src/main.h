#ifndef MAIN_H
#define MAIN_H

//#define WIN32_LEAN_AND_MEAN
#define _WINSOCKAPI_ // prevent winsock.h
#define _WIN32_WINNT 0x500 // for readdirectorychangesw
#include <windows.h>
#include <stdio.h>
#include <io.h>
#include <memory.h>
#include <malloc.h>
#include <vector>
#include <deque>
#include <set>
#include <algorithm>
#include <string>
#include "timer.h"
#include "vector3.h"
#include "matrix.h"
#include "random.h"
#include "util.h"
#include "debug_util.h"

extern int use_sound;

// framerate tracking
#define FPS_FRAMES 30
extern float averagefps;
extern float fps[FPS_FRAMES];
//extern float frametime;
extern float elapsedtime;
extern Timer timer;


#endif