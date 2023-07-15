import gradio as gr
from utils.tokenizer import BasicTokenizer
from bangla_person_name_extractor import BanglaPersorNer

# create an object of BanglaPersorNer
bp_ner = BanglaPersorNer()
# create tokenizer object
tokenizer = BasicTokenizer()

def handler(text: str) -> list:
    """This function extracts person name from given text and
    prepares output to be shown on gradio interface.

    Args:
        text (str): Input text from gradio input field

    Returns:
        list: list of tuples. Each tuple is token of text and it's entity (Person or None)
    """
    # get doc object of text from the model
    doc = bp_ner.get_doc(text)
    # initialize list of tokens
    ner_tokens = []
    # iterate over each token of doc
    for token in doc:
        # if token has an entity type then use it, otherwise set None
        entity = token.ent_type_ if token.ent_type_ else None
        # add the tuple (token_text, token_entity) to token list
        ner_tokens.extend([(token.text, entity)])
    # return the tokens
    return ner_tokens

# Description to be shown at top of gradio interface
description = "This project lets you extract bangla person name from the provided text. To extract \
    names type (or, copy paste) your text in the text box below at left side and press submit button. \
    On the right side text box you will see your text with person name highlighted."
# Articale to be shown after input output field of gradio interface
article = "The model used in this project is fine-tuned from \
    [BERT model](https://huggingface.co/csebuetnlp/banglabert) using \
    [Rifat1493/Bengali-NER/annotated data](https://github.com/Rifat1493/Bengali-NER/tree/master/annotated%20data) and \
    [banglakit/bengali-ner-data](https://raw.githubusercontent.com/banglakit/bengali-ner-data/master/main.jsonl) data."
# color map for entities
color_map = {"PER": "green"}
# input field for gradio interface, a gradio textbox in our case
inputs = gr.Textbox(placeholder="Enter sentence here...")
# output field for gradio interface, gradio HighlightedText in our case
# as we want to show extracted person name highlighted in the output.
output = gr.HighlightedText(
        color_map=color_map,
        combine_adjacent=True,
        adjacent_separator=" "
    )
# a list of input samples to be shown on gradio interface
examples = [
    "ডা. মো. শরিফুল ইসলাম, শহীদ সোহরাওয়ার্দী মেডিকেল, কলেজ ও হাসপাতাল।",
    "মো. আলমের কাছ থেকে ১৫ লাখ টাকা আদায় করা হয়।",
    "এতিমখানার কর্মকর্তা-শিক্ষার্থীরা কমিটি ও চুক্তির বিরুদ্ধে আন্দোলন শুরু করে।",
]
# initialize gradio interface.
app = gr.Interface(
    fn=handler,
    inputs=inputs,
    outputs=output,
    examples=examples,
    title="Bangla Person Name Extractor",
    description=description,
    article=article,
    allow_flagging="never",
    )

if __name__ == "__main__":
    # launch gradio app.
    app.launch()