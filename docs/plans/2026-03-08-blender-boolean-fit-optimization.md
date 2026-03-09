# Blender Boolean Fit Optimization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a Blender Python routine that rotates cutter object `B` (all 3 axes), finds the minimal uniform scale for target object `A` that still contains `B`, and applies boolean difference with the best rotation maximizing remaining volume.

**Architecture:** Implement a new optimization module in `scripts/python/src` with pure helper functions for search (unit-testable without Blender) and Blender-specific geometry operations for containment/volume. Use grid search over Euler angles and per-rotation binary search for minimal feasible uniform scale. Reuse existing boolean-difference functionality for final application.

**Tech Stack:** Python, Blender `bpy`/`bmesh`/`mathutils`, pytest (for pure helper functions)

---

### Task 1: Add test coverage for search helpers

**Files:**
- Create: `scripts/python/tests/test_optimize_boolean_fit.py`

**Step 1: Write failing tests**
- Add tests for angle-grid generation and binary-search helper behavior.

**Step 2: Run tests to verify failure**
- Run: `cd scripts/python && .venv/bin/python -m pytest tests/test_optimize_boolean_fit.py -q`
- Expected: FAIL due to missing module/functions.

**Step 3: Implement minimal helper code to pass tests**
- Add helper functions in new module:
  - `_generate_euler_grid(step_degrees)`
  - `_binary_search_min_feasible(low, high, predicate, iterations)`

**Step 4: Run tests to verify pass**
- Run same pytest command.
- Expected: PASS.

### Task 2: Implement Blender optimization routine

**Files:**
- Create: `scripts/python/src/optimize_boolean_fit.py`
- Modify: `scripts/python/src/add_boolean_difference.py` (only if import/reuse adjustment needed)

**Step 1: Add Blender geometry utilities**
- Implement temporary duplication, mesh volume computation, and point-inside checks.

**Step 2: Implement optimization loop**
- For each sampled cutter rotation: binary-search minimal feasible target uniform scale.
- Compute resulting remaining volume after temporary boolean difference.
- Track best rotation/scale by max remaining volume.

**Step 3: Implement final application**
- Apply best rotation to real `B`, best uniform scale multiplier to real `A`, and apply boolean difference.

**Step 4: Add clear return payload**
- Return best rotation, scale multiplier, and resulting remaining volume.

### Task 3: Verify end-to-end quality

**Files:**
- Modify: `scripts/python/src/optimize_boolean_fit.py` (if fixes required)

**Step 1: Run tests**
- Run: `cd scripts/python && .venv/bin/python -m pytest -q`

**Step 2: Run syntax validation**
- Run: `cd scripts/python && .venv/bin/python -m py_compile src/*.py`

**Step 3: Review diff for scope**
- Ensure only planned files changed in worktree.
