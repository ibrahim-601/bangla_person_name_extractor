import os
import json
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
            updated_tags.append(tag)
    # return the updated tags
    return updated_tags

def process_text_data(data_path: str, save_path: str) -> list:
    processed_data = []
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
        processed_data.append(processed_dict)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(processed_data, ensure_ascii=False))

if __name__ == "__main__":
    # download the dataset provided for the project if it does not exist
    if not os.path.exists("./data_raw/data_1_raw.txt") or not os.path.exists("./data_raw/data_2_raw.jsonl"):
        download_data("data_raw")
    process_text_data("./data_raw/data_1_raw.txt", "./data_processed/data_1.json")

