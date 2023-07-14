import argparse
import spacy
from config import config as cfg

# Load the model
model = spacy.load(cfg.MODEL_DIR)

def extract_person_name(text: str) -> dict:
    """This function takes a text string and extract bangla person names from the text
    and return the results as list of dictionary. Each dictionary in returned list
    contains text of the name, start and end position in tokenized text.

    Args:
        text (str): text on which we want to perform name extraction

    Returns:
        dict: dictionary in format
                {
                    "sentence" : text,
                    "extracted_names" : [
                        {
                            "name": entity_text, 
                            "label": entity_label,
                            "start": entity_start,
                            "end": entity_end
                        }
                    ]
                }
    """
    # initialize variable to store and return outputs
    result = {
      "sentence" : text,
      "extracted_names" : []
    }
    # get prediction on model
    doc = model(text)
    
    # if no name found then add "no name is found" as extracted names and return
    if not doc.ents:
      result["extracted_names"] = "কোন নাম খুঁজে পাওয়া যায় নি/No name is found"
      return result

    # iterate over each entity and append entity details to extracted names
    for entity in doc.ents:
        result["extracted_names"].append(
            {
                "name": entity.text, 
                "label": entity.label_,
                "start": entity.start,
                "end": entity.end
            }
        )
    # return the result
    return result

if __name__ == "__main__":
    # define list of sentences
    texts = [
        "এ ট্যাবলেটটির নাম হতে পারে 'আইপ্যাড ম্যাক্সি'।",
        "মো. আলমের কাছ থেকে ১৫ লাখ টাকা আদায় করা হয়।",
        "এতিমখানার কর্মকর্তা-শিক্ষার্থীরা কমিটি ও চুক্তির বিরুদ্ধে আন্দোলন শুরু করে।",
        "ডা. মো. শরিফুল ইসলাম, শহীদ সোহরাওয়ার্দী মেডিকেল, কলেজ ও হাসপাতাল।"
    ]
    # take prediction for every sentence and print the results
    for text in texts:
        res = extract_person_name(text)
        print(res)