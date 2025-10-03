from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import asyncio

#My methods from summary and translation files
from app.summary import summarize as summarize_llm
from app.summary import summarize_and_translate
from app.translation import translate, Hebrew, English



#Optional sets value to default unless user inputs
class chatRequest(BaseModel):
    prompt: str
    temperature: Optional[float] = 0.7
    top_k: Optional[int] = 40
    top_p: Optional[float] = 0.7
    max_tokens: Optional[int] = 500






# Options for the LLM model - Temperature is for the creativty of the model and randomemness
# top_k limits how many of the top next word candidates the model consider - lower top k more predictable safer , higher more variety and riskier
# top_p - chooses the smallest set of tokens with probalities the add up to p - if 0.9 then it will consider top tokens that make up to 90% probality , higher p more variety and creative and risky
# num_predict - is how many tokens to predict - max length of response - bigger number longer response can be .

def build_options(req: chatRequest):
    return{
        "temperature" : req.temperature,
        "top_k" : req.top_k,
        "top_p" : req.top_p,
        "num_predict": req.max_tokens,
    }


#     ********** FastAPI app and endpoints **********

app = FastAPI(title = "Testing LLM")

# Root endpoint to check if api is running

@app.get("/")
async def root():
    return {"message": "API is running"}


# Endpoint for summarize - takes hebrew text translate it into english then while it summarize by bulletpoints it translates each bullet point in real time
# to hebrew and returns the summariztion on hebrew in real time
@app.post("/summarize")
async def summarize_endpoint(request: chatRequest):
    #take hebrew text and temperature from request json
    hebrew_text = request.prompt
    #Build options dictionary for the model
    options = build_options(request)
    
    #Translate hebrew text to english
    english_text = translate(hebrew_text,Hebrew,English)

    async def event_stream():
        
        #Summarize and translating live from english to hebrew by each bullets
        for bullet in summarize_and_translate(english_text,options):
            print(bullet)
            yield bullet + "\n"
            
    #Streaming response as is generated via http
    return StreamingResponse(event_stream(),media_type = "text/plain")


@app.post("/summarize_english")
async def summarize_english_endpoint(request: chatRequest):
    hebrew_text = request.prompt
    options = build_options(request)

    english_text = translate(hebrew_text,Hebrew,English)

    async def event_stream():
        for chunk in summarize_llm(english_text,options):
            print(chunk,end="",flush=True)
            yield chunk 

    return StreamingResponse(event_stream(),media_type="text/plain")


