#include "sorted.h"
#include "common.h"
#include <algorithm>

long solve_sorted(int* arr, int n) {
    std::sort(arr, arr + n);
    long total = 0;
    for (int r = 0; r < REPEATS; r++)
        for (int i = 0; i < n; i++)
            if (arr[i] > 128)
                total += arr[i];
    return total;
}
