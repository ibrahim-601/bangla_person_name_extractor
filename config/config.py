# tags we want to keep. tags not listed here will be removed
TAGS_TO_KEEP = []

# punctuation to not tokenize. punctuation listed here will not be tokenized seperately
SKIP_PUNC = [".",]

# raw data related directory and file names
RAW_DATA_DOWNLOAD_DIR = "data_raw"
RAW_DATA_1_FILE_NAME = "data_1_raw.txt"
RAW_DATA_2_FILE_NAME = "data_2_raw.jsonl"

# processesed data related directory and file names
PROCESSESED_DATA_SAVE_DIR = "data_processesed"
PROCESSESED_DATA_1_NAME = "data_1.json"
PROCESSESED_DATA_2_NAME = "data_2.json"

# final training, validation data paths
TRAIN_DATA_PATH = "dataset/train.spacy"
VALID_DATA_PATH = "dataset/valid.spacy"
TEST_DATA_PATH = "dataset/test.spacy"

# training data split percentage as float
# percentage of test+validation data w.r.t. total data
TEST_VAL_PERCENTAGE = 0.20 # 20% of total data
# percentage of test data w.r.t. test+validation data
TEST_PERCENTAGE = 0.50 # 50% of test+validation data, which is 10% of total data

# model directory
MODEL_DIR = "./models/bangla_person_ner"
# public url of model
MODEL_URL = "https://drive.google.com/drive/folders/1ZpCcXqqYpOnuasPmK6zYgMJM_iJICoWt"