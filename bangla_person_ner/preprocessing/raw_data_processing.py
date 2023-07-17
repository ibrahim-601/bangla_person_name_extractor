import os
import re
import json
from spacy.training.iob_utils import iob_to_biluo
from ..utils.downloader import download_data 
from ..utils.tokenizer import BasicTokenizer
from ..config import config as cfg

# initialize a tokenizer object
tokenizer = BasicTokenizer()

def _write_json(json_data: json, json_save_path: str):
    """This function saves json data to given path.

    Args:
        json_data (json): Json data to save
        json_save_path (str): path to save json data
    """
    # create folders if not exists
    os.makedirs(os.path.dirname(json_save_path), exist_ok=True)
    # open file for writing with "utf-8" encoding
    with open(json_save_path, "w", encoding="utf-8") as f:
        # write json data to file
        f.write(json.dumps(json_data, ensure_ascii=False, indent=4))

def _remove_unwanted_tags(tags: list) -> list:
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
        if tag.upper() not in cfg.TAGS_TO_KEEP:
            updated_tags.append("O")
        # otherwise add the tag into updated tags
        else:
            # replace PER with PERSON in the tag so that tag is similar in both dataset
            tag = re.sub(r"PER$", "PERSON", tag, flags=re.IGNORECASE)
            updated_tags.append(tag)
    # return the updated tags
    return updated_tags

def _handle_dot_and_minus_text(tokens: list, tags: list) -> tuple:
    """This function merges "." with previous token and split token by "-".
    and updates tag accordingly for text data.

    Args:
        tokens (list): List of tokens strings
        tags (list): list of tags for the tokens

    Returns:
        tuple: tuple of two lists. first ones is token list and second is tag list.
    """
    # initialize variables
    new_tokens, new_tags = [], []
    # iterate over tokens and tags
    for token, tag in zip(tokens, tags):
        # if token is "." then append with previus token
        if token == "." and new_tokens:
            new_tokens[-1] = new_tokens[-1] + "."
        # if token is "-" and tag is "O" then tokenize the token
        # for each part of the token add "O" tag to the list
        elif "-" in token and tag=="O":
            token_parts = tokenizer.tokenize(token)
            for token_part in token_parts:
                new_tokens.append(token_part)
                new_tags.append(tag)
        else:
            new_tokens.append(token)
            new_tags.append(tag)
    # return new tokens and new tags
    return (new_tokens, new_tags)

def _print_data_processing_summary(processed_data: dict, data_name: str):
    """This function prints summary of data proccessing.

    Args:
        processed_data (dict): dictionary of processed data
        data_name (str): Name of data set.
    """
    print("\nData summary: ", data_name)
    print("-"*30)
    print(f"Total sentence : {len(processed_data['no_person']) + len(processed_data['person'])}")
    print(f"Sentence with person tag: {len(processed_data['person'])}")
    print(f"Sentence without person tag: {len(processed_data['no_person'])}")

def _clean_jsonl(text: str) -> str:
    """This function cleans data and places placeholders for non-breaking-space and "..."

    Args:
        text (str): whole jsonl file as string

    Returns:
        str: text after cleaning
    """
    # strip extra spaces
    text = text.strip('\n')
    # remove "|"
    text = text.replace("|", "")
    # add placeholder for non-breaking-space
    text = re.sub(r" +", " xtmpnbsp ", text)
    # add placeholder for "..."
    text = text.replace("...", " xtmpellipsis ")
    # return clean text
    return text

def _handle_nbsp_and_replacement_jsonl(tokens: list, tags: list) -> tuple:
    """This function removes non-breaking-space and replaces temporary placeholder for "..."

    Args:
        tokens (list): List of tokens strings
        tags (list): list of tags for the tokens

    Returns:
        tuple: tuple of two lists. first ones is token list and second is tag list.
    """
    # initialize new variables
    new_tokens, new_tags = [], []
    # iterate over tokens and tags
    for token, tag in zip(tokens, tags):
        # if token is temporary replacement for "..." then revert back
        if token == "xtmpellipsis":
            new_tokens.append("...")
        # if token is temporary replacement for non-breaking-space then skip
        elif token == "xtmpnbsp":
            continue
        # otherwise keep the token as it is
        else:
            new_tokens.append(token)
        # add tag for the token
        new_tags.append(tag)
    # return new tokens and tags
    return (new_tokens, new_tags)

def process_text_data(data_path: str, print_summary: bool = True, save_path: str = "") -> dict:
    """This function does all processing necessary for text data.

    Args:
        data_path (str): path to the text data
        print_summary (bool, optional): If set True print summary of the processed data. Defaults to True.
        save_path (str, optional): If provided writes the processed data as json file. Defaults to "".

    Returns:
        dict: dictionary of processed data. Dictionary has format
                {
                    "person": [
                        {
                        "tokens" : ["ইব্রাহীম", "ভালো", "কোডিং", "পারে", "।"],
                        "tags": ["B-PER", "O", "O", "O", "O"],
                        },
                    ],
                    "person": [
                        {
                        "tokens" : ["আগামীকাল", "পরীক্ষা", "আছে", "।"],
                        "tags": ["O", "O", "O", "O"],
                        },
                    ]
                }
    """
    # initialize variable
    processed_data = {
        'person': [],
        'no_person': [],
    }
    # read text from file
    raw_data = open(data_path, encoding="utf8").read()
    # seperate sentences
    tagged_sentences = raw_data.split("\n\n")
    # process each sentence
    for tagged_sentence in tagged_sentences:
        # if sentence is empty skip
        if not tagged_sentence:
            continue
        # strip extra spaces
        tagged_sentence = tagged_sentence.strip()
        # strip extra new lines
        tagged_sentence = tagged_sentence.strip("\n")
        # seperate words (tokens, tags)
        tagged_words = tagged_sentence.split("\n")
        # initialize variable
        tokens, tags = [], []
        # iterate each word
        for tagged_word in tagged_words:
            # if empty skip
            if not tagged_word:
                continue
            # remove consecutive tab space with single tab space
            tagged_word = re.sub(r"\t+", "\t", tagged_word)
            # remove extra tab space
            tagged_word = tagged_word.strip("\t")
            # seperate token and tag
            word_tag_split = tagged_word.split("\t")
            # if token and tag both does not exists then skip
            if len(word_tag_split)<2:
                continue
            # add token to tokens list
            tokens.append(word_tag_split[0])
            # add tag to tags list
            tags.append(word_tag_split[1])
        # remove unwanted tags (everything except PERSON tag)
        tags = _remove_unwanted_tags(tags)
        # convert from IOB to BILUO
        tags = iob_to_biluo(tags)
        # handle "." and "-" to match with jsonl data
        tokens, tags = _handle_dot_and_minus_text(tokens, tags)
        # format tokens and tags
        processed_dict = {
                "tokens": tokens,
                "tags": tags,
            }
        # seperate by PERSON tags
        if len(set(tags))==1:
            processed_data["no_person"].append(processed_dict)
        else:
            processed_data["person"].append(processed_dict)
    # print summary if flag is on
    if print_summary:
        _print_data_processing_summary(processed_data=processed_data, data_name="data_1")
    # save json if path is passed
    if save_path:
        _write_json(json_data=processed_data, json_save_path=save_path)
    # return processed data
    return processed_data

def process_jsonl_data(data_path: str, print_summary: bool = True, save_path: str = "") -> dict:
    """This function does all processing necessary for jsonl data.

    Args:
        data_path (str): path to the text data
        print_summary (bool, optional): If set True print summary of the processed data. Defaults to True.
        save_path (str, optional): If provided writes the processed data as json file. Defaults to "".

    Returns:
        dict: dictionary of processed data. Dictionary has format
                {
                    "person": [
                        {
                        "tokens" : ["ইব্রাহীম", "ভালো", "কোডিং", "পারে", "।"],
                        "tags": ["B-PER", "O", "O", "O", "O"],
                        },
                    ],
                    "person": [
                        {
                        "tokens" : ["আগামীকাল", "পরীক্ষা", "আছে", "।"],
                        "tags": ["O", "O", "O", "O"],
                        },
                    ]
                }
    """
    # initialize variables
    processed_data = {
        'person': [],
        'no_person': [],
    }
    # read text from file
    raw_data = open(data_path, encoding="utf8").read()
    # clean text
    raw_data = _clean_jsonl(raw_data)
    # seperate lines
    raw_lines = raw_data.split("\n")
    # iterate over each line
    for raw_line in raw_lines:
        # load line data to json
        tagged_sentence = json.loads(raw_line)
        # if length of line json is not 2 then print that and skip
        if len(tagged_sentence)!=2:
            print(f"Issue found with line data : {tagged_sentence}")
            continue
        # get sentence and tags
        sentence, tags = tagged_sentence[0], tagged_sentence[1]
        # tokenize sentence
        tokens = tokenizer.tokenize(sentence)
        # remove unwanted tags (everything except PERSON tag)
        tags = _remove_unwanted_tags(tags)
        # if tokens length is less than tags length and only one type 
        # of tag exits then reduce the tags to token length
        if len(tokens)<len(tags) and len(set(tags))==1:
            tags = [tags[0]]*len(tokens)
        # if length of tokens and length of tags do not match then skip
        if len(tokens)!=len(tags):
            continue
        # remove non-breaking-space and revert back placeholders
        tokens, tags = _handle_nbsp_and_replacement_jsonl(tokens, tags)
        # format tokens and tags
        processed_dict = {
                "tokens": tokens,
                "tags": tags,
            }
        # seperate by PERSON tags
        if len(set(tags))==1:
            processed_data["no_person"].append(processed_dict)
        else:
            processed_data["person"].append(processed_dict)
    # print summary if flag is on
    if print_summary:
        _print_data_processing_summary(processed_data=processed_data, data_name="data_2")
    # save json if path is passed
    if save_path:
        _write_json(json_data=processed_data, json_save_path=save_path)
    # return processed data
    return processed_data

if __name__ == "__main__":
    # download the dataset provided for the project if it does not exist
    data_path_1 = cfg.RAW_DATA1_FILE_PATH
    data_path_2 = cfg.RAW_DATA2_FILE_PATH
    if not os.path.exists(data_path_1) or not os.path.exists(data_path_2):
        download_data()
    # process text data (data_1)
    data_1 = process_text_data(data_path=data_path_1, save_path=cfg.PROCESSESED_DATA1_PATH)
    # process jsonl data (data_2)
    data_2 = process_jsonl_data(data_path=data_path_2, save_path=cfg.PROCESSESED_DATA2_PATH)