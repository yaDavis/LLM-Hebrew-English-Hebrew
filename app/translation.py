from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# hebrew and english in language codes
Hebrew = "heb_Hebr"
English = "eng_Latn"

# Setup translation model and tokenizer
translation_model_name = "facebook/nllb-200-distilled-600M"
translation_tokenizer = AutoTokenizer.from_pretrained(translation_model_name)
translation_model = AutoModelForSeq2SeqLM.from_pretrained(translation_model_name)

# Function to translate text from source language to target language 
# returns translated text in str format
#The entire process: Text → Tokens → Model Processing → Output Tokens → Translated Text.

def translate(text: str, src_language: str, tgt_language : str) -> str:

    #Tokenize text
    inputs = translation_tokenizer(text, return_tensors = "pt",truncation = True)

    #Translate tokens 
    # The forced_bos_token_id parameter tells the model which language to translate into by forcing the target language token 
    #  at the beginning of output.
    translated_tokens = translation_model.generate(
        **inputs,
        forced_bos_token_id = translation_tokenizer.convert_tokens_to_ids(tgt_language)

    )
    #Decode tokens back to text
    return translation_tokenizer.decode(translated_tokens[0],skip_special_tokens=True)




