#pragma once

static constexpr int  N                 = 100'000;
static constexpr int  REPEATS           = 100;
static constexpr int  RUNS              = 7;
// Deterministic result for N=100000, REPEATS=100, seed=42, dist [0,255], threshold >128
static constexpr long EXPECTED_CHECKSUM = 951'163'500L;
