#!/usr/bin/env python3
"""Fix all bugs in _iteration_5.ipynb."""
import json, ast, sys

NB_PATH = "_iteration_5.ipynb"

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
# CELL 2 — Setup/Reset Utilities
# ============================================================
src2 = get_src(2)

# BUG 5-M1: Safe deletion (3 locations)
src2 = safe_replace(src2,
    "            for file in glob.glob(os.path.join(RESULTS_DIR, '*')):\n                os.remove(file)\n            print(\"All iteration 5 results deleted\")",
    "            for file in glob.glob(os.path.join(RESULTS_DIR, '*')):\n                if os.path.isfile(file):\n                    os.remove(file)\n            print(\"All iteration 5 results deleted\")",
    "5-M1a: safe delete in reset_results")
fixes.append("5-M1a: safe delete in reset_results")

src2 = safe_replace(src2,
    "            for file in glob.glob(os.path.join(RESULTS_DIR, '*')):\n                os.remove(file)\n            print(\"Results deleted\")",
    "            for file in glob.glob(os.path.join(RESULTS_DIR, '*')):\n                if os.path.isfile(file):\n                    os.remove(file)\n            print(\"Results deleted\")",
    "5-M1b: safe delete in full_reset")
fixes.append("5-M1b: safe delete in full_reset")

src2 = safe_replace(src2,
    "            for file in glob.glob(os.path.join(RESULTS_DIR, '*')):\n                os.remove(file)\n            print(\"Results cleared\")",
    "            for file in glob.glob(os.path.join(RESULTS_DIR, '*')):\n                if os.path.isfile(file):\n                    os.remove(file)\n            print(\"Results cleared\")",
    "5-M1c: safe delete in complete_rerun")
fixes.append("5-M1c: safe delete in complete_rerun")

set_src(2, src2)

# ============================================================
# CELL 8 — Main Pipeline
# ============================================================
src8 = get_src(8)

# BUG 5-M5: Remove unused imports from sklearn
src8 = safe_replace(src8,
    "from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_val_score",
    "from sklearn.model_selection import train_test_split, GridSearchCV",
    "5-M5a: remove unused StratifiedKFold, cross_val_score")
fixes.append("5-M5a: remove unused StratifiedKFold, cross_val_score")

src8 = safe_replace(src8,
    "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier, StackingClassifier",
    "from sklearn.ensemble import RandomForestClassifier, VotingClassifier",
    "5-M5b: remove unused GradientBoostingClassifier, StackingClassifier")
fixes.append("5-M5b: remove unused GradientBoostingClassifier, StackingClassifier")

# Remove unused imblearn imports (keep SMOTE, RandomUnderSampler, TomekLinks)
src8 = safe_replace(src8,
    "    from imblearn.over_sampling import SMOTE, ADASYN\n    from imblearn.under_sampling import RandomUnderSampler, TomekLinks, EditedNearestNeighbours\n    from imblearn.combine import SMOTETomek, SMOTEENN\n    from imblearn.pipeline import Pipeline as ImbPipeline",
    "    from imblearn.over_sampling import SMOTE\n    from imblearn.under_sampling import RandomUnderSampler, TomekLinks",
    "5-M5c: remove unused imblearn imports")
fixes.append("5-M5c: remove unused ADASYN, EditedNearestNeighbours, SMOTETomek, SMOTEENN, ImbPipeline")

# BUG 5-M2: Add MPS cache clearing (2 locations)
# Location 1: in batch loop (device == 'cuda' check)
src8 = safe_replace(src8,
    "        if device == 'cuda':\n            torch.cuda.empty_cache()\n        if i % 50 == 0 and i > 0:\n            gc.collect()",
    "        if device == 'cuda':\n            torch.cuda.empty_cache()\n        elif device == 'mps' and hasattr(torch.mps, 'empty_cache'):\n            torch.mps.empty_cache()\n        if i % 50 == 0 and i > 0:\n            gc.collect()",
    "5-M2a: add MPS cache clearing in batch loop")
fixes.append("5-M2a: add MPS cache clearing in batch loop")

# Location 2: after model processing
src8 = safe_replace(src8,
    "                if torch.cuda.is_available():\n                    torch.cuda.empty_cache()",
    "                if torch.cuda.is_available():\n                    torch.cuda.empty_cache()\n                elif hasattr(torch, 'mps') and hasattr(torch.mps, 'empty_cache'):\n                    torch.mps.empty_cache()",
    "5-M2b: add MPS cache clearing after model")
fixes.append("5-M2b: add MPS cache clearing after model processing")

# BUG 5-M4: eval_ → iter5_eval_ prefix
src8 = safe_replace(src8,
    'fig_path = os.path.join(RESULTS_DIR, f"eval_{dataset_name}_{model_name.replace',
    'fig_path = os.path.join(RESULTS_DIR, f"iter5_eval_{dataset_name}_{model_name.replace',
    "5-M4: eval_ → iter5_eval_ prefix")
fixes.append("5-M4: eval_ → iter5_eval_ prefix on plot files")

# BUG 5-M3 + 5-C1: Fix summary section — remove aliases, fix JSON-exists bug
src8 = safe_replace(src8,
    """import json as _json5, pandas as _pd5

_results_json5 = os.path.join(RESULTS_DIR, 'iteration_5_comprehensive_results.json')
_results_csv5 = os.path.join(RESULTS_DIR, 'iteration_5_comprehensive_results.csv')
if os.path.exists(_results_json5):
    _df5 = _pd5.read_json(_results_json5)
elif os.path.exists(_results_csv5):
    _df5 = _pd5.read_csv(_results_csv5)
    _best5 = _df5.loc[_df5['macro_f1'].idxmax()] if 'macro_f1' in _df5.columns else _df5.iloc[0]
    _summary5 = {
        'iteration': 5,
        'model': '9 multilingual embedding models + SMOTE balancing + classical ML classifiers',
        'strategy': 'SMOTE oversampling + aggressive class weighting',
        'best_result': {
            'embedding_model': str(_best5.get('embedding_model', '')),
            'classifier': str(_best5.get('classifier', '')),
            'dataset': str(_best5.get('dataset', '')),
            'macro_f1': round(float(_best5.get('macro_f1', 0)), 4),
            'recall_ps': round(float(_best5.get('recall_ps', 0)), 4),
        },
        'gap_analysis': {
            'current_macro_f1': round(float(_best5.get('macro_f1', 0)), 4),
            'rq1_target': 0.8161,
            'gap': round(float(0.8161 - _best5.get('macro_f1', 0)), 4)
        }
    }
    with open(os.path.join(RESULTS_DIR, 'iteration_5_summary.json'), 'w') as _f5:
        _json5.dump(_summary5, _f5, indent=2)
    print(f"[OK] Saved: iteration_5_summary.json")
else:
    print(f"[INFO] Results CSV not found yet. Run pipeline first.")""",
    """_RQ1_BASELINE = 0.7825  # Iteration 0: bert-base-uncased + SVM

_results_json5 = os.path.join(RESULTS_DIR, 'iteration_5_comprehensive_results.json')
_results_csv5 = os.path.join(RESULTS_DIR, 'iteration_5_comprehensive_results.csv')
_df5 = None
if os.path.exists(_results_json5):
    _df5 = pd.read_json(_results_json5)
elif os.path.exists(_results_csv5):
    _df5 = pd.read_csv(_results_csv5)

if _df5 is not None:
    _best5 = _df5.loc[_df5['macro_f1'].idxmax()] if 'macro_f1' in _df5.columns else _df5.iloc[0]
    _summary5 = {
        'iteration': 5,
        'model': '9 multilingual embedding models + SMOTE balancing + classical ML classifiers',
        'strategy': 'SMOTE oversampling + aggressive class weighting',
        'best_result': {
            'embedding_model': str(_best5.get('embedding_model', '')),
            'classifier': str(_best5.get('classifier', '')),
            'dataset': str(_best5.get('dataset', '')),
            'macro_f1': round(float(_best5.get('macro_f1', 0)), 4),
            'recall_ps': round(float(_best5.get('recall_ps', 0)), 4),
        },
        'gap_analysis': {
            'current_macro_f1': round(float(_best5.get('macro_f1', 0)), 4),
            'rq1_target': 0.85,
            'baseline': _RQ1_BASELINE,
            'gap': round(float(0.85 - _best5.get('macro_f1', 0)), 4),
            'improvement_over_baseline': round(float(_best5.get('macro_f1', 0)) - _RQ1_BASELINE, 4)
        }
    }
    with open(os.path.join(RESULTS_DIR, 'iteration_5_summary.json'), 'w') as _f5:
        json.dump(_summary5, _f5, indent=2)
    print(f"[OK] Saved: iteration_5_summary.json")
else:
    print(f"[INFO] Results not found yet. Run pipeline first.")""",
    "5-C1+M3+L2: fix summary section")
fixes.append("5-C1 CRITICAL: fix summary creation when JSON exists")
fixes.append("5-M3: remove _json5/_pd5 aliases, use json/pd")
fixes.append("5-L2: add _RQ1_BASELINE + improvement_over_baseline, fix target to 0.85")

set_src(8, src8)

# ============================================================
# SYNTAX VERIFICATION
# ============================================================
print(f"\n{'='*60}")
print(f"Applied {len(fixes)} fixes:")
for f in fixes:
    print(f"  ✓ {f}")

for cell_idx in [2, 5, 8, 9, 10]:
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
