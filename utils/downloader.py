import os
import requests
import gdown
from config import config as cfg

def download_data():
    """This function downloads dataset using the links provided in the test description.
    """
    # create data folders
    os.makedirs(cfg.RAW_DATA_DOWNLOAD_DIR, exist_ok=True)
    # url for data_1 (https://github.com/Rifat1493/Bengali-NER/tree/master/annotated%20data)
    url_1 = 'https://raw.githubusercontent.com/Rifat1493/Bengali-NER/master/annotated%20data/'
    # create an empty file
    data_path_1 = os.path.join(cfg.RAW_DATA_DOWNLOAD_DIR, cfg.RAW_DATA_1_FILE_NAME)
    open(data_path_1, "w")
    # there is total 20 text file in the repository, we will download all of them using loop
    for i in range(1,21):
        # if i!=1:
        #     continue
        # create url for each file 
        url = url_1 + str(i) + ".txt"
        # get the data
        res = requests.get(url)
        # append the data to a text file
        with open(data_path_1, "a", encoding="utf-8") as file:
            # take the text from the web response and remove first character which is an extra character
            text_data = res.text
            file.write(text_data[1:])
            # add a new line character as this dataset contains sentences seperated with new line
            file.write("\n")

    # url for data_2 (https://raw.githubusercontent.com/banglakit/bengali-ner-data/master/main.jsonl)
    url_2 = 'https://raw.githubusercontent.com/banglakit/bengali-ner-data/master/main.jsonl'
    # get the data
    res = requests.get(url_2)
    # write the data to a text file
    data_path_2 = os.path.join(cfg.RAW_DATA_DOWNLOAD_DIR, cfg.RAW_DATA_2_FILE_NAME)
    with open(data_path_2, "w", encoding="utf-8") as file:
        file.write(res.text)
    # print a message after completion of downloading data
    print("Successfully downloaded data.")

def download_model():
    """This function download model from google drive using the public url set in the config
    """
    model_url = cfg.MODEL_URL
    model_save_dir = cfg.MODEL_DIR
    gdown.download_folder(model_url, output=model_save_dir)

if __name__ == "__main__":
    download_model()