#include "ins.h"

/*
* Roughly equivalent to an array subscript, but this works best when type information 
* is not available.
*/
#define getEAddr(base, typeSz, offset) (void*)(((char*)base) + (offset) * (typeSz))

typedef struct swapperSlot {
	void* slot;
} swapperSlot;


// Comparison count. Must be cleared upon top-level entries.
extern volatile size_t cmpcnt = 0;


/* GENERAL STATICS */
  
static swapperSlot s = { 0 };

static void swapInit(size_t typeSz) {
	/* unbalanced management of swapperSlot */
	if (s.slot != NULL) abort();
	s.slot = malloc(typeSz);
}

static void swapFree() {
	free(s.slot);
	s.slot = NULL;
}

static inline void swap(void* a, void* b, size_t typeSz) {
	// there should be a more efficient way to do this
	memcpy(s.slot, a, typeSz);
	memcpy(a, b, typeSz);
	memcpy(b, s.slot, typeSz);
}



/* INSERTION SORT */

static void _insertionSort(void* arr, size_t nmemb, size_t membSz, comparator compare) {
	for (int i = 1; i < nmemb; i++) {
		for (int j = i; j >= 1; j--) {
			void* l = getEAddr(arr, membSz, j - 1);
			void* r = getEAddr(arr, membSz, j);
			cmpcnt++;
			if (compare(l, r) < 0) swap(l, r, membSz);
			else break;
		}
	}
}

/* 
* Exposed signature, wrapper for comparison count and SwapperSlot initialisations 
* (to allow _hybridSort to call this procedure without errors in comparison counting) 
*/
void insertionSort(void* arr, size_t nmemb, size_t membSz, comparator compare) {
	cmpcnt ^= cmpcnt;
	swapInit(membSz);
	_insertionSort(arr, nmemb, membSz, compare);
	swapFree();
}



/* MERGE SORT */

/* MERGE HELPER (CORE) */
static void merge(void* arr, size_t nmemb, size_t membSz, comparator compare) {
	// re-evaluate this to avoid stack arguments (?)
	size_t mid = (nmemb - 1) >> 1;

	size_t curl = 0;
	size_t curr = mid + 1;
	// We will use an auxilliary storage to avoid rotations
	/* 
	* Perhaps this allocation can be done in MergeSort, and
	* maintained through a global variable. But at this point 
	* the overhead of a call to malloc is negligible and the 
	* discussion thereof is trivial.
	*/
	void* sorted = malloc(nmemb * membSz);
	if (!sorted) abort();
	size_t sortedTop = 0;

	while (curl <= mid && curr <= nmemb - 1) {
		void* l = getEAddr(arr, membSz, curl);
		void* r = getEAddr(arr, membSz, curr);
		int res = compare(l, r);
		cmpcnt++;

		if (res < 0) {
			memcpy(getEAddr(sorted, membSz, sortedTop++), r, membSz);
			curr++;
		}
		else if (res == 0) {
			memcpy(getEAddr(sorted, membSz, sortedTop++), l, membSz);
			memcpy(getEAddr(sorted, membSz, sortedTop++), r, membSz);
			curr++;
			curl++;
		}
		else {
			memcpy(getEAddr(sorted, membSz, sortedTop++), l, membSz);
			curl++;
		}
	}

	/* 
	* Only one of the following memmove's can move a nonzero amount of bytes,
	* as the preceding loop conditions implied; may create assertions for debug purpose
	*/
	memmove(getEAddr(arr, membSz, sortedTop), getEAddr(arr, membSz, curl), (mid - curl + 1) * membSz);
	memmove(getEAddr(arr, membSz, sortedTop), getEAddr(arr, membSz, curr), (nmemb - curr) * membSz);

	memcpy(arr, sorted, sortedTop * membSz);

	free(sorted);
}

static void _mergeSort(void* arr, size_t nmemb, size_t membSz, comparator compare) {
	// ASSERTION: sign(nmemb) == 0
	if (nmemb <= 1) return;

	// (start - stop) / 2
	size_t mid = (nmemb - 1) >> 1;

	_mergeSort(arr, mid + 1, membSz, compare);
	_mergeSort(getEAddr(arr, membSz, mid + 1), nmemb - (mid + 1), membSz, compare);

	merge(arr, nmemb, membSz, compare);
}

/* Exposed signature, wrapper for comparison count initialisation */
void mergeSort(void* arr, size_t nmemb, size_t membSz, comparator compare) {
	cmpcnt ^= cmpcnt;
	_mergeSort(arr, nmemb, membSz, compare);
}



/* HYBRID SORT */

static void _hybridSort(void* arr, size_t nmemb, size_t membSz, comparator compare, size_t threshold) {
	// ASSERTION: sign(nmemb) == 0
	if (nmemb <= 1) return;

	// Sort small lists using insertion sort to avoid recursion overhead
	if (nmemb <= threshold) {
		_insertionSort(arr, nmemb, membSz, compare);
		return;
	}

	// (start - stop) / 2
	size_t mid = (nmemb - 1) >> 1;

	_hybridSort(arr, mid + 1, membSz, compare, threshold);
	_hybridSort(getEAddr(arr, membSz, mid + 1), nmemb - (mid + 1), membSz, compare, threshold);

	merge(arr, nmemb, membSz, compare);
}

/* Exposed signature, wrapper for comparison count and SwapperSlot initialisation */
void hybridSort(void* arr, size_t nmemb, size_t membSz, comparator compare, size_t threshold) {
	cmpcnt ^= cmpcnt;
	swapInit(membSz);
	_hybridSort(arr, nmemb, membSz, compare, threshold);
	swapFree();
}


