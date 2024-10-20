import asyncio
from openai import OpenAI
client = OpenAI( api_key = "" )


QUEUES = {
    "positive_queue": asyncio.Queue(), 
    "negative_queue": asyncio.Queue(), 
    "neutral_queue": asyncio.Queue()
}

async def askGPT(prompt):
    '''
        Use OpenAI Gpt API to generate requried text
    '''
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content  # Get the generated text
    except Exception as e:
        return f'Error: {str(e)}'

