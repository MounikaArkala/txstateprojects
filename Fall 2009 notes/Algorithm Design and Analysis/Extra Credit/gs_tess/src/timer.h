#ifndef TIMER_H
#define TIMER_H

// timer class

#define _WINSOCKAPI_ // prevent winsock.h
#include <windows.h>

class Timer
{
public:

	Timer();

	void init();
	float getelapsed();
	float get();
	float frametime();
	void pause();
	void unpause();

private:

	LARGE_INTEGER startpt, start, current, tps, framestart, pausept;
	int paused;
};

#endif