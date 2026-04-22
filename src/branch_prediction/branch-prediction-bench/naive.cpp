#include "naive.h"
#include "common.h"

long solve_naive(const int* arr, int n) {
    long total = 0;
    for (int r = 0; r < REPEATS; r++)
        for (int i = 0; i < n; i++)
            if (arr[i] > 128)
                total += arr[i];
    return total;
}
