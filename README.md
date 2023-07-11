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
        "tags": ["B-PER", "O", "O", "O", "O"],
    },
]
```
N.B.: We found that some words in data_1 has no tag tag for it, so we will remove those tokens. Also some sentence have extra tags, we will remove those also. There are many more issues in the data i.e. there is a person name but it is tagged as `O`, same person name is tagged as `PERSON` in some sentence and tagged as `O` in other sentence, etc. We will ignore these as we have limited time for the submission.

After this we will convert `IOB` notation into `BLIOU` notation and we will also remove all NER tags other than `Person` tags. We will changes all `x-PERSON` tag to `x-PER` tag for consistancy across data.

N.B.: After removing other tags than `Person` we have some sentences with `Person` and some sentences with `O` tags only (which actually means no tag). To prevent skewness is data we will make train, test, validation sets from those two categories seperately.

N.B.: The tokenizer we created from bert tokenizer treat all punctuations as token. Which leads to converting `মো.`, `ডা.`, `কো-অপারেটিভ` into `মো` and `.`, `ডা` and `.`, `কো` and `-` and `অপারেটিভ` respectivly. This results into inconsistency in token lengths and tag lengths. We will think of an way to resolve this.