#include <stdio.h>
#include <time.h>
#include "ins.h"
#include <math.h>
#include <Windows.h>
#include "Benchmarker.h"

/* Compliant to Project Specification */
#define X ((int)1'000'000)
#define NMEMB ((size_t)10'000'000)


int cmp(const void* l, const void* r) {
	return *(const int*)l - *(const int*)r;
}

// To generate shuffled arrays without duplicate keys.
// The maximum value in an arr of length-nmemb is nmemb - 1;
// might have deviated from the project specification but fuck it.
void populateInc(int* arr, size_t nmemb) {
	for (size_t i = 0; i < nmemb; i++) {
		arr[i] = i;
	}
}

void distinctArray(int *arr, size_t nmemb) {
	populateInc(arr, nmemb);
	srand((unsigned int)clock());

	for (size_t i = nmemb - 1; i > 0; i--) {
		size_t j = (size_t)((float)rand() / (float)RAND_MAX * X) % (i + 1);
		int temp = arr[i];
		arr[i] = arr[j];
		arr[j] = temp;
	}
}


void printArray(int* arr, size_t nmemb) {
	for (int i = 0; i < nmemb; i++) {
		printf("%d\n", arr[i]);
	}
	printf("\n");
}

// ./scripts/hcmpcnt.py
void countHybrid() {
	for (size_t nmemb = 1000; nmemb <= 2E7; nmemb *= 1.25) {
		int* arr = malloc(nmemb * sizeof(int));
		distinctArray(arr, nmemb);

		hybridSort(arr, nmemb, sizeof(int), cmp, 2);
		printf_s("%zu\t%zu\n", nmemb, cmpcnt);
		free(arr);
	}
}

// ./scripts/thresholds.py
void tryThresholds() {
	for (int i = 3; i <= 7; i++) {
		size_t nmemb = (size_t)pow((double)10, (double)i);
		int* arr = malloc(nmemb * sizeof(int));
		int* copy = malloc(nmemb * sizeof(int));
		distinctArray(arr, nmemb);

		for (size_t s = 1; s <= 100; s++) {
			// sort a copy, leaving the dataset untouched
			memcpy_s(copy, nmemb * sizeof(int), arr, nmemb * sizeof(int));

			hybridSort(copy, nmemb, sizeof(int), cmp, s);
			printf_s("%zu\t%zu\n", s, cmpcnt);

		}
		// EOD
		printf_s("%d\t%d\n", -1, -1);
		free(arr);
		free(copy);
	}
}


void compareMergeHybrid_cmpcnt() {
	const size_t nmemb = 1'000'000;
	int* arr = malloc(nmemb * sizeof(int));
	int* copy = malloc(nmemb * sizeof(int));
	distinctArray(arr, nmemb);
	memcpy_s(copy, nmemb * sizeof(int), arr, nmemb * sizeof(int));

	mergeSort(copy, nmemb, sizeof(int), cmp);
	const size_t mCount = cmpcnt;

	for (size_t s = 1; s <= 50; s++) {
		memcpy_s(copy, nmemb * sizeof(int), arr, nmemb * sizeof(int));
		hybridSort(copy, nmemb, sizeof(int), cmp, s);
		printf_s("%zu\t%zu\t%zu\n", s, cmpcnt, mCount);
	}

	free(arr);
	free(copy);
}

void timedTryThresholds() {
	for (int i = 3; i <= 7; i++) {
		size_t nmemb = (size_t)pow((double)10, (double)i);
		int* arr = malloc(nmemb * sizeof(int));
		int* copy = malloc(nmemb * sizeof(int));
		distinctArray(arr, nmemb);

		for (size_t s = 1; s <= 80; s++) {
			// sort a copy, leaving the dataset untouched
			memcpy_s(copy, nmemb * sizeof(int), arr, nmemb * sizeof(int));

			Timer* t = startTiming();
			hybridSort(copy, nmemb, sizeof(int), cmp, s);
			double dt = stopTiming(t);
			printf_s("%zu\t%.0lf\n", s, dt * 1000 * 1000);

		}
		// EOD
		printf_s("%d\t%d\n", -1, -1);
		free(arr);
		free(copy);
	}
}

// ./scripts/boxplots.py
void compareMergeHybrid() {
	int* arr1 = NULL;
	int* arr2 = NULL;
	Timer* t = NULL;
	double dt = 0.0;

	const size_t i = 1'000'000;
	for (size_t k = 0; k < 100; k++) {
		arr1 = malloc(i * sizeof(int));
		arr2 = malloc(i * sizeof(int));
		if (!arr1 || !arr2) abort();

		distinctArray(arr1, i);
		memcpy_s(arr2, i * sizeof(int), arr1, i * sizeof(int));

		Timer* t = startTiming();
		hybridSort(arr1, i, sizeof(int), cmp, OPTIMAL_THRESHOLD);
		double dt = stopTiming(t);
		printf_s("%.0lf\t", dt * 1000 * 1000);

		t = startTiming();
		mergeSort(arr2, i, sizeof(int), cmp);
		dt = stopTiming(t);
		printf_s("%.0lf\n", dt * 1000 * 1000);

		free(arr1);
		free(arr2);
	}
}

int main() {
	compareMergeHybrid();

	return 0;
}


//void populateRand(int* arr, size_t nmemb) {
//	srand((unsigned int)clock());
//
//	for (int i = 0; i < nmemb; i++) {
//		arr[i] = 0;
//		for (int b = 30; b >= 0; b--) {
//			arr[i] |= (rand() << 16 | rand()) & (1 << b);
//			printf_s("%d\n", arr[i]);
//		}
//	}
//}
