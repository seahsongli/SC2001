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

void printArray(int* arr, size_t nmemb) {
	for (int i = 0; i < nmemb; i++) {
		printf("%d ", arr[i]);
	}
	printf("\n");
}

// to check if the sorting corrupted array space
void checkSum(int* arr, size_t nmemb) {
	static int previousSum = 0;
	if (previousSum == 0) {
		for (int i = 0; i < nmemb; i++) {
			previousSum += arr[i];
		}
	}
	else {
		for (int i = 0; i < nmemb; i++) {
			previousSum -= arr[i];
		}
		if (previousSum != 0) abort();
	}
}

void populate2Rand(int* arr, int* arr2, size_t nmemb) {
	srand((unsigned int)time(NULL));

	for (int i = 0; i < nmemb; i++) {
		arr[i] = (int)((float)rand() / (float)RAND_MAX * X);
		arr2[i] = arr[i];
	}
}

int main() {
	int* arr = NULL;
	// a copy of arr for insertion sort to sort
	int* insArr = NULL;
	Timer* t = NULL;
	double dt = 0.0;

	arr = malloc(NMEMB * sizeof(int));
	insArr = malloc(NMEMB * sizeof(int));
	if (!arr || !insArr) abort();

	for (size_t i = 1; i < 100; i++) {

		populate2Rand(arr, insArr, NMEMB);

		t = startTiming();
		hybridSort(insArr, NMEMB, sizeof(int), cmp, 198);
		dt = stopTiming(t);
		printf_s("%.0lf\t", dt * 1000);

		t = startTiming();
		mergeSort(arr, NMEMB, sizeof(int), cmp);
		dt = stopTiming(t);
		printf_s("%.0lf\n", dt * 1000);
	}
	free(arr);
	free(insArr);

	return 0;
}
