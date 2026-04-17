#pragma once

// Branchless – multiply by boolean; compiler emits cmov/setg, no jump
long solve_branchless(const int* arr, int n);
