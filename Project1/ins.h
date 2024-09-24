#ifndef INS_H
#define INS_H

/*
* O Lord, forgive me, for I am about to sin.
*/

#include <stdlib.h>
#include <string.h>

volatile size_t cmpcnt;

/*
* The return value of a comparator must be:
* - <0, when the item on the right must be put at a lower index than that on the left;
* - 0, when both items are of the same order;
* - >0, when the item on the right must be put at a higher index than that on the left.
*/
typedef int (*comparator)(const void* l, const void* r);
typedef void (*sorter)(void* arr, size_t nmemb, size_t membSz, comparator compare);

void insertionSort(void* arr, size_t nmemb, size_t membSz, comparator compare);
void mergeSort(void* arr, size_t nmemb, size_t membSz, comparator compare);
void hybridSort(void* arr, size_t nmemb, size_t membSz, comparator compare, size_t threshold);

#endif /* INS_H */