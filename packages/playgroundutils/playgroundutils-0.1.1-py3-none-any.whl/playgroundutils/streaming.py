# Streamlit code partially from langchain-ai streamlit-agent repo:
# https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_streaming.py
# SHA: 6125bddf43f643b7ffd6d41eb463e2524f6d47a0
# License: Apache 2.0

import json
from requests.models import ChunkedEncodingError, Response
import sseclient


# TODO: This is not good if we get a single block of text instead of a stream.
class StreamHandler:
    """
    A handler for displaying streaming responses from an AI model.

    Attributes:
        container (Any): The UI container to update with new tokens.
        text (str): Accumulated text from streamed tokens.

    Methods:
        on_llm_new_token: Appends a token to the accumulated text and updates the UI container.
    """

    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str) -> None:
        """
        Callback for receiving new tokens from an LLM.

        Args:
            token (str): The new token received.

        Updates the accumulated text and refreshes the UI container with the updated content.
        """
        self.text += token
        self.container.markdown(self.text)


# TODO: this doesn't work with completion responses (non-streaming)
def parse_stream(stream: Response, stream_handler: StreamHandler):
    """
    Parses a streaming response from an AI model. The stream must follow the openAI streaming output format.

    Args:
        stream (requests.Response): The raw HTTP response object containing the streamed data.
        stream_handler (StreamHandler): An instance of StreamHandler to display streamed text in real time.

    Returns:
        str: Accumulated text from all received tokens.

    Note: This function is designed for handling streaming responses and may not work properly with non-streaming completions.
    """
    try:
        bot_answer = ""
        print("Bot: ", flush=True)

        client = sseclient.SSEClient(stream)
        for event in client.events():
            print(event.data)
            if event.data == "[DONE]":
                break
            data = event.data
            try:
                new_token = json.loads(data)["choices"][0]["delta"]["content"] or ""
                stream_handler.on_llm_new_token(new_token)
                bot_answer += new_token
            except (IndexError, TypeError, json.JSONDecodeError, KeyError) as error:
                print(f"{type(error).__name__}: {error}")
                continue
        print("\n", flush=True)
        return bot_answer
    except ChunkedEncodingError as error:
        print(f"ChunkedEncodingError: {error}")
        return bot_answer
