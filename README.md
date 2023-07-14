# Bangla Persosn-Name Extractor
This repository contains code for extracting `person-name` form bangla text.

# Data Analysis and Preprocessing
## Analysis
We got two datasets.
1. [Rifat1493/Bengali-NER/annotated data](https://github.com/Rifat1493/Bengali-NER/tree/master/annotated%20data) (data_1), and
2. [banglakit/bengali-ner-data](https://raw.githubusercontent.com/banglakit/bengali-ner-data/master/main.jsonl) (data_2)

After looking through the data it is found that data_1 is in `IOB` notation and data_2 is in `BILUO` notation. So, we need to process the data to be in similar notation. We will use `BILUO` notation for our project as initial plan is to use `spacy`.

## Preprocessing
### Step 1:
To process the data, we first need to download them. A [function](./data_processing.py#L4) was written to save two dataset in two seperate files.
### Step 2:
Now we need to convert both the data into similar format. Data_1 is tokenized, but Data_2 is not. We will need a tokenizer for tokenizing data_2. We will modify (bert tokenizer)[https://github.com/google-research/bert/blob/master/tokenization.py]. We will convert both data into below format for processing further.
```py
[
    {
        "tokens": ["ইব্রাহীম", "ভালো", "কোডিং", "পারে", "।"],
        "tags": ["B-PER", "O", "O", "O", "O"],
    },
]
```
N.B. (1): We found that some words in data_1 has no tag tag for it, so we will remove those tokens. Also some sentence have extra tags, we will remove those also. There are many more issues in the data i.e. there is a person name but it is tagged as `O`, same person name is tagged as `PERSON` in some sentence and tagged as `O` in other sentence, etc. We will ignore these as we have limited time for the submission.

After this we will convert `IOB` notation into `BILUO` notation and we will also remove all NER tags other than `Person` tags. We will changes all `x-PERSON` tag to `x-PER` tag for consistancy across data.

N.B. (2): After removing other tags than `Person` we have some sentences with `Person` and some sentences with `O` tags only (which actually means no tag). To prevent skewness is data we will make train, test, validation sets from those two categories seperately.

N.B. (3): The tokenizer we created from bert tokenizer treat all punctuations as token. Which leads to converting `মো.` --> `মো` and `.`, `ডা.` --> `ডা` and `.`, `৯.৭` --> `৯` and `.` and `৭`, `কো-অপারেটিভ` --> `কো` and `-` and `অপারেটিভ`, etc. This results into inconsistency in token lengths and tag lengths. We will modify the tokenizer to not tokenize on `.` character. But data_1 has `.` as a seperate token and `-` not seperated i.e. `মো.` --> `মো` and `.`, and `কো-অপারেটিভ` --> `কো-অপারেটিভ`. We will modify the processing steps for data_1 so that these cases match on both datasets. We will merge `মো` and `.` --> `মো.`, and split `কো-অপারেটিভ` --> `কো` and `-` and `অপারেটিভ`. We will also modify the tags accordingly.

With above processing we were able to retieve data with below numbers.
```
Data summary:
------------------------------
Total sentence : 6580
Sentence with person tag: 1776
Sentence without person tag: 4804

Data summary:
------------------------------
Total sentence : 3494
Sentence with person tag: 1189
Sentence without person tag: 2305
```

### Step 3:
We will merge sentences containing `PERSON` tag from both dataset (data_1 data_2) and split them into train, validation, and test set in (80%,10%,10%) ratio respectively.
We will merge sentences without `PERSON` tag from both dataset (data_1 data_2) and split them into train, validation, and test set in (80%,10%,10%) ratio respectively.
Now, we will merge both train data (with and without `PERSON` tag) into one and convert them to spacy data format (spacy binary data). We will do the same for validation and test set also.

```
Training data summary :  Data with PERSON tag
------------------------------
Number of train samples :  2372
Number of validation samples :  296
Number of test samples :  297
-----------------------------------
Number of total data :  2965

Training data summary :  Data without PERSON tag
------------------------------
Number of train samples :  5687
Number of validation samples :  711
Number of test samples :  711
-----------------------------------
Number of total data :  7109

Training data summary :  All data
------------------------------
Number of train samples :  8059
Number of validation samples :  1007
Number of test samples :  1008
-----------------------------------
Number of total data :  10074
```

## Model Training
We will fine-tune (`BERT` model)[https://huggingface.co/csebuetnlp/banglabert] from (BUET CSE NLP group)[https://huggingface.co/csebuetnlp] using spacy. We chose to fine-tune this model because this model better test result claimed by (BUET CSE NLP group)[https://huggingface.co/csebuetnlp] and moderate numbers of parameters (110 M) to be trained on free cloud GPUs (Google Colab)[https://colab.research.google.com/]. 