# MCP Server Use Case Examples

Here are practical examples of how to use the CPU Optimization RAG MCP server with Continue.dev:

## 1. Learning Path Discovery

**You ask Continue:**
> "I'm new to CPU optimization. What should I learn first?"

**Continue uses** `get_learning_path` tool with `level: "beginner"`

**You get:**
- Lab 1: Cache Optimization
- Lab 2: Branch Prediction  
- Lab 3: SIMD Basics

Complete with durations, topics, and speedup targets for each lab.

---

## 2. Topic Research

**You ask Continue:**
> "Find resources about SIMD vectorization"

**Continue uses** `search_optimization_topics` tool with `query: "SIMD"`

**You get:**
- Books: "SIMD for C++ Developers"
- Online Resources: Intel Intrinsics Guide
- Projects: Google Highway, EVE
- Labs: Lab 3 (SIMD Basics), Lab 6 (Highway SIMD Library), Lab 7 (Advanced Vectorization)

---

## 3. Specific Lab Information

**You ask Continue:**
> "Tell me about lab 5"

**Continue uses** `get_lab_info` tool with `labNumber: 5`

**You get:**
```json
{
  "title": "Data Structures for Performance",
  "duration": "2-3 hours",
  "topics": ["data structures", "SoA", "AoS", "cache-friendly layouts"],
  "description": "Design data structures optimized for modern CPU architectures",
  "level": "intermediate",
  "speedupTargets": {
    "basic": "2x",
    "good": "5x", 
    "excellent": "10x+"
  }
}
```

---

## 4. Platform-Specific Tooling

**You ask Continue:**
> "What profiling tools should I use on Linux?"

**Continue uses** `get_profiling_tools` tool with `platform: "linux"`

**You get:**
- `perf stat` - CPU performance counters
- `perf record/report` - Detailed profiling with call graphs
- `valgrind cachegrind` - Cache simulation and analysis

With exact usage commands for each tool.

---

## 5. Code Optimization Help

**You ask Continue:**
> "I have a cache miss problem in my code. How can I fix it?"

**Continue uses** `search_optimization_topics` tool with `query: "cache"`

**You get:**
- Lab 1: Cache Optimization techniques
- Books: "Performance Analysis and Tuning on Modern CPUs"
- Online: "Algorithms for Modern Hardware" 
- Specific topics: cache-oblivious algorithms, memory access patterns

Then Continue can help you apply these concepts to your specific code!

---

## 6. Finding External Resources

**You ask Continue:**
> "Show me all available learning resources"

**Continue uses** `get_all_resources` tool

**You get:** Complete catalog including:
- 3 recommended books
- 4 online resources with URLs
- 3 open-source projects
- 8 lab exercises
- Platform-specific profiling tools

---

## 7. Progressive Learning

**You ask Continue:**
> "I've completed the beginner labs. What's next?"

**Continue uses** `get_learning_path` tool with `level: "intermediate"`

**You get:**
- Lab 4: Memory Bound Optimizations
- Lab 5: Data Structures for Performance
- Lab 6: Highway SIMD Library

---

## 8. Combined Queries

**You ask Continue:**
> "I want to learn about branch prediction. Show me resources and tell me which lab covers it."

**Continue uses:**
1. `search_optimization_topics` with `query: "branch prediction"`
2. Results include Lab 2 info automatically

**You get:**
- Lab 2: Branch Prediction (beginner, 1-2 hours)
- Topics: branchless programming, cmov, lookup tables
- Speedup targets and detailed description

---

## 9. Tool Selection Guidance

**You ask Continue:**
> "I'm on macOS. How do I profile my code?"

**Continue uses** `get_profiling_tools` tool with `platform: "macos"`

**You get:**
- Instruments (Xcode profiling tools)

---

## 10. Research and Implementation

**You ask Continue:**
> "Help me optimize this loop using SIMD. First show me what resources are available."

**Continue workflow:**
1. Uses `search_optimization_topics` with `query: "SIMD"`
2. Shows you relevant labs and resources
3. Then helps you write actual SIMD code based on the knowledge base

This combines the MCP server's knowledge with Continue's code generation capabilities!

---

## Pro Tips

- **Be specific**: "SIMD" works better than "make code faster"
- **Ask follow-ups**: After getting resources, ask Continue to explain concepts
- **Combine with code**: Ask Continue to apply techniques to your actual code
- **Platform-aware**: Mention your OS when asking about tooling
- **Progressive learning**: Ask for beginner → intermediate → advanced paths
