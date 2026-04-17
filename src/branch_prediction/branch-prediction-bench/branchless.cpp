#include "branchless.h"
#include "common.h"

long solve_branchless(const int* arr, int n) {
    long total = 0;
    for (int r = 0; r < REPEATS; r++)
        for (int i = 0; i < n; i++) {
            int val = arr[i];
            total += val * (val > 128);
        }
    return total;
}
