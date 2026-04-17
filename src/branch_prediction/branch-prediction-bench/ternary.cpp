#include "ternary.h"
#include "common.h"

long solve_ternary(const int* arr, int n) {
    long total = 0;
    for (int r = 0; r < REPEATS; r++)
        for (int i = 0; i < n; i++) {
            int val = arr[i];
            total += (val > 128) ? val : 0;
        }
    return total;
}
