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


from iteration 3:

Notes and References: 

https://cholakovit.com/en/ai/embeddings/sentence-transformers

https://arxiv.org/pdf/2002.06652

https://viso.ai/deep-learning/pytorch-vs-tensorflow/#:~:text=However%2C%20the%20core%20difference%20between,resulting%20in%20generally%20higher%20flexibility.

file:///C:/Users/M02555/OneDrive%20-%20Uniper%20SE/1.%20Thesis/Books/Pattern%20Recognition%20and%20Machine%20Learning%20-%20Bishop.pdf

https://zilliz.com/ai-faq/what-are-some-popular-pretrained-sentence-transformer-models-and-how-do-they-differ-for-example-allminilml6v2-vs-allmpnetbasev2

https://arxiv.org/pdf/2008.08567

https://huggingface.co/transformers/v3.0.2/multilingual.html

https://huggingface.co/google-bert/bert-base-multilingual-uncased

https://arxiv.org/pdf/2008.08567

https://huggingface.co/models?language=multilingual


From iteration 4:
Notes and References: 
SVM: https://www.youtube.com/watch?v=_YPScrckx28
xgboost', 'lightgbm', 'random_forest', 'ensemble'

Overall, **the approach is directionally correct**, but in its current form it is still **methodologically vulnerable**. The repository now contains notebooks `_iteration_0.ipynb` through `_iteration_8.ipynb`. Iteration 0 establishes the English baseline; Iteration 1 moves to country-stratified BERT-base-cased experiments; Iteration 2 loads the cleaned 34,576-record master dataset and evaluates multiple transformer models on manual English/German/Swedish/Dutch subsets; Iteration 7 is a multilingual few-shot LLM PS/NPS pipeline; and Iteration 8 explicitly targets RQ3 through hazard-type classification with a Flan-T5-based setup. ([GitHub][1])

The strongest part of your design is the **iterative ladder**: establish a defensible baseline, vary dataset construction, then vary encoders/models, then vary balancing/robustness strategies, and only afterward test direct LLM classification. That is exactly the kind of progression a thesis committee usually likes, because it creates a causal narrative rather than a bag of disconnected experiments. Your current Iteration 0 baseline is also coherent in principle: the saved report files show manual English at accuracy 0.8112 and macro-F1 0.7825, versus 0.7636 for `langdetect` and 0.7714 for `lingua`, so retaining the manually curated subset as the official baseline is defensible. ([GitHub][2])

Where the thesis becomes vulnerable is **not the existence of iterations**, but whether each iteration is explicitly tied to a research question and whether the comparisons are genuinely fair.

## Does the approach answer the research questions?

### RQ1

For **RQ1**, your approach is good. You have a fixed baseline from Iteration 0, and the later iterations are clearly designed to exceed it via multilingual modelling, architecture comparison, and enhanced training pipelines. That is the right experimental logic. The risk is not the design itself, but whether the reported improvements are based on a **single consistent dataset regime** and a **single consistent evaluation protocol** across the iterations.

### RQ2

For **RQ2**, your approach is only **partially correct**. Comparing traditional ML and LLM-based systems is valid, but only if the comparison is framed carefully. Iteration 7 is not “LLMs in general”; it is specifically **few-shot Flan-T5-style direct classification** under one prompting setup. The moment you generalise that into “traditional ML is better than LLMs,” a professor can object that you tested only one narrow LLM regime, not fine-tuned LLMs, not API-grade frontier models, and not hybrid LLM+classifier pipelines. The correct claim is narrower: *in the current experiments, direct few-shot LLM classification underperformed trained embedding-classifier pipelines.*

### RQ3

For **RQ3**, Iteration 8 is the right direction, but this is one of the most attackable parts of the thesis. The notebook explicitly states that it extracts and analyses the `HAZARD` column, identifies hazard types, and then uses a Process Safety-trained LLM to classify hazard types. That means your construct validity must be extremely clear: are you using `HAZARD` only to **define the ground-truth taxonomy**, or are you inadvertently using it in a way that leaks target information into the model design? Since RQ3 is about identifying hazard types **from titles and descriptions**, any ambiguity here will be a serious weakness. ([GitHub][3])

### RQ4

**RQ4 is the weakest part** of the thesis. At present, it is a framework proposal, not a full empirical experiment. That can still be acceptable at Master’s level, but only if you state very explicitly that RQ4 is answered at the level of **conceptual suitability and framework design**, not through completed predictive benchmarking. If you leave the wording empirical while the evidence remains conceptual, that is one of the easiest ways a committee can say the research question was not actually answered.

## Where a professor can attack you hard

### 1. Internal inconsistency of numbers

This is the single biggest danger. A professor can fail or heavily downgrade the thesis if the abstract, methodology, results, discussion, and conclusion use different numbers for the same experiment. You already had this problem in Iteration 0 and Iteration 1 drafts. If even one chapter still says that Iteration 1 achieved macro-F1 around 0.88 while the current notebook outputs are around 0.60–0.74 depending on dataset, that immediately damages credibility. The same applies if old 54,750-record claims remain while the current pipeline clearly operates from the 34,576-record cleaned master dataset.

### 2. Apples-to-oranges comparisons across iterations

A committee member can ask:
**“Are these improvements due to a better model, a different dataset, a different split, or a different label space?”**

That is a serious question in your thesis. Some iterations are on the manual English subset, some on country-specific subsets, some on multilingual groupings, and Iteration 7 loads a different multilingual CSV-based corpus totaling 60,767 records with 9,494 Process Safety cases. If you compare those results as though they were on the same benchmark, that is methodologically weak. ([GitHub][4])

### 3. Overclaiming what “LLM comparison” means

A professor can ask:
**“Why should I accept that RQ2 is answered if your LLM side is basically one few-shot Flan-T5 setup?”**

That is a fair criticism. Your current Iteration 7 notebook is a few-shot multilingual prompting pipeline. It is not a comprehensive LLM benchmark. So your conclusion must be framed as: *direct few-shot prompting was not competitive in this setting*, not *LLMs are inferior to traditional ML*. ([GitHub][4])

### 4. Construct validity and leakage in RQ3

A professor can ask:
**“If hazard types are built from the `HAZARD` column, how do you prove the model is learning from titles and descriptions rather than from a taxonomy engineered from the labels themselves?”**

This is probably the sharpest technical criticism available against RQ3. If the taxonomy design, label cleaning, and evaluation protocol are not separated cleanly, RQ3 will look like label engineering rather than hazard extraction.

### 5. RQ4 may be judged “not answered”

A professor can ask:
**“Where is the actual severity prediction experiment?”**

If your answer is that you designed the framework but did not implement the benchmark, then the thesis must present RQ4 as a **design-oriented research contribution**, not a completed experimental result. Otherwise, the committee can say one of your four research questions remains empirically unanswered.

### 6. Lack of statistical rigor

A strong examiner may ask:

* Why no repeated stratified cross-validation?
* Why no confidence intervals?
* Why no significance test for differences between top models?
* Why is model selection based only on a single split?

If your thesis relies mainly on one 80/20 split per experiment, that is defendable as an exploratory industrial study, but you must state that limitation explicitly.

### 7. Weak causal interpretation of improvement

A professor can ask:
**“How do you know the gain comes from mean pooling rather than SMOTE, or from LightGBM rather than the new multilingual embeddings?”**

Your thesis becomes much stronger if each later iteration is interpreted as testing one main hypothesis. Otherwise the committee can say the thesis contains many experiments, but weak scientific attribution.

### 8. Business-case relevance

A practical examiner can ask:
**“Why should Uniper trust this model in deployment if the strongest results are not clearly tied to calibration, explainability, thresholding, and error cost?”**

For an industrial thesis, raw macro-F1 alone is not enough. You need to show that the model helps the business case: fewer missed Process Safety incidents, interpretable errors, operational thresholding, and realistic deployment trade-offs.

## The most dangerous viva questions

These are the kinds of questions that could seriously hurt the thesis if you do not have crisp answers:

1. **Why is Iteration 0 the official baseline if some later automatic subsets have higher accuracy?**
   Correct answer: because macro-F1 is the primary selection metric under class imbalance, and the manual subset produced the strongest class-balanced result.

2. **Why is Iteration 1 much weaker than the later results?**
   You need to explain that country stratification exposed the weakness of monolingual BERT-base-cased + Linear SVM under multilingual and imbalanced conditions, which motivated Iterations 2–4.

3. **Are your later improvements due to better models or different datasets?**
   You need a clean answer about benchmark comparability.

4. **What exactly is being compared in RQ2?**
   Not “traditional ML vs LLMs in general,” but “trained embedding-classifier pipelines vs direct few-shot LLM classification under the current experimental setup.”

5. **How is RQ3 evaluated without leakage from the HAZARD field?**
   This needs a precise methodological answer.

6. **Why should RQ4 be accepted if you did not run the full experiment?**
   Your answer must be: because the contribution is a rigorously justified framework, not a claimed finished predictive benchmark.

## My judgement

Your **overall research strategy is good enough for a strong Master’s thesis**, but only if you tighten the thesis around a stricter scientific narrative:

* **Iteration 0–1:** establish the problem and baseline sensitivity
* **Iteration 2–4:** answer RQ1 through controlled model and pipeline improvements
* **Iteration 5–6:** analyse class-balancing trade-offs and robustness
* **Iteration 7:** limited RQ2 evidence on direct few-shot LLM classification
* **Iteration 8:** targeted RQ3 hazard-type extraction study
* **RQ4:** explicitly framed as a conceptual framework contribution, not a completed benchmark

If you do that, the thesis looks coherent. If you leave it as a sequence of partially synchronized experiments with broad claims, a professor has multiple legitimate ways to attack it.

The **single most important action now** is to make every chapter defend the same story, using one consistent set of numbers and one precise claim per research question.

[1]: https://github.com/ShariarImroze/masterThesis2026/tree/main/_Iterations "masterThesis2026/_Iterations at main · ShariarImroze/masterThesis2026 · GitHub"
[2]: https://raw.githubusercontent.com/ShariarImroze/masterThesis2026/main/Results/_iteration_0/classification_report_manual.txt "raw.githubusercontent.com"
[3]: https://raw.githubusercontent.com/ShariarImroze/masterThesis2026/main/_Iterations/_iteration_8.ipynb "raw.githubusercontent.com"
[4]: https://raw.githubusercontent.com/ShariarImroze/masterThesis2026/main/_Iterations/_iteration_7.ipynb "raw.githubusercontent.com"


