# Streamlit code partially from langchain-ai streamlit-agent repo:
# https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/basic_streaming.py
# SHA: 6125bddf43f643b7ffd6d41eb463e2524f6d47a0
# License: Apache 2.0

from confidentialmind_app_helpers.llm_api_helpers import LLMAPIHandler, ChatMessage

import streamlit as st


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


def clear_chat():
    """Clear the chat history by resetting the session state's messages list."""
    st.session_state.messages = [
        ChatMessage(role="assistant", content="How can I help you?")
    ]


def chat_ui(
    llm_config_id: str,
    pre_hook=None,
    post_hook=None,
    system_prompt="You are a helpful assistant.",
):
    """Display user interface and handle logic for a multi-turn conversation with an LLM.

    Parameters:
         llm_config_id (str): The ID of the Large Language Model configuration.
         pre_hook (function, optional): A function to be called before UI rendering. Defaults to None.
         post_hook (function, optional): A function to be called after UI rendering. Defaults to None.
         system_prompt (str, optional): The initial prompt for the chatbot's context. Defaults to a helpful assistant.

     Description:
         This function initializes and manages the Streamlit UI components for interacting with an LLM-powered chatbot.
         It includes setting up the session state for messages and system prompt, rendering past messages,
         processing user input, calling the LLM API handler, handling stream responses, and providing hooks
         for pre- and post-rendering customizations.

     Usage Example:
         >>> LLM_CONFIG_ID = "llm"
         >>> chat_ui(LLM_CONFIG_ID, system_prompt=tool.config.prompt)
    """
    llm_api_handler = LLMAPIHandler(llm_config_id)
    if pre_hook:
        pre_hook()

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            ChatMessage(role="assistant", content="How can I help you?")
        ]

    if "system_prompt" not in st.session_state:
        st.session_state["system_prompt"] = system_prompt

    for msg in st.session_state.messages:
        st.chat_message(msg.role).write(msg.content)

    if prompt := st.chat_input():
        st.session_state.messages.append(ChatMessage(role="user", content=prompt))
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            stream_handler = StreamHandler(st.empty())
            history = [obj for obj in st.session_state.messages[1:]]
            history.insert(
                0, ChatMessage(role="system", content=st.session_state["system_prompt"])
            )
            temperature = st.session_state.get("temperature", 0.7)
            response = chat_query(stream_handler, llm_api_handler, history, temperature)
            st.session_state.messages.append(
                ChatMessage(role="assistant", content=response)
            )

    if "messages" in st.session_state and len(st.session_state.messages) > 1:
        st.button("Clear chat", on_click=clear_chat)

    if post_hook:
        post_hook()


def chat_query(
    stream_handler: StreamHandler,
    llm_api_handler: LLMAPIHandler,
    messages: list[ChatMessage],
    temperature=0.7,
):
    """
    Query the LLM to generate a response based on the provided conversation history.

    Parameters:
        stream_handler (StreamHandler): A handler for processing streamed responses.
        llm_api_handler (LLMAPIHandler): An API handler instance configured with an LLM model ID.
        messages (list[ChatMessage]): The conversation history including system, user and assistant messages.
        temperature (float, optional): Sampling temperature to control creativity of the response. Defaults to 0.7.

    Returns:
        str: The generated bot answer as a text string.

    Description:
        This function uses the provided LLM API handler to generate an assistant's response based on
        the conversation history. It supports streaming responses through the stream_handler for real-time updates.

    Usage Example:
        >>> chat_query(my_stream_handler, my_llm_api_handler, my_messages)
        # Generates a bot answer using the given StreamHandler and LLMAPIHandler with specified messages.
    """
    bot_answer = llm_api_handler.handle_query(
        messages, stream_handler.on_llm_new_token, temperature, stream=True
    )
    return bot_answer


def text_embedding(
    llm_api_handler: LLMAPIHandler,
    texts: list[str],
):
    return llm_api_handler.handle_embedding(texts)
