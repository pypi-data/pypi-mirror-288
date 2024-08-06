# Streamlit code partially from langchain-ai streamlit-agent repo:
# https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_streaming.py
# SHA: 6125bddf43f643b7ffd6d41eb463e2524f6d47a0
# License: Apache 2.0

import json
from requests.models import ChunkedEncodingError, Response
from sseclient import SSEClient


# TODO: this doesn't work with completion responses (non-streaming)
def parse_stream(stream: Response, token_callback: callable = None) -> str:
    """
    Parses a streaming response from an AI model. The stream must follow the openAI streaming output format.

    Args:
        stream (requests.Response): The raw HTTP response object containing the streamed data.
        token_callback (callable): A callback function to handle each new token received.

    Returns:
        str: Accumulated text from all received tokens.

    Note: This function is designed for handling streaming responses and may not work properly with non-streaming completions.
    """
    try:
        bot_answer = ""
        print("Bot: ", flush=True)

        client = SSEClient(stream)
        for event in client.events():
            print(event.data)
            if event.data == "[DONE]":
                break
            data = event.data
            try:
                new_token = json.loads(data)["choices"][0]["delta"]["content"] or ""
                if token_callback:
                    token_callback(new_token)
                bot_answer += new_token
            except (IndexError, TypeError, json.JSONDecodeError, KeyError) as error:
                print(f"{type(error).__name__}: {error}")
                continue
        print("\n", flush=True)
        return bot_answer
    except ChunkedEncodingError as error:
        print(f"ChunkedEncodingError: {error}")
        return bot_answer
