from dotenv import load_dotenv
import openai
import os
import time
from typing import Callable

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(start_time)
        result = func(*args, **kwargs)
        end_time = time.time()
        print(end_time)
        print(f"Execution time of {func.__name__}: {end_time - start_time} seconds")
        return result
    return wrapper



load_dotenv()

openai.api_key = os.environ.get('OPENAI_API_KEY')

# text-davinci-003

def codex(ask):
    
    response = openai.Completion.create(
    model="text-davinci-001",
    prompt="""
1. Get a reputable news API website
2. Make a request to get the latest news stories
3. Create a flask application to display the news stories on the front HTML template
""",
    temperature=0,
    max_tokens=1500,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
    #text = response['choices'][0]['text']
    print(response)
    
@measure_time
def chat_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
        )
    answer = response['choices'][0]['message']['content']
    print(answer)



#chat_gpt("Can you tell me about chatgpt ?")
codex("Ask the user for their name and say 'Hello'")
