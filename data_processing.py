import os
import json
from spacy.training.iob_utils import iob_to_biluo
from utils.downloader import download_data 
from utils.tokenizer import BasicTokenizer

tokenizer = BasicTokenizer()

def remove_unwanted_tags(tags: list) -> list:
    """Removed tags which are not required for this project.

    Args:
        tags (list): list of tags

    Returns:
        list: list of tags after removing not required tags
    """
    # initialize variable for updated tags
    updated_tags = []
    # iterate over each tag
    for tag in tags:
        # if tag does not contain "PER" then add "O" for that tag
        if "per" not in tag.lower():
            updated_tags.append("O")
        # otherwise add the tag into updated tags
        else:
            # replace PERSON with PER in the tag so that tag is similar in both dataset
            tag = tag.replace("PERSON","PER")
            updated_tags.append(tag)
    # return the updated tags
    return updated_tags

def process_text_data(data_path: str, save_path: str) -> list:
    processed_data = {
        'person': [],
        'no_person': [],
    }
    # read data from file
    raw_data = open(data_path, encoding="utf8").read()
    tagged_sentences = raw_data.split("\n\n")
    for tagged_sentence in tagged_sentences:
        if not tagged_sentence:
            continue
        tagged_sentence = tagged_sentence.strip()
        tagged_sentence = tagged_sentence.strip("\n")
        processed_dict = {
                "tokens": [],
                "tags": [],
            }
        tagged_words = tagged_sentence.split("\n")
        for tagged_word in tagged_words:
            if not tagged_word:
                continue
            tagged_word = tagged_word.replace("\t\t", "\t")
            tagged_word = tagged_word.strip("\t")
            word_tag_split = tagged_word.split("\t")
            if len(word_tag_split)<2:
                continue

            processed_dict["tokens"].append(word_tag_split[0])
            processed_dict["tags"].append(word_tag_split[1])
        processed_dict["tags"] = remove_unwanted_tags(processed_dict["tags"])
        processed_dict["tags"] = iob_to_biluo(processed_dict["tags"])
        if len(set(processed_dict["tags"]))==1:
            processed_data["no_person"].append(processed_dict)
        else:
            processed_data["person"].append(processed_dict)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(processed_data, ensure_ascii=False))

def process_jsonl_data(data_path: str, save_path: str) -> list:
    processed_data = {
        'person': [],
        'no_person': [],
    }
    # read data from file
    raw_data = open(data_path, encoding="utf8").read()
    raw_data = raw_data.strip('\n')
    raw_lines = raw_data.split("\n")
    for raw_line in raw_lines:
        tagged_sentence = json.loads(raw_line)
        if len(tagged_sentence)!=2:
            print("Issue found with line data :", tagged_sentence)
            continue
        sentence, tags = tagged_sentence[0], tagged_sentence[1]
        tokens = tokenizer.tokenize(sentence)
        tags = remove_unwanted_tags(tags)
        assert len(tokens)==len(tags), f"tokens and tags count doesn't match. {tokens}, {tags}"
        processed_dict = {}
        processed_dict["tokens"] = tokens
        processed_dict["tags"] = tags
        if len(set(processed_dict["tags"]))==1:
            processed_data["no_person"].append(processed_dict)
        else:
            processed_data["person"].append(processed_dict)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(processed_data, ensure_ascii=False))

if __name__ == "__main__":
    # download the dataset provided for the project if it does not exist
    if not os.path.exists("./data_raw/data_1_raw.txt") or not os.path.exists("./data_raw/data_2_raw.jsonl"):
        download_data("data_raw")
    # process_text_data("./data_raw/data_1_raw.txt", "./data_processed/data_1.json")
    process_jsonl_data("./data_raw/data_2_raw.jsonl", "./data_processed/data_2.json")

