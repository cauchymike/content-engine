import openai
from settings import OPENAI_API_KEY
import re

def initialize_chatbot(user_input: str) -> str:
    """
    Initialize and run a chatbot using OpenAI's GPT-3.

    Args:
        api_key (str): Your OpenAI API key.
        user_input (str): The user's input prompt.

    Returns:
        str: The chatbot's response.
    """
    openai.api_key = OPENAI_API_KEY

    def chat_with_bot(prompt: str) -> str:
        """
        Send a user prompt to the chatbot and receive a response with extracted item ID.

        Args:
            prompt (str): The user's input prompt.

        Returns:
            tuple (str, str): The chatbot's response and extracted item ID (if found).
        """
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()
        

        # Use regular expression to extract item ID from the bot's response
        item_id = re.search(r'\b\d+\b', bot_response)
        
        if item_id:
            
            return item_id.group()
        else:
            return bot_response

    prompt = f"You: {user_input}\nBot:"
    bot_response = chat_with_bot(prompt)
    return bot_response

def chat_with_bot(prompt: str) -> (str, str):
    """
    Send a user prompt to the chatbot and receive a response with extracted item ID.

    Args:
        prompt (str): The user's input prompt.

    Returns:
        tuple (str, str): The chatbot's response and extracted item ID (if found).
    """
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50
    )
    bot_response = response.choices[0].text.strip()
    print(bot_response)

    # Use regular expression to extract item ID
    item_id = re.search(r'\b\d+\b', bot_response)
    
    if item_id:
        return bot_response, item_id.group()
    else:
        return bot_response, None




