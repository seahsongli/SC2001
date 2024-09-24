#include "Benchmarker.h"

static LARGE_INTEGER f = { 0 };

struct Timer {
	LARGE_INTEGER initialTick;
	LARGE_INTEGER finalTick;
	LARGE_INTEGER performanceFrequency;
};

Timer* startTiming() {
	if (!f.QuadPart) QueryPerformanceFrequency(&f);
	
	Timer* timer = malloc(sizeof(Timer));
	if (!timer) abort();

	timer->performanceFrequency = f;
	QueryPerformanceCounter(&timer->initialTick);
	return timer;
}

double stopTiming(Timer* hTimer) {
	QueryPerformanceCounter(&hTimer->finalTick);
	double expense = (double)(hTimer->finalTick.QuadPart - hTimer->initialTick.QuadPart) / hTimer->performanceFrequency.QuadPart;
	free(hTimer);
	return expense;
}