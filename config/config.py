import os

# get absolute path of bangla person name extractor module
_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# tags we want to keep. tags not listed here will be removed.
# Always write tags here in uppercase letters. Do not include "O" tag.
TAGS_TO_KEEP = ["B-PER", "I-PER", "B-PERSON", "I-PERSON", "L-PERSON", "U-PERSON"]

# punctuation to not tokenize. punctuation listed here will not be tokenized seperately
SKIP_PUNC = [".",]

# raw data related directory and file names
RAW_DATA1_FILE_PATH = os.path.join(_module_path,"dataset/data1_raw.txt")
RAW_DATA2_FILE_PATH = os.path.join(_module_path,"dataset/data2_raw.jsonl")

# processesed data related directory and file names
PROCESSESED_DATA1_PATH = os.path.join(_module_path,"dataset/data1_processed.json")
PROCESSESED_DATA2_PATH = os.path.join(_module_path,"dataset/data2_processed.json")

# final training, validation data paths
TRAIN_DATA_PATH = os.path.join(_module_path,"dataset/train.spacy")
VALID_DATA_PATH = os.path.join(_module_path,"dataset/valid.spacy")
TEST_DATA_PATH = os.path.join(_module_path,"dataset/test.spacy")

# training data split percentage as float
# percentage of test+validation data w.r.t. total data
TEST_VAL_PERCENTAGE = 0.20 # 20% of total data
# percentage of test data w.r.t. test+validation data
TEST_PERCENTAGE = 0.50 # 50% of test+validation data, which is 10% of total data

# model directory
MODEL_DIR = os.path.join(_module_path,"models/model-best")
# public url of model
MODEL_URL = "https://drive.google.com/drive/folders/1zJfAVSItJVkHt-ttGgB383VrXeBasAHX"