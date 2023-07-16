import os
import spacy
from spacy.tokens import DocBin, Doc, Span
from spacy.training.iob_utils import tags_to_entities
from sklearn.model_selection import train_test_split
from config import config as cfg

def _split_train_val_test(data: list) -> tuple:
    """This function takes data as a list and splits it into train, validation, and test set.

    Args:
        data (list): data as list

    Returns:
        tuple: tuple of train, validation, and test set of data
    """
    # split into train data and test+validation data
    train_data, test_val_data = train_test_split(data, test_size=cfg.TEST_VAL_PERCENTAGE)
    # split into validation data and test data
    test_data, val_data = train_test_split(test_val_data, test_size=cfg.TEST_PERCENTAGE)
    # return train, validation, and test data as tuple
    return (train_data, val_data, test_data)

def _convert_save_spacy_binary(data: list, save_path: str):
    """This function converts our custom data into spacy binary format.
    This piece of code is inspired from spacy conll_ner_to_docs converter.

    Args:
        data (list): list of data in custom format
        save_path (str): path where the binary file will be saved
    """
    # initialize a blank model
    nlp = spacy.blank("bn")
    # initialize DocBin to store the converted binary data
    db = DocBin()
    # iterate over each data
    for dict_data in data:
        # extract tokens and tags from data
        tokens, tags = dict_data["tokens"], dict_data["tags"]
        # create token object
        doc = Doc(nlp.vocab, words=tokens)
        # generate entities with additional info
        entities = tags_to_entities(tags)
        # add entities with span info to the token object
        doc.ents = [Span(doc, start=s, end=e + 1, label=L) for L, s, e in entities]
        # add the token object to binary data
        db.add(doc)
    # create directories to save data
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    # write spacy binary data to file
    db.to_disk(save_path)

def _print_data_processing_summary(data_name: str, train_len: int, val_len: int, test_len: int):
    """This function prints summary of data proccessing.

    Args:
        processed_data (dict): dictionary of processed data
        data_name (str): Name of data set.
    """
    print("\nTraining data summary : ", data_name)
    print("-"*30)
    print("Number of train samples : ", train_len)
    print("Number of validation samples : ", val_len)
    print("Number of test samples : ", test_len)
    print("-"*35)
    print("Number of total data : ", train_len + val_len + test_len)

def split_and_convert_data(data: list):
    """This function takes data for tuple with two types of data.

    Args:
        data (list): _description_

    Returns:
        tuple: _description_
    """
    # take data_1 and data_2 from data
    data_1, data_2 = data
    # merge data containing person tag from both data_1 and data_2
    all_person_data = data_1["person"] + data_2["person"]
    # merge data containing no person tag from both data_1 and data_2
    all_no_person_data = data_1["no_person"] + data_2["no_person"]
    # get train, validation and test set for data with person tag
    train_person, valid_person, test_person = _split_train_val_test(all_person_data)
    # print stats of data containing person tag
    _print_data_processing_summary("Data with PERSON tag", len(train_person), len(valid_person), len(test_person))
    # get train, validation and test set for data without person tag
    train_no_person, valid_no_person, test_no_person = _split_train_val_test(all_no_person_data)
    # print stats of data without person tag
    _print_data_processing_summary("Data without PERSON tag", len(train_no_person), len(valid_no_person), len(test_no_person))
    # merge train set for both data with and without person tag
    train = train_person+train_no_person
    # merge validation set for both data with and without person tag
    valid = valid_person+valid_no_person
    # merge validation set for both data with and without person tag
    test = test_person+test_no_person
    # print stats of total training data
    _print_data_processing_summary("All data", len(train), len(valid), len(test))
    # save data to binary format
    print("\nSaving spacy binary format data...")
    # save train data in spacy binary format
    _convert_save_spacy_binary(train, cfg.TRAIN_DATA_PATH)
    print("Saved train data at : ", cfg.TRAIN_DATA_PATH)
    # save validation data in spacy binary format
    _convert_save_spacy_binary(valid, cfg.VALID_DATA_PATH)
    print("Saved train data at : ", cfg.VALID_DATA_PATH)
    # save test data in spacy binary format
    _convert_save_spacy_binary(test, cfg.TEST_DATA_PATH)
    print("Saved train data at : ", cfg.TEST_DATA_PATH)
    # print stats of training data
    
if __name__ == "__main__":
    import json
    # process text data (data_1)
    data_1 = json.load(open(cfg.PROCESSESED_DATA1_PATH, encoding="utf-8"))
    # process jsonl data (data_2)
    data_2 = json.load(open(cfg.PROCESSESED_DATA2_PATH, encoding="utf-8"))
    split_and_convert_data(data=(data_1,data_2))