#ifndef DEBUG_UTIL_H
#define DEBUG_UTIL_H

// enable debug output
#define DEBUG_ENABLED


#ifdef DEBUG_ENABLED


#define DebugPrint(...) _DebugPrint(__VA_ARGS__)

void _DebugPrint(const char *format, ...);

#else


#define DebugPrint(...)


#endif // DEBUG_ENABLED


#endif // DEBUG_UTIL_H