from typing import Literal, Optional
from typing import List
import requests
import os

from .streaming import StreamHandler, parse_stream

from confidentialmindserver.config_manager import ConfigManager

LOCAL_DEV = False
if os.environ.get("CONFIDENTIAL_MIND_LOCAL_DEV") == "True":
    LOCAL_DEV = True

LOCAL_MIRRORD_DEV = False
if os.environ.get("CONFIDENTIAL_MIND_LOCAL_MIRRORD_DEV") == "True":
    LOCAL_MIRRORD_DEV = True


class ChatMessage:
    """
    Represents a chat message in the context of an AI assistant.

    Attributes:
        role (Literal["user", "assistant", "system"]): The role associated with the message.
            Typically, the system message is optional and the order must be: system, user, assistant, user, assistant, ...
        content (str): The text content of the message.
    """

    def __init__(self, role: Literal["user", "assistant", "system"], content: str):
        self.role = role
        self.content = content


class LLMAPIHandler:
    """
    Handles API interactions for a language model.

    Attributes:
        config_id (str): The identifier of the LLM connector to use.
        embedding_id (Optional[str]): The identifier of the embedding connector, if any.

    Methods:
        handle_query: Processes and sends chat messages to an LLM endpoint for completion.
    """

    def __init__(self, config_id: str, embedding_id=None):
        self.config_id = config_id
        self.embedding_id = embedding_id

    # TODO: define the handle_query method to use at initialization
    def handle_query(
        self,
        messages: list[ChatMessage],
        stream_handler: StreamHandler,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = True,
    ):
        """
        Handles a query by sending it to the LLM service and processing the response.

        Args:
            messages (list[ChatMessage]): List of chat messages representing the conversation.
            stream_handler (StreamHandler): The handler for streaming responses from the LLM.
            temperature (float, optional): Sampling temperature for text generation. Defaults to 0.7.
            max_tokens (Optional[int], optional): Maximum number of tokens in the generated response. Defaults to None.
            stream (bool, optional): Whether to enable streaming mode for receiving results. Defaults to True.

        Returns:
            str: The LLM's response as a string.
        """

        print("CALLING HANDLE QUERY")
        configManager = ConfigManager()
        url_base = configManager.getUrlForConnector(self.config_id)

        if LOCAL_MIRRORD_DEV:
            url_base = "http://host.minikube.internal:8083"
        elif LOCAL_DEV:
            url_base = "http://localhost:8083"

        url = url_base + "/v1/chat/completions"

        url_base_embedding = configManager.getUrlForConnector(self.embedding_id)
        # TODO Now doesn't work with local setup without adding
        # or LOCAL_DEV to this rule
        if url_base_embedding is not None:
            # create url
            if LOCAL_DEV:
                url_base_embedding = "http://localhost:8085"
            url_embeddings = url_base_embedding + "/query"
            # body: query: str, top_k: int optional
            # fetch
            # TODO make function async
            results = requests.post(
                url_embeddings, json={"query": messages[-1].content}
            )
            # parse results
            # TODO read this correctly
            # print(results.json())
            results_to_loop = results.json()["results"]["results"]
            # Add results to last message
            if len(results_to_loop) > 0:
                string_to_add = "\n\nHere are references which to use when answering to the question:\n"
                for result in results_to_loop:
                    print(result)
                    array_str = [str(x) for x in result["sql_metadata"]["pages"]]
                    string_to_add += (
                        "source file: "
                        + result["sql_metadata"]["filename"]
                        + " . source pages: "
                        + ".".join(array_str)
                        + " result score: "
                        + str(result["score"])
                        + "\n\n"
                    )
                    string_to_add += result["sql_metadata"]["text"] + "\n\n"
                string_to_add += "\n\n  Include the source file, source page and result score in your answer."

                messages[-1].content += string_to_add
        else:
            print("No config for embedding service")

        response = get_response(
            messages, url, temperature=temperature, max_tokens=max_tokens, stream=stream
        )
        if stream:
            answer = parse_stream(response, stream_handler)
        else:
            # TODO: should we return the whole response or just the answer?
            answer = response.json()["choices"][0]["message"]["content"]
            stream_handler.on_llm_new_token(answer)
        return answer

    def handle_embedding(
        self,
        texts: list[str],
    ):
        print("CALLING HANDLE EMBEDDING")
        configManager = ConfigManager()
        url_base = configManager.getUrlForConnector(self.config_id)

        if LOCAL_MIRRORD_DEV:
            url_base = "http://host.minikube.internal:8083"
        elif LOCAL_DEV:
            url_base = "http://localhost:8083"

        if url_base is None:
            print("No config for embedding service")

        url = url_base + "/v1/embeddings"

        return get_embeddings(texts, url)


def get_response(
    messages: list[ChatMessage],
    url: str,
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    stream: bool = True,
):
    """
    Sends a request to the LLM API and returns the response.

    Args:
        messages (list[ChatMessage]): List of chat messages representing the conversation.
        url (str): The URL endpoint for the LLM service.
        temperature (float, optional): Sampling temperature for text generation. Defaults to 0.7.
        max_tokens (Optional[int], optional): Maximum number of tokens in the generated response. Defaults to None.
        stream (bool, optional): Whether to enable streaming mode for receiving results. Defaults to True.

    Returns:
        requests.Response: The raw response object from the API call.
    """
    parsed_messages = [obj.__dict__ for obj in messages]
    jsonBody = {
        "messages": parsed_messages,
        "temperature": temperature,
        "stream": stream,
        "model": "cm-llm",  # Hardcoded model for vllm; ignored by our proxy
    }
    if max_tokens:
        jsonBody["max_tokens"] = max_tokens
    res = requests.post(
        url,
        json=jsonBody,
        stream=stream,
        headers={"Content-Type": "application/json"},
    )
    return res


# This is copied from apis/rag-service/services/embeddings.py
def get_embeddings(texts: List[str], url: str) -> List[List[float]]:
    """
    Embed texts using Connected Embedding service.

    Args:
        texts: The list of texts to embed.

    Returns:
        A list of embeddings, each of which is a list of floats.

    Raises:
        Exception: If the HTTP call fails.
    """
    if url is None:
        raise Exception("No embedding connector found")
    print(f"Calling Embedding service with {url}")
    # Call the Connected Embedding service
    try:
        response = requests.post(
            url,
            json={
                "input": texts,
            },
        )
        data = response.json()
        embeddings = [item["embedding"] for item in data["data"]]
        return embeddings
    except Exception as e:
        print(e)
        raise Exception(f"Error calling Embedding service: {e}")
