import os
import requests

def download_data(save_dir: str):
    """This function downloads dataset using the links provided in the test description.

    Args:
        save_dir (str): directory to save data

    """
    # create data folders
    os.makedirs(save_dir, exist_ok=True)
    # url for data_1 (https://github.com/Rifat1493/Bengali-NER/tree/master/annotated%20data)
    url_1 = 'https://raw.githubusercontent.com/Rifat1493/Bengali-NER/master/annotated%20data/'
    # create an empty file
    data_path_1 = os.path.join(save_dir, "data_1_raw.txt")
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
    data_path_2 = os.path.join(save_dir, "data_2_raw.jsonl")
    with open(data_path_2, "w", encoding="utf-8") as file:
        file.write(res.text)
    # print a message after completion of downloading data
    print("Successfully downloaded data.")