Combined master_df (before removing duplicates): (790405, 36)
Total records before deduplication: 790,405

Per-source record counts:
  14K (PS):           14,432
  28K (ALL):          28,323
  30K (ALL v2):       30,609
  700K (NH_OBS):     717,041
  ───────────────────────────────────
  Total:             790,405

Total columns: 36
Columns: ['CASENO', 'COMPANY', 'FUNCTIONAL_GROUP', 'FUNCTION', 'FUNCTIONAL_AREA', 'FUNCTIONAL_LOCATION', 'FUNCTIONAL_SUB_LOCATION', 'LOCATION_SID', 'LOCATION_SHORT', 'COUNTRY_SHORT', 'SL_COUNTRY', 'SL_LOCATION_LVL_1', 'SL_LOCATION_LVL_2', 'SL_LOCATION_LVL_3', 'SL_LOCATION_LVL_4', 'CASE_OCCURENCE_DATE', 'TITLE', 'COMPANY_INVOLVED_TYPE', 'CASE_TYPE', 'CASE_SEVERITY', 'CASE_DESCRIPTION', 'STATUS', 'HAZARD', 'IMM_ACTION_TAKEN_RECOM', 'FULL_INVESTIGATION_DONE', 'CREATED_DATE', 'MODIFIED_DATE', 'APPROVED_WITHIN_DEADLINE', 'CASE_CLOSED_DATE', 'CASES_NO_OF_REGISTRATIONS', 'VALID_FROM', 'VALID_TO', 'POTENTIAL_SEV_LEVEL', 'RISK_AREA', 'LEARNINGS_ACTUAL_SEVERITY', 'LEARNINGS_POTENTIAL_RISK']




International
Unknown 


UK
Russia
Poland
UAE

Germany
Sweden
NetherLands
Hungary

International
Unknown

Make Iterations 1 to 8 consistent with Iteration 0, follow these steps:

Review Iteration 0: Open _iteration_0.ipynb and note the key steps, code structure, data preprocessing, column naming, language code handling, and output formats.

Compare Structure: For each of _Iteration_1.ipynb to _iteration_8.ipynb, compare:

Data loading (file paths, formats). Use the master_df output from iteration_0: /Users/shariarimrozekhan/Documents/GitHub/masterThesis2026/Master Dataset 34k/master_df.json
Data cleaning and preprocessing steps can be skipped as I already did in in iretation_0
Feature engineering and model input preparation
Model training, evaluation, and output cells
Output file naming and saving conventions
Standardize Language Handling: Ensure all notebooks use the same mapping for language codes (e.g., "English" → "EN", "German" → "DE", etc.) and apply it to the same column.

Unify Preprocessing: Make sure all data cleaning, missing value handling, and feature creation steps are identical.

Consistent Outputs: All result files, plots, and metrics should be saved in the same format and folder structure as in Iteration 0.

Code Comments and Markdown: Ensure markdown explanations and code comments are clear and follow the same style as Iteration 0.

Instructions:

Open _iteration_0.ipynb and one of the other iteration notebooks side by side.
For each section (data load, preprocessing, modeling, output), copy or adapt code from Iteration 0 to the other notebook, replacing or updating as needed.
Pay special attention to language code replacement and any custom functions or mappings.
Repeat for all notebooks from Iteration 1 to 8.
Test each notebook by running all cells to ensure outputs match the style and structure of Iteration 0.

Checklist: 
1. Data Loading

Use the same file paths and formats as in Iteration 0.
Ensure the same columns are loaded and in the same order.
2. Data Preprocessing

Apply identical cleaning steps (e.g., missing value handling, type conversions).
Use the same language code mapping (e.g., "English" → "EN", etc.).
Standardize column names and ensure all required columns are present.
3. Feature Engineering

Create features in the same way as Iteration 0.
Use the same functions or code blocks for feature extraction.
4. Model Training & Evaluation

Use the same model type, parameters, and training process.
Evaluate using the same metrics and methods.
5. Output Consistency

Save results (e.g., predictions, metrics, plots) in the same format and folder structure.
Use consistent file naming conventions.
6. Code Structure & Comments

Organize code cells in the same logical order.
Use similar markdown explanations and code comments for clarity.
7. Visualizations

Generate the same plots/figures with matching styles and labels.
8. Reproducibility

Ensure all random seeds and environment settings are set as in Iteration 0.


From iteration 2: 

Notes and References: 

https://huggingface.co/transformers/v2.4.0/pretrained_models.htmlhttps://huggingface.co/transformers/v2.4.0/pretrained_models.html 

which to use: TensoFlow or Pytorch?

https://viso.ai/deep-learning/pytorch-vs-tensorflow/#:~:text=However%2C%20the%20core%20difference%20between,resulting%20in%20generally%20higher%20flexibility.

A Brief Recap
The answer to the question “What is better, PyTorch vs Tensorflow?” essentially depends on the use case and application.

In general, TensorFlow and PyTorch implementations show equal accuracy. However, the training time of TensorFlow is substantially higher, but the memory usage was lower.

PyTorch allows quicker prototyping than TensorFlow. However, TensorFlow may be a better option if custom features are needed in the neural network.

TensorFlow treats the neural network as a static object. So, if you want to change the behavior of your model, you have to start from scratch. 

With PyTorch, the neural network can be tweaked on the fly at run-time, making it easier to optimize the model.

Another major difference lies in how developers go about debugging. Effective debugging with TensorFlow requires a special debugger tool to examine how the network nodes do calculations at each step. 

PyTorch can be debugged using one of the many widely available Python debugging tools.

Both PyTorch and TensorFlow provide ways to speed up model development and reduce the amount of boilerplate code. However, the core difference between PyTorch and TensorFlow is that PyTorch is more “Pythonic” and based on an object-oriented approach. 

At the same time, TensorFlow provides more options to choose from, resulting in generally higher flexibility. For many developers familiar with Python, this is an important reason why PyTorch is better than TensorFlow.

https://huggingface.co/transformers/v2.4.0/pretrained_models.html

MODELS = {
    'bert-base': 'bert-base-cased', # trained on only english text
    'bert-large': 'bert-large-cased', # trained on only english text
    'roberta-base': 'roberta-base', # trained on only english text - check
    'roberta-large': 'roberta-large', # trained on only english text - check
    'distilbert': 'distilbert-base-cased', # trained on only english text - check
    'xlnet-base': 'xlnet-base-cased', # trained on only english text
    'modernbert-base': 'answerdotai/ModernBERT-base',
    'modernbert-large': 'answerdotai/ModernBERT-large'
    # Add more models as needed
}

