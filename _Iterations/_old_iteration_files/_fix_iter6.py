#!/usr/bin/env python3
"""Fix all bugs in _iteration_6.ipynb."""
import json, ast, sys

NB_PATH = "_iteration_6.ipynb"

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
# CELL 3 — Imports, Data Loading
# ============================================================
src3 = get_src(3)

# BUG 6-1: Remove unused import pickle
src3 = safe_replace(src3,
    "import pickle\n",
    "",
    "6-1: remove unused pickle import")
fixes.append("6-1: remove unused pickle import")

# BUG 6-3: Fix device selection to support MPS
src3 = safe_replace(src3,
    "DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'\nprint(f'Using device: {DEVICE}')",
    "if torch.backends.mps.is_available() and torch.backends.mps.is_built():\n    DEVICE = 'mps'\nelif torch.cuda.is_available():\n    DEVICE = 'cuda'\nelse:\n    DEVICE = 'cpu'\nprint(f'Using device: {DEVICE}')",
    "6-3: add MPS device support")
fixes.append("6-3: add MPS device support for Apple Silicon")

# Add MPS cache clearing alongside CUDA
src3 = safe_replace(src3,
    "        if torch.cuda.is_available():\n            torch.cuda.empty_cache()",
    "        if torch.cuda.is_available():\n            torch.cuda.empty_cache()\n        elif DEVICE == 'mps' and hasattr(torch.mps, 'empty_cache'):\n            torch.mps.empty_cache()",
    "6-3b: add MPS cache clearing")
fixes.append("6-3b: add MPS cache clearing")

set_src(3, src3)

# ============================================================
# CELL 5 — Scaler data leakage
# ============================================================
src5 = get_src(5)

# BUG 6-2: Fit scaler on original X_train, not undersampled X_train_bal
src5 = safe_replace(src5,
    "    X_train_bal, y_train_bal, balanced_df = make_balanced_train_split(\n        X_train, y_train, idx_train, df, ratio=CONFIG['undersample_strategy']\n    )\n\n    scaler = StandardScaler()\n    X_train_scaled = scaler.fit_transform(X_train_bal)\n    X_test_scaled = scaler.transform(X_test)",
    "    # Fit scaler on original (pre-undersampling) X_train to avoid data leakage\n    scaler = StandardScaler()\n    scaler.fit(X_train)\n    X_test_scaled = scaler.transform(X_test)\n\n    X_train_bal, y_train_bal, balanced_df = make_balanced_train_split(\n        X_train, y_train, idx_train, df, ratio=CONFIG['undersample_strategy']\n    )\n    X_train_scaled = scaler.transform(X_train_bal)",
    "6-2: fix scaler data leakage")
fixes.append("6-2: fit scaler on pre-undersampling X_train (avoid data leakage)")

set_src(5, src5)

# ============================================================
# CELL 8 — Summary export
# ============================================================
src8 = get_src(8)

# BUG 6-4: Add _RQ1_BASELINE and improvement tracking
src8 = safe_replace(src8,
    """        'gap_analysis': {
            'current_macro_f1': round(float(best['macro_f1']), 4),
            'rq1_target': CONFIG['target_macro_f1'],
            'gap': round(float(CONFIG['target_macro_f1'] - best['macro_f1']), 4),
        }""",
    """        'gap_analysis': {
            'current_macro_f1': round(float(best['macro_f1']), 4),
            'rq1_target': 0.85,
            'baseline': 0.7825,
            'gap': round(float(0.85 - best['macro_f1']), 4),
            'improvement_over_baseline': round(float(best['macro_f1'] - 0.7825), 4),
        }""",
    "6-4: add baseline + improvement tracking")
fixes.append("6-4: add baseline + improvement_over_baseline in gap_analysis")

set_src(8, src8)

# ============================================================
# SYNTAX VERIFICATION
# ============================================================
print(f"\n{'='*60}")
print(f"Applied {len(fixes)} fixes:")
for f in fixes:
    print(f"  ✓ {f}")

for cell_idx in [2, 3, 4, 5, 6, 7, 8]:
    src = get_src(cell_idx)
    try:
        ast.parse(src)
        print(f"  [OK] Cell {cell_idx} syntax valid")
    except SyntaxError as e:
        print(f"  [FAIL] Cell {cell_idx} syntax error: {e}")
        sys.exit(1)

with open(NB_PATH, "w") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\n[OK] Saved {NB_PATH} with {len(fixes)} fixes")
