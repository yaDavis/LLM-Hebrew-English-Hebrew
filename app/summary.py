from ollama import Client
from app.translation import translate , English, Hebrew

#localhost defualt port 11434
client = Client(host ="http://localhost:11434")

system_prompt = "You are a proffessional text summarizer. Summarize as simply as possible and by 5 conise bullet points." \
"each bullet point starts with - and ends with a new line"
"REMEMBER ONLY 5 BULLET POINTS NO MORE NO LESS"

#I call it ph3mini and not phi3:mini-4k-instruct because i have created a new custom model via gguf file of phi3:mini... in ollama
#and now if i want to use that model i have to use the custom name i called phi3mini
model_name = "phi3mini"


# Function to summarize text via ollama client and model , method that i built before the bonus
def summarize(prompt: str, options: dict):
    response = client.chat(
        model = model_name,
        options = options,
        messages = [
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : prompt},
        ],
        stream = True,
        )   

    #Yield each chunk of the response as it is generated
    for chunk in response:
        if "content" in chunk["message"]:
            yield chunk["message"]["content"]




def summarize_and_translate(text: str, options: dict):
    
    #buffer of bulletpoints
    buffer = ""
    #summarize in 5 bullet points
    for chunk in summarize(text,options):
        buffer += chunk

        #while we are not done with the bullet point
        while "\n" in buffer:
            line_end = buffer.index("\n") + 1 #include the \n
            line = buffer[:line_end].strip() #this is the bullet point
            buffer = buffer[line_end:]  #continue with the next bullet point
            if line: #if we have a bullet point
                yield translate(line,English,Hebrew) #yield the translated bullet point from english to hebrew


