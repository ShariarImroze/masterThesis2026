1. Increase Batch Size for Embeddings
 Find the line:
BATCH_SIZE = 4
 Change it to:
BATCH_SIZE = 12
 If you get memory errors, try BATCH_SIZE = 8 or BATCH_SIZE = 12.

2. Use PyTorch MPS Backend (if available)
 In your get_bert_embeddings function, change device selection from:
device = 'cuda' if torch.cuda.is_available() else 'cpu'
to:
device = 'mps' if torch.backends.mps.is_available() else 'cpu'
 This will use Apple’s Metal backend if available, otherwise CPU.

3. Parallelize Model/Dataset Processing
 Add at the top:
from concurrent.futures import ProcessPoolExecutor
 Replace your main loop with:

def process_one(args):
    model_key, model_name, dataset_name, json_file = args
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
    pkl_file = process_dataset(json_file, model_name, model_key, tokenizer, model, dataset_name=dataset_name)
    result = train_svm_and_evaluate(pkl_file)
    return result

tasks = []
for model_key, model_name in MODELS.items():
    for dataset_name, json_file in json_files:
        item_key = (model_key, dataset_name)
        if item_key not in processed_items:
            tasks.append((model_key, model_name, dataset_name, json_file))

with ProcessPoolExecutor(max_workers=4) as executor:  # Adjust 4 to your CPU core count
    all_results = list(executor.map(process_one, tasks))

 Ensure all code inside process_one is self-contained (no global state).

4. Lower Data Size for Debugging
 For quick tests, set:
MAX_SAMPLES_SVM = 6000
 Restore to MAX_SAMPLES_SVM = 6000 for full runs.

5. Update PyTorch and Transformers
 In your terminal, run:
pip install --upgrade torch torchvision torchaudio transformers
