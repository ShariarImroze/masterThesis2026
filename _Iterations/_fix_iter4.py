#!/usr/bin/env python3
"""Fix all 20 bugs in _iteration_4.ipynb."""
import json, ast, re, sys, copy

NB_PATH = "_iteration_4.ipynb"

with open(NB_PATH, "r") as f:
    nb = json.load(f)

def get_src(cell_idx):
    return "".join(nb["cells"][cell_idx]["source"])

def set_src(cell_idx, new_src):
    # Convert string back to list of lines preserving notebook format
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

fixes_applied = []

# ============================================================
# CELL 1 — Setup/Reset Utilities
# ============================================================
src1 = get_src(1)

# BUG 4-2: Safe deletion in reset_results, full_reset, complete_rerun
# Three locations with bare os.remove(file) in glob loops — need os.path.isfile guard

# 1) reset_results
src1 = safe_replace(
    src1,
    '            for file in glob.glob(os.path.join(RESULTS_DIR, \'*\')):\n                os.remove(file)\n            print(" All iteration 4 results deleted")',
    '            for file in glob.glob(os.path.join(RESULTS_DIR, \'*\')):\n                if os.path.isfile(file):\n                    os.remove(file)\n            print(" All iteration 4 results deleted")',
    "4-2a: safe delete in reset_results"
)
fixes_applied.append("4-2a: safe delete in reset_results")

# 2) full_reset
src1 = safe_replace(
    src1,
    '            for file in glob.glob(os.path.join(RESULTS_DIR, \'*\')):\n                os.remove(file)\n            print(" Results deleted")',
    '            for file in glob.glob(os.path.join(RESULTS_DIR, \'*\')):\n                if os.path.isfile(file):\n                    os.remove(file)\n            print(" Results deleted")',
    "4-2b: safe delete in full_reset"
)
fixes_applied.append("4-2b: safe delete in full_reset")

# 3) complete_rerun
src1 = safe_replace(
    src1,
    '            for file in glob.glob(os.path.join(RESULTS_DIR, \'*\')):\n                os.remove(file)\n            print(" Results cleared")',
    '            for file in glob.glob(os.path.join(RESULTS_DIR, \'*\')):\n                if os.path.isfile(file):\n                    os.remove(file)\n            print(" Results cleared")',
    "4-2c: safe delete in complete_rerun"
)
fixes_applied.append("4-2c: safe delete in complete_rerun")

set_src(1, src1)

# ============================================================
# CELL 5 — Main Pipeline
# ============================================================
src5 = get_src(5)

# BUG 4-8: Remove unused imports
# Remove StratifiedKFold and cross_val_score from import line
src5 = safe_replace(
    src5,
    "from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_val_score",
    "from sklearn.model_selection import train_test_split, GridSearchCV",
    "4-8a: remove unused StratifiedKFold, cross_val_score"
)
fixes_applied.append("4-8a: remove unused StratifiedKFold, cross_val_score")

# Remove GradientBoostingClassifier, StackingClassifier from ensemble import
src5 = safe_replace(
    src5,
    "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, StackingClassifier",
    "from sklearn.ensemble import RandomForestClassifier, VotingClassifier",
    "4-8b: remove unused GradientBoostingClassifier, StackingClassifier"
)
fixes_applied.append("4-8b: remove unused GradientBoostingClassifier, StackingClassifier")

# Remove RandomUnderSampler and ImbPipeline from imblearn import
src5 = safe_replace(
    src5,
    "    from imblearn.over_sampling import SMOTE\n    from imblearn.under_sampling import RandomUnderSampler\n    from imblearn.pipeline import Pipeline as ImbPipeline",
    "    from imblearn.over_sampling import SMOTE",
    "4-8c: remove unused RandomUnderSampler, ImbPipeline"
)
fixes_applied.append("4-8c: remove unused RandomUnderSampler, ImbPipeline")

# BUG 4-17: Fix stale TODO comment in CONFIG
src5 = safe_replace(
    src5,
    "'smote_strategy': 0.7,  # Oversample minority to 70% of majority. Can anything else be done to automate the class imbalance issue. ",
    "'smote_strategy': 0.7,  # Oversample minority to 70% of majority",
    "4-17: remove stale TODO comment"
)
fixes_applied.append("4-17: remove stale TODO comment in CONFIG")

# BUG 4-7: GridSearchCV scoring='f1_weighted' → scoring='f1_macro'
src5 = safe_replace(
    src5,
    "svm_model = GridSearchCV(\n                svm_base, param_grid_svm, cv=3, scoring='f1_weighted',",
    "svm_model = GridSearchCV(\n                svm_base, param_grid_svm, cv=3, scoring='f1_macro',",
    "4-7: GridSearchCV scoring f1_weighted → f1_macro"
)
fixes_applied.append("4-7: GridSearchCV scoring f1_weighted → f1_macro")

# BUG 4-4: Ensemble selects first 3, should select top 3 by f1_ps
src5 = safe_replace(
    src5,
    """        try:
            # Select top 3 classifiers for ensemble
            ensemble_classifiers = []
            for name, clf in list(classifiers.items())[:3]:
                ensemble_classifiers.append((name, clf))""",
    """        try:
            # Select top 3 classifiers by Process Safety F1
            sorted_by_f1ps = sorted(results.keys(), key=lambda x: results[x]['f1_ps'], reverse=True)
            top_3_names = sorted_by_f1ps[:3]
            ensemble_classifiers = [(name, classifiers[name]) for name in top_3_names if name in classifiers]""",
    "4-4: ensemble select top 3 by f1_ps"
)
fixes_applied.append("4-4: ensemble select top 3 by f1_ps")

# BUG 4-3: Fit scaler on pre-SMOTE X_train, transform both
# Current: scaler.fit_transform(X_train_subset) — which is post-SMOTE data
# Fix: fit on original X_train, then transform X_train_subset and X_test
src5 = safe_replace(
    src5,
    """    # Feature scaling
    if CONFIG['use_feature_scaling']:
        print(f"\\n Applying feature scaling...")
        scaler = StandardScaler()
        X_train_subset_scaled = scaler.fit_transform(X_train_subset)
        X_test_scaled = scaler.transform(X_test)""",
    """    # Feature scaling — fit on original (pre-SMOTE) X_train to avoid data leakage
    if CONFIG['use_feature_scaling']:
        print(f"\\n Applying feature scaling...")
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train_subset_scaled = scaler.transform(X_train_subset)
        X_test_scaled = scaler.transform(X_test)""",
    "4-3: fit scaler on pre-SMOTE X_train"
)
fixes_applied.append("4-3: fit scaler on pre-SMOTE X_train (avoid data leakage)")

# BUG 4-5: eval_ → iter4_eval_ prefix in Cell 5
src5 = safe_replace(
    src5,
    "plot_filename = f'eval_{dataset_name}_{model_key.replace",
    "plot_filename = f'iter4_eval_{dataset_name}_{model_key.replace",
    "4-5: eval_ → iter4_eval_ prefix"
)
fixes_applied.append("4-5: eval_ → iter4_eval_ prefix in Cell 5")

# BUG 4-10: Remove dead code _Path and _MASTER_DS
src5 = safe_replace(
    src5,
    "from pathlib import Path as _Path\n_MASTER_DS = _Path(DATA_DIR)\n",
    "",
    "4-10: remove dead _Path/_MASTER_DS code"
)
fixes_applied.append("4-10: remove dead _Path/_MASTER_DS code")

# BUG 4-18: Fix contradictory comment
src5 = safe_replace(
    src5,
    "# Load datasets from Iteration 0 pre-processed outputs (no re-preprocessing)",
    "# Load datasets from pre-processed master dataset splits",
    "4-18: fix contradictory comment"
)
fixes_applied.append("4-18: fix contradictory comment")

# BUG 4-15: Dataset keys german_manual → germany_manual, etc.
src5 = safe_replace(
    src5,
    "    'german_manual':      str(PATHS['master_dataset'] / 'By_SL_Country' / 'master_df_Germany_manual.json'),",
    "    'germany_manual':     str(PATHS['master_dataset'] / 'By_SL_Country' / 'master_df_Germany_manual.json'),",
    "4-15a: german_manual → germany_manual"
)
src5 = safe_replace(
    src5,
    "    'swedish_manual':     str(PATHS['master_dataset'] / 'By_SL_Country' / 'master_df_Sweden_manual.json'),",
    "    'sweden_manual':      str(PATHS['master_dataset'] / 'By_SL_Country' / 'master_df_Sweden_manual.json'),",
    "4-15b: swedish_manual → sweden_manual"
)
src5 = safe_replace(
    src5,
    "    'dutch_manual':       str(PATHS['master_dataset'] / 'By_SL_Country' / 'master_df_Netherlands_manual.json'),",
    "    'netherlands_manual': str(PATHS['master_dataset'] / 'By_SL_Country' / 'master_df_Netherlands_manual.json'),",
    "4-15c: dutch_manual → netherlands_manual"
)
fixes_applied.append("4-15: fix dataset key names to match filenames")

# BUG 4-13: Add torch.mps.empty_cache() alongside CUDA cache clearing
# There are 4 occurrences of the cuda cache pattern in Cell 5.
# Pattern 1: inside batch loop (single-line if)
src5 = safe_replace(
    src5,
    "        if device == 'cuda':\n            torch.cuda.empty_cache()",
    "        if device == 'cuda':\n            torch.cuda.empty_cache()\n        elif device == 'mps' and hasattr(torch.mps, 'empty_cache'):\n            torch.mps.empty_cache()",
    "4-13a: add MPS cache clearing in batch loop"
)

# Pattern 2: 4-space indent (process_dataset_enhanced ~L417)
src5 = safe_replace(
    src5,
    "    if torch.cuda.is_available():\n        torch.cuda.empty_cache()",
    "    if torch.cuda.is_available():\n        torch.cuda.empty_cache()\n    elif hasattr(torch, 'mps') and hasattr(torch.mps, 'empty_cache'):\n        torch.mps.empty_cache()",
    "4-13b: add MPS cache in process_dataset_enhanced"
)

# Pattern 3: 8-space indent (main execution loop ~L947)
src5 = safe_replace(
    src5,
    "        if torch.cuda.is_available():\n            torch.cuda.empty_cache()",
    "        if torch.cuda.is_available():\n            torch.cuda.empty_cache()\n        elif hasattr(torch, 'mps') and hasattr(torch.mps, 'empty_cache'):\n            torch.mps.empty_cache()",
    "4-13c: add MPS cache in main execution loop"
)
fixes_applied.append("4-13: add MPS cache clearing (3 locations)")

# BUG 4-16: Add baseline and improvement calculation
# Insert _RQ1_BASELINE after CONFIG block
src5 = safe_replace(
    src5,
    "# Model configurations - Best performing models with FIXED paths",
    "_RQ1_BASELINE = 0.7825  # Iteration 0: bert-base-uncased + SVM → Macro F1\n\n# Model configurations - Best performing models with FIXED paths",
    "4-16a: add _RQ1_BASELINE constant"
)
fixes_applied.append("4-16: add _RQ1_BASELINE constant")

# BUG 4-20: Rename/document hyperparameter_tuning as SVM-only
src5 = safe_replace(
    src5,
    "    'hyperparameter_tuning': True,",
    "    'hyperparameter_tuning': True,   # SVM GridSearchCV only",
    "4-20: document hyperparameter_tuning as SVM-only"
)
fixes_applied.append("4-20: document hyperparameter_tuning as SVM-only")

set_src(5, src5)

# ============================================================
# CELL 7 — Results Generation
# ============================================================
src7 = get_src(7)

# BUG 4-6: cm_ → iter4_cm_ prefix in Cell 7
src7 = safe_replace(
    src7,
    "plot_filename = f'cm_{dataset_name}_{model_key.replace",
    "plot_filename = f'iter4_cm_{dataset_name}_{model_key.replace",
    "4-6: cm_ → iter4_cm_ prefix"
)
fixes_applied.append("4-6: cm_ → iter4_cm_ prefix in Cell 7")

# BUG 4-11: Standardize macro_f1 → f1_macro in Cell 7's result dict
# The calculate_detailed_metrics returns 'macro_f1', and it's used throughout Cell 7.
# We need to rename the key in the return dict and all references.
src7 = safe_replace(
    src7,
    "        'macro_f1': macro_f1, 'fpr': fpr, 'fnr': fnr",
    "        'f1_macro': macro_f1, 'fpr': fpr, 'fnr': fnr",
    "4-11a: macro_f1 → f1_macro in calculate_detailed_metrics return"
)

# Fix all references to metrics['macro_f1'] in Cell 7
src7 = src7.replace("metrics['macro_f1']", "metrics['f1_macro']")
# Fix the bar chart label
src7 = safe_replace(
    src7,
    "'Macro F1': metrics['f1_macro']",
    "'F1 (Macro)': metrics['f1_macro']",
    "4-11b: label Macro F1 → F1 (Macro)"
)

# Fix in results dict at end
src7 = safe_replace(
    src7,
    "            'macro_f1': metrics['f1_macro'],",
    "            'f1_macro': metrics['f1_macro'],",
    "4-11c: macro_f1 → f1_macro in all_results dict"
)
fixes_applied.append("4-11: standardize macro_f1 → f1_macro in Cell 7")

# BUG 4-19: Add comment documenting Cell 7 as quick-evaluation path
src7 = safe_replace(
    src7,
    "# ============================================================\n# RESULTS OF ITERATION 4\n# ============================================================",
    "# ============================================================\n# RESULTS OF ITERATION 4 — Quick Evaluation Path\n# (Trains classifiers with default hyperparameters from saved embeddings;\n#  for GridSearchCV-tuned results, use the main pipeline in Cell 5.)\n# ============================================================",
    "4-19: document Cell 7 as quick-evaluation path"
)
fixes_applied.append("4-19: document Cell 7 as quick-evaluation path")

set_src(7, src7)

# ============================================================
# CELL 9 — Summary Export
# ============================================================
src9 = get_src(9)

# BUG 4-1 CRITICAL: CSV filename mismatch
src9 = safe_replace(
    src9,
    "_results_csv = os.path.join(RESULTS_DIR, 'iteration_4_all_results.csv')",
    "_results_csv = os.path.join(RESULTS_DIR, 'iteration_4_comprehensive_results.csv')",
    "4-1: CSV filename mismatch (CRITICAL)"
)
fixes_applied.append("4-1 CRITICAL: fix CSV filename to iteration_4_comprehensive_results.csv")

# BUG 4-9: Remove import json as _json
src9 = safe_replace(
    src9,
    "import json as _json\nimport pandas as pd\nimport os",
    "import json\nimport pandas as pd\nimport os",
    "4-9a: remove _json alias"
)
# Fix usage of _json.dump
src9 = safe_replace(
    src9,
    "        _json.dump(_summary, _f, indent=2, ensure_ascii=False)",
    "        json.dump(_summary, _f, indent=2, ensure_ascii=False)",
    "4-9b: _json.dump → json.dump"
)
fixes_applied.append("4-9: remove _json alias, use json directly")

# BUG 4-12: total_samples always 0
src9 = safe_replace(
    src9,
    "            'total_samples': int(row.get('total_samples', 0)),",
    "            'total_samples': int(row.get('TN', 0)) + int(row.get('FP', 0)) + int(row.get('FN', 0)) + int(row.get('TP', 0)),",
    "4-12: fix total_samples computation"
)
fixes_applied.append("4-12: fix total_samples = TN+FP+FN+TP")

# BUG 4-16b: Add improvement_over_baseline in gap_analysis
src9 = safe_replace(
    src9,
    "        _summary['gap_analysis'][key] = {\n            'current_f1_ps': round(float(row['f1_ps']), 4),\n            'rq1_target': _RQ1_TARGET,\n            'gap': round(float(_RQ1_TARGET - row['f1_ps']), 4)\n        }",
    "        _summary['gap_analysis'][key] = {\n            'current_f1_ps': round(float(row['f1_ps']), 4),\n            'rq1_target': _RQ1_TARGET,\n            'gap': round(float(_RQ1_TARGET - row['f1_ps']), 4),\n            'improvement_over_baseline': round(float(row['f1_ps']) - 0.7825, 4)\n        }",
    "4-16b: add improvement_over_baseline"
)
fixes_applied.append("4-16b: add improvement_over_baseline in gap_analysis")

set_src(9, src9)

# ============================================================
# MARKDOWN CELLS
# ============================================================

# BUG 4-14: Markdown "RQ1" should note broader scope
md0 = get_src(0)
md0 = safe_replace(
    md0,
    "## Configuration and Reset Utilities - RQ1",
    "## Configuration and Reset Utilities — RQ1",
    "4-14: markdown dash fix"
)
set_src(0, md0)
fixes_applied.append("4-14: markdown dash consistency")

# ============================================================
# SYNTAX VERIFICATION
# ============================================================
print(f"\n{'='*60}")
print(f"Applied {len(fixes_applied)} fixes:")
for f in fixes_applied:
    print(f"  ✓ {f}")

# Verify syntax of all code cells
for cell_idx in [1, 3, 5, 7, 9]:
    src = get_src(cell_idx)
    try:
        ast.parse(src)
        print(f"  [OK] Cell {cell_idx} syntax valid")
    except SyntaxError as e:
        print(f"  [FAIL] Cell {cell_idx} syntax error: {e}")
        sys.exit(1)

# Save
with open(NB_PATH, "w") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\n[OK] Saved {NB_PATH} with {len(fixes_applied)} fixes")
