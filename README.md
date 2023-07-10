# Bangla Persosn-Name Extractor
This repository contains code for extracting `person-name` form bangla text.

# Data Analysis and Preprocessing
## Analysis
We got two datasets.
1. [Rifat1493/Bengali-NER/annotated data](https://github.com/Rifat1493/Bengali-NER/tree/master/annotated%20data) (data_1), and
2. [banglakit/bengali-ner-data](https://raw.githubusercontent.com/banglakit/bengali-ner-data/master/main.jsonl) (data_2)

After looking through the data it is found that data_1 is in `IOB` notation and data_2 is in `BLIOU` notation. So, we need to process the data to be in similar notation. We will use `BLIOU` notation for our project as initial plan is to use `spacy`.

## Preprocessing
### Step 1:
To process the data, we first need to download them. A [function](./data_processing.py#L4) was written to save two dataset in two seperate files.
### Step 2:
Now we need to convert both the data into similar format. Data_1 is tokenized, but Data_2 is not. We will need a tokenizer for tokenizing data_2. We will modify (bert tokenizer)[https://github.com/google-research/bert/blob/master/tokenization.py]. We will convert both data into below format for processing further.
```py
[
    {
        "tokens": ["ইব্রাহীম", "ভালো", "কোডিং", "পারে", "।"],
        "tags": ["B-PERSON", "O", "O", "O", "O"],
    },
]
```
After this we will convert `IOB` notation into `BLIOU` notation and then we will remove all NER tags other than `Person` tags.