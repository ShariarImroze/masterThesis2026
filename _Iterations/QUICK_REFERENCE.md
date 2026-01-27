# Professional Version - Quick Reference Guide

## Notebook Structure at a Glance

```
ITERATION 0 - PROFESSIONAL VERSION
├── Cell 1: Title & Overview (Markdown)
├── Cell 2: Master Configuration (Python)
│   └── All paths, parameters, and constants
├── Cell 3: Consolidated Imports (Python)
│   └── All required libraries organized by category
├── Cell 4: Logging Setup (Python)
│   └── Professional logging framework
│
├── SECTION 1: DATA CLEANING & PREPROCESSING
│   ├── Cell 5: Data Loading
│   ├── Cell 6: Duplicate Removal
│   ├── Cell 7: Data Type Conversion
│   ├── Cell 8: Language Character Normalization
│   ├── Cell 9: Column Harmonization
│   ├── Cell 10: Dataset Merging
│   ├── Cell 11: Initial Cleaning
│   ├── Cell 12: Field Validation
│   └── Cell 13: Save Master Dataset
│
├── SECTION 2: LANGUAGE DETECTION & FILTERING
│   ├── Cell 14: Language Detection
│   └── Cell 15: English Filtering
│
├── SECTION 3: BERT EMBEDDINGS GENERATION
│   ├── Cell 16: Load & Create Binary Labels
│   ├── Cell 17: Initialize BERT Model
│   ├── Cell 18: Generate Embeddings
│   ├── Cell 19: Train-Test Split
│   └── Cell 20: Save Embeddings & Metadata
│
├── SECTION 4: SVM TRAINING & EVALUATION
│   ├── Cell 21: Load Embeddings
│   ├── Cell 22: Train SVM Model
│   ├── Cell 23: Baseline Evaluation
│   ├── Cell 24: K-Fold Cross-Validation
│   ├── Cell 25: Classification Report
│   └── Cell 26: Save Model & Results
│
├── SECTION 5: ADVANCED VISUALIZATIONS
│   ├── Cell 27: Confusion Matrices
│   ├── Cell 28: ROC-AUC & PR Curves
│   ├── Cell 29: Performance Metrics Charts
│   └── Cell 30: Save Classification Report
│
└── SECTION 6: FINAL SUMMARY
    └── Cell 31: Comprehensive Summary Report
```

## Key Configuration Parameters

### Essential Paths

```python
BASE_DIR = Path(r"D:\Thesis\M02555")
PATHS = {
    'raw_data': BASE_DIR / "Datasets" / "RW_Datasets",
    'iteration_output': BASE_DIR / "Datasets" / "Iteration_Outputs" / "_iteration_0",
    'embeddings': BASE_DIR / "Datasets" / "Embeddings" / "_iteration_0" / "bert-base-uncased",
    'results': BASE_DIR / "Results" / "_iteration_0"
}
```

### Data Processing

```python
DATA_CONFIG = {
    'duplicate_key': 'CASENO',
    'sort_column': 'MODIFIED_DATE',
    'required_fields': ['CASENO', 'CASE_DESCRIPTION', 'TITLE'],
    'target_column': 'CASE_TYPE',
    'target_class': 'Process Safety',
}
```

### Embedding Model

```python
EMBEDDING_CONFIG = {
    'model_name': 'bert-base-uncased',
    'max_length': 512,
    'batch_size': 8,
    'embedding_dim': 768,
    'random_state': 42,
    'test_split': 0.2
}
```

### SVM Model

```python
MODEL_CONFIG = {
    'kernel': 'rbf',
    'C': 1.0,
    'gamma': 'scale',
    'probability': True,
    'random_state': 42,
    'class_weights': 'balanced'  # Handles imbalance
}
```

### Evaluation

```python
EVAL_CONFIG = {
    'cv_folds': 5,
    'class_labels': ['Non-PS', 'Process Safety'],
    'figsize': (12, 6),
    'dpi': 300
}
```

---

## Critical Improvements Over Original

| Aspect               | Original           | Professional                      |
| -------------------- | ------------------ | --------------------------------- |
| **Organization**     | Scattered imports  | Centralized configuration         |
| **Error Handling**   | Basic try-catch    | Comprehensive validation          |
| **Logging**          | Print statements   | Professional logging framework    |
| **Documentation**    | Minimal comments   | Comprehensive docstrings          |
| **Type Safety**      | No type hints      | Full type annotations             |
| **Model Evaluation** | Accuracy only      | 8+ metrics including ROC-AUC      |
| **Validation**       | Train-test only    | 5-Fold cross-validation           |
| **Visualizations**   | 3 basic charts     | 6 professional visualizations     |
| **Reproducibility**  | Inconsistent seeds | Fixed random states               |
| **Class Imbalance**  | Not addressed      | Weighted SVM & stratification     |
| **Results Export**   | Minimal            | Comprehensive JSON + TXT reports  |
| **Metadata**         | None               | Complete tracking with timestamps |

---

## Important Functions

### Data Processing

```python
load_data(file_path) → pd.DataFrame
clean_dataframe_duplicates(df, subset_col, sort_col) → pd.DataFrame
set_column_types(df) → pd.DataFrame
replace_language_specific_chars(df) → pd.DataFrame
validate_required_fields(df, required_fields) → pd.DataFrame
compare_columns(*dfs) → List[str]
```

### Language & Embeddings

```python
detect_language(text) → Optional[str]
get_bert_embeddings(texts) → np.ndarray
```

### Logging

```python
setup_logging(log_file=None) → logging.Logger
```

---

## Running the Pipeline

### Step 1: Execute Setup

- Run Configuration Cell
- Run Imports Cell
- Run Logging Setup Cell

### Step 2: Data Preparation

- Execute Section 1 cells sequentially
- Check logs for issues
- Verify master dataset creation

### Step 3: Language Filtering

- Execute Section 2 cells
- Review English dataset statistics

### Step 4: Embeddings

- Execute Section 3 cells
- Monitor GPU/CPU memory usage
- Verify embedding dimensions

### Step 5: Model Training

- Execute Section 4 cells
- Review cross-validation results
- Check model performance metrics

### Step 6: Visualizations

- Execute Section 5 cells
- All charts saved automatically

### Step 7: Summary

- Execute Section 6 cells
- Review JSON summary file

---

## Output Files Generated

### Datasets (CSV)

- `master_df_0.csv` (~450 MB)
- `english_dataset_langdetect.csv` (~50 MB)

### Embeddings (Pickle)

- `english_dataset_bert_embeddings.pkl` (~200 MB)

### Models (Joblib)

- `svm_baseline_model.joblib` (~5 MB)

### Reports (Text/JSON)

- `classification_report.txt`
- `baseline_results.json`
- `iteration_0_summary.json`
- `pipeline.log`

### Visualizations (PNG @ 300 DPI)

- `confusion_matrix.png`
- `confusion_matrix_normalized.png`
- `roc_pr_curves.png`
- `performance_metrics.png`

---

## Troubleshooting

### GPU Out of Memory

- Reduce `batch_size` in EMBEDDING_CONFIG
- Reduce `max_length` if needed

### File Not Found

- Verify paths in DATA_FILES configuration
- Check BASE_DIR is correct for your system

### Langdetect Issues

- Install: `pip install langdetect`
- May need: `pip install --upgrade langdetect`

### BERT Download Issues

- First run downloads ~440 MB model
- Ensure internet connection stable
- Cache stored in `~/.cache/huggingface/`

### Memory Issues During Training

- Check available RAM
- Consider using GPU for embeddings
- Batch processing handles large datasets

---

## Recommended Next Steps

1. **Run the notebook** from top to bottom
2. **Check results** in the Results directory
3. **Review metrics** in classification_report.txt
4. **Compare baseline** for future iterations
5. **Modify CONFIG** for different parameter experiments
6. **Save checkpoints** before making changes

---

## Key Academic Contributions

✓ **Reproducibility:** Complete parameter logging
✓ **Methodology:** Proper train-test-validation split
✓ **Metrics:** Beyond accuracy (ROC-AUC, F1, Precision, Recall)
✓ **Robustness:** Cross-validation and stratified splitting
✓ **Documentation:** Professional code and results
✓ **Imbalance Handling:** Class weights and stratification
✓ **Code Quality:** Type hints, docstrings, error handling

---

## Citation Format

For thesis reference:

```
Iteration 0 Baseline: SVM with BERT embeddings
- BERT Model: bert-base-uncased (768D)
- Classifier: Support Vector Machine (RBF kernel)
- Validation: 5-Fold Stratified Cross-Validation
- Evaluation Metrics: Accuracy, Precision, Recall, F1, ROC-AUC
- Class Imbalance: Balanced class weights
```

---

**Last Updated:** January 15, 2026
**Version:** 1.0 Professional Edition
**Status:** Production Ready
