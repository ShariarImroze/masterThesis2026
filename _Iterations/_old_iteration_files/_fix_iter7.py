#!/usr/bin/env python3
"""Fix all bugs in _iteration_7.ipynb — primarily 6a→7 renaming."""
import json, ast, sys, re

NB_PATH = "_iteration_7.ipynb"

with open(NB_PATH, "r") as f:
    nb = json.load(f)

def get_src(cell_idx):
    return "".join(nb["cells"][cell_idx]["source"])

def set_src(cell_idx, new_src):
    lines = new_src.split("\n")
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + "\n")
        else:
            result.append(line)
    nb["cells"][cell_idx]["source"] = result

def safe_replace(src, old, new, label, count=1):
    n = src.count(old)
    assert n == count, f"[FAIL] {label}: expected {count} occurrence(s), found {n}"
    return src.replace(old, new, count)

fixes = []

# ============================================================
# CELL 1 — Results path
# ============================================================
src1 = get_src(1)
src1 = safe_replace(src1,
    "'results':        BASE_DIR / 'Results' / '_iteration_6a',",
    "'results':        BASE_DIR / 'Results' / '_iteration_7',",
    "7-1: results path _iteration_6a → _iteration_7")
fixes.append("7-1 CRITICAL: results path _iteration_6a → _iteration_7")
set_src(1, src1)

# ============================================================
# CELL 2 — Variable name master_df_6a → master_df_7
# ============================================================
src2 = get_src(2)
src2 = src2.replace("master_df_6a", "master_df_7")
assert "master_df_6a" not in src2
fixes.append("7-2 CRITICAL: master_df_6a → master_df_7 (4 occurrences)")
set_src(2, src2)

# ============================================================
# CELL 4 — Checkpoint filename
# ============================================================
src4 = get_src(4)
src4 = safe_replace(src4,
    "checkpoint_file = os.path.join(RESULTS_DIR, f'checkpoint_6a_{language.lower()}.json')",
    "checkpoint_file = os.path.join(RESULTS_DIR, f'checkpoint_7_{language.lower()}.json')",
    "7-3: checkpoint_6a_ → checkpoint_7_")
fixes.append("7-3 CRITICAL: checkpoint filename 6a → 7")
set_src(4, src4)

# ============================================================
# CELL 8 — Print labels
# ============================================================
src8 = get_src(8)
src8 = src8.replace("Iteration 6a", "Iteration 7")
assert "6a" not in src8
fixes.append("7-4: Iteration 6a → Iteration 7 in print statements (Cell 8)")
set_src(8, src8)

# ============================================================
# CELL 9 — Confusion matrix title and filename
# ============================================================
src9 = get_src(9)
src9 = safe_replace(src9,
    "'Iteration 6a — XLM-RoBERTa XNLI Zero-Shot Classification\\n'",
    "'Iteration 7 — XLM-RoBERTa XNLI Zero-Shot Classification\\n'",
    "7-5a: CM title 6a → 7")
src9 = safe_replace(src9,
    "cm_path = os.path.join(RESULTS_DIR, 'confusion_matrix_6a.png')",
    "cm_path = os.path.join(RESULTS_DIR, 'iter7_confusion_matrix.png')",
    "7-5b: CM filename 6a → iter7_")
fixes.append("7-5 CRITICAL: confusion matrix title and filename 6a → 7")
set_src(9, src9)

# ============================================================
# CELL 11 — Summary export
# ============================================================
src11 = get_src(11)
src11 = safe_replace(src11,
    "# SAVE ITERATION 6a SUMMARY (consistent with Iteration 0 format)",
    "# SAVE ITERATION 7 SUMMARY (consistent with Iteration 0 format)",
    "7-6a: comment 6a → 7")
src11 = safe_replace(src11,
    "'iteration': '6a',",
    "'iteration': 7,",
    "7-6b: iteration value 6a → 7")
src11 = safe_replace(src11,
    "out_path = os.path.join(RESULTS_DIR, 'iteration_6a_summary.json')",
    "out_path = os.path.join(RESULTS_DIR, 'iteration_7_summary.json')",
    "7-6c: summary filename 6a → 7")
src11 = safe_replace(src11,
    'print("  ITERATION 6a — FINAL STATUS")',
    'print("  ITERATION 7 — FINAL STATUS")',
    "7-6d: print label 6a → 7")
fixes.append("7-6 CRITICAL: summary export all 6a → 7 references")
set_src(11, src11)

# ============================================================
# SYNTAX VERIFICATION
# ============================================================
print(f"\n{'='*60}")
print(f"Applied {len(fixes)} fixes:")
for f in fixes:
    print(f"  ✓ {f}")

for ci in range(1, 12):
    if nb['cells'][ci]['cell_type'] != 'code':
        continue
    src = get_src(ci)
    try:
        ast.parse(src)
        print(f"  [OK] Cell {ci} syntax valid")
    except SyntaxError as e:
        print(f"  [FAIL] Cell {ci} syntax error: {e}")
        sys.exit(1)

# Verify no remaining 6a references in code cells
for ci in range(1, 12):
    if nb['cells'][ci]['cell_type'] != 'code':
        continue
    src = get_src(ci)
    if '6a' in src:
        print(f"  [WARN] Cell {ci} still contains '6a' reference")

with open(NB_PATH, "w") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\n[OK] Saved {NB_PATH} with {len(fixes)} fixes")
