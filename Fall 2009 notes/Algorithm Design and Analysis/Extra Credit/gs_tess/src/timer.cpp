// timer class

#include "timer.h"

Timer::Timer()
{
}

void Timer::init()
{
	QueryPerformanceFrequency(&tps);
	QueryPerformanceCounter(&startpt);
	framestart = startpt;
	start = startpt;
	paused = 0;
}

float Timer::get()
{
	QueryPerformanceCounter(&current);
	float time = ((float)current.QuadPart - (float)start.QuadPart) / (float)tps.QuadPart;
	start = current;
	return time;
}

float Timer::getelapsed()
{
	if (paused)
	{
		return ((float)pausept.QuadPart - (float)startpt.QuadPart) / (float)tps.QuadPart;
	}
	else
	{
		QueryPerformanceCounter(&current);
		return ((float)current.QuadPart - (float)startpt.QuadPart) / (float)tps.QuadPart;
	}
}

float Timer::frametime()
{
	QueryPerformanceCounter(&current);
	float time = ((float)current.QuadPart - (float)framestart.QuadPart) / (float)tps.QuadPart;
	framestart = current;
	return time;
}

void Timer::pause()
{
	paused = 1;
	QueryPerformanceCounter(&pausept);
}

void Timer::unpause()
{
	paused = 0;
	QueryPerformanceCounter(&current);
	startpt.QuadPart += current.QuadPart - pausept.QuadPart;
}