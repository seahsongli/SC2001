#ifndef BENCHMARKER_H
#define BENCHMARKER_H

#include <Windows.h>
#include <stdlib.h>

typedef struct Timer Timer;

Timer* startTiming();
double stopTiming(Timer* hTimer);

#endif /* BENCHMARKER_H */
