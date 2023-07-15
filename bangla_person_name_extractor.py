import os
import argparse
import json
import spacy
from config import config as cfg

class BanglaPersorNer(object):
    """Class for Bangla person name extraction.
    """
    def __init__(self) -> None:
        """Initialize BanglaPersorNer class.
        """
        # Load the model
        self._model = spacy.load(cfg.MODEL_DIR)

    def get_doc(self, text: str) -> object:
        """This function performs model inference on given text and returns space Doc object.

        Args:
            text (str): text to be inferenced on

        Returns:
            object: Spacy.tokens.Doc object
        """
        # get prediction on text
        doc = self._model(text)
        # return Doc object
        return doc

    def extract_person_name(self, text: str) -> dict:
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
        # get prediction on text
        doc = self.get_doc(text)
        
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

def main() -> None:
    """This function is called if the script is called directly. It takes user input
    from terminal and prints output to either terminal or file.
    """
    # create argument parser
    parser = argparse.ArgumentParser(description='Predict bangla names in given text.')
    # add argument for input to argrument parser
    parser.add_argument(
        '-i', '--input', required=True, type=str, help='input string - bangla text to predict names.')
    # add argument for output to argrument parser
    parser.add_argument(
        '-o', '--output', required=False, type=str, help='output json path - path of a json file to write the output.')
    # parse arguments
    args = parser.parse_args()
    # create an object of BanglaPersorNer
    bp_ner = BanglaPersorNer()
    # extract names from argument input
    res = bp_ner.extract_person_name(args.input)
    # if there is output argument then write the output to 
    if args.output:
        # create directories if does not exists
        os.makedirs(os.path.dirname(args.output)[0], exist_ok=True)
        # open and write to file
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(json.dumps(res, ensure_ascii=False, indent=4))
        print(f"Output saved to file : {args.output}")
    # print to terminal instead
    else:
        print(res)

if __name__ == "__main__":
    # call main function
    main()