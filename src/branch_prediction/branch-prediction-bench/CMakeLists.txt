cmake_minimum_required(VERSION 3.16)
project(branch_prediction CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Shared implementation objects
add_library(branch_impls OBJECT
    naive.cpp
    sorted.cpp
    branchless.cpp
    ternary.cpp
    bench_harness.cpp
)

# ── Combined benchmark (all implementations) ──────────────────────────────────
foreach(OPT O0 O2 O3)
    add_executable(bench_all_${OPT} main.cpp $<TARGET_OBJECTS:branch_impls>)
    if(OPT STREQUAL "O0")
        target_compile_options(bench_all_${OPT} PRIVATE -O0 -g)
    elseif(OPT STREQUAL "O2")
        target_compile_options(bench_all_${OPT} PRIVATE -O2 -g)
    else()
        target_compile_options(bench_all_${OPT} PRIVATE -O3 -mavx2 -g)
    endif()
endforeach()

# ── Standalone targets – one per implementation, for perf / VTune ─────────────
# Each standalone is built at O0, O2 and O3 so you can compare assembly.

set(STANDALONE_TARGETS
    naive:main_naive.cpp:naive.cpp
    sorted:main_sorted.cpp:sorted.cpp
    branchless:main_branchless.cpp:branchless.cpp
    ternary:main_ternary.cpp:ternary.cpp
)

foreach(ENTRY ${STANDALONE_TARGETS})
    string(REPLACE ":" ";" PARTS ${ENTRY})
    list(GET PARTS 0 NAME)
    list(GET PARTS 1 MAIN_SRC)
    list(GET PARTS 2 IMPL_SRC)

    foreach(OPT O0 O2 O3)
        set(TARGET bench_${NAME}_${OPT})
        add_executable(${TARGET} ${MAIN_SRC} ${IMPL_SRC})
        if(OPT STREQUAL "O0")
            target_compile_options(${TARGET} PRIVATE -O0 -g)
        elseif(OPT STREQUAL "O2")
            target_compile_options(${TARGET} PRIVATE -O2 -g)
        else()
            target_compile_options(${TARGET} PRIVATE -O3 -mavx2 -g)
        endif()
    endforeach()
endforeach()
