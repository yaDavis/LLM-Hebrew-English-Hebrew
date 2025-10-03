Hello,

***Summary***
    Real time hebrew text summarization with streaming responeses by bullets.
    Uses phi3:mini-4k-instruct for summirzation and facebook/nllb-200-distilled-600M for translation
    First it gets the prompt and options to play with temperatus and other variables , then it translates the text to english and creates a Summary
    in 5 bullet points , after each bullet that is generated it is being translated back to hebrew and stream back to the user.
    *** Hebrew -> English -> Hebrew pipeline

uses fastAPI endpoint with /summary for the summary in hebrew and /summary_english for only english 


example for json input - 

{
"prompt": "Hebrew text to summarize",
"temperature": 0.7,
"top_k": 40,
"top_p": 0.7,
"max_tokens": 500
}


***Requierments***
Need to have the ollama localy on your computer and setup the phi3:mini-4k-instruct locally on the ollama
FastAPI
HuggingFace Transformers
Streaming Response
Pydantic



Made by Davis Yakubenko