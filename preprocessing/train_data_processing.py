import os
import spacy
from spacy.tokens import DocBin, Doc, Span
from spacy.training.iob_utils import tags_to_entities
from sklearn.model_selection import train_test_split
from config import config as cfg

def split_data(data: list) -> tuple:
    """This function takes data as a list and splits it into train, validation, and test set

    Args:
        data (list): data as list

    Returns:
        tuple: tuple of train, validation, and test set of data
    """
    # split into train data and test+validation data
    train_data, test_val_data = train_test_split(data, test_size=cfg.TEST_VAL_PERCENTAGE)
    # split into validation data and test data
    val_val, test_data = train_test_split(test_val_data, test_size=cfg.TEST_PERCENTAGE)
    # return train, validation, and test data as tuple
    return (train_data, val_val, test_data)

def convert_spacy_binary(data: list, save_path: str):
    """This function converts our custom data into spacy binary format

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