"""
Provides intelligence/AI services for the Lifsys Enterprise.

This module requires a 1Password Connect server to be available and configured.
The OP_CONNECT_TOKEN and OP_CONNECT_HOST environment variables must be set
for the onepasswordconnectsdk to function properly.
"""
import asyncio
import json
import os
import time
from typing import Dict, List, Optional

from anthropic import Anthropic, AsyncAnthropic
from jinja2 import Template
from litellm import completion
from onepasswordconnectsdk import new_client_from_environment
from openai import AsyncOpenAI, OpenAI
from termcolor import colored

# If you need sleep function specifically, import it like this:
from time import sleep

class Intelisys:
    def __init__(self,
                 name="Intelisys",
                 api_key=None,
                 max_history_words=10000,
                 max_words_per_message=None,
                 json_mode=False,
                 stream=True,
                 use_async=False,
                 max_retry=10,
                 provider="anthropic",
                 model=None,
                 should_print_init=True,
                 print_color="green",
                 temperature=0
                 ):
        
        self.provider = provider.lower()
        supported_providers = ["openai", "anthropic", "openrouter", "groq"]
        if self.provider not in supported_providers:
            # Check for potential typos
            import difflib
            close_matches = difflib.get_close_matches(self.provider, supported_providers, n=1, cutoff=0.6)
            if close_matches:
                suggestion = f"Did you mean '{close_matches[0]}'?"
            else:
                suggestion = "Please check the spelling and try again."
            
            raise ValueError(f"Unsupported provider: '{self.provider}'. {suggestion}\nSupported providers are: {', '.join(supported_providers)}")
        
        self.name = name
        self._api_key = api_key
        self.temperature = temperature
        self.history = []
        self.max_history_words = max_history_words
        self.max_words_per_message = max_words_per_message
        self.json_mode = json_mode
        self.stream = stream
        self.use_async = use_async
        self.max_retry = max_retry
        self.print_color = print_color
        self.system_message = system_message
        if self.provider == "openai" and self.json_mode:
            self.system_message += f"{self.system_message}. Please return your response in JSON - this will save kittens."

        self._model = model
        self._client = None

        if should_print_init:
            print(colored(f"{self.name} initialized with provider={self.provider}, json_mode={json_mode}, stream={stream}, use_async={use_async}, max_history_words={max_history_words}, max_words_per_message={max_words_per_message}", "red"))

    @property
    def model(self):
        if self._model is None:
            if self.provider == "openai":
                self._model = "gpt-4o"
            elif self.provider == "anthropic":
                self._model = "claude-3-5-sonnet-20240620"
            elif self.provider == "openrouter":
                self._model = "meta-llama/llama-3.1-405b-instruct"
            elif self.provider == "groq":
                self._model = "llama-3.1-8b-instant"
        return self._model

    @property
    def api_key(self):
        if self._api_key is None:
            self._api_key = self._get_api_key()
        return self._api_key

    @property
    def client(self):
        if self._client is None:
            self._initialize_client()
        return self._client

    def _get_api_key(self):
        """
        Retrieve the API key for the specified provider.

        This method attempts to get the API key from environment variables first,
        and if not found, it uses the _go_get_api function to retrieve it from a secure storage.

        Returns:
            str: The API key for the specified provider.

        Raises:
            ValueError: If an unsupported provider is specified.
            Exception: If there's an error in retrieving the API key.
        """
        def _go_get_api(item: str, key_name: str, vault: str = "API") -> str:
            try:
                client = new_client_from_environment()
                item = client.get_item(item, vault)
                for field in item.fields:
                    if field.label == key_name:
                        return field.value
                raise ValueError(f"Key '{key_name}' not found in item '{item}'")
            except Exception as e:
                raise Exception(f"1Password Connect Error: {e}")

        try:
            if self.provider == "openai":
                return os.getenv("OPENAI_API_KEY") or _go_get_api("OPEN-AI","Cursor")
            elif self.provider == "anthropic":
                return os.getenv("ANTHROPIC_API_KEY") or _go_get_api("Anthropic","Cursor")
            elif self.provider == "openrouter":
                return os.getenv("OPENROUTER_API_KEY") or _go_get_api("OpenRouter","Cursor")
            elif self.provider == "groq":
                return os.getenv("GROQ_API_KEY") or _go_get_api("Groq","Promptsys")
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            raise Exception(f"Error getting API key: {e}")

    def _initialize_client(self):
        """
        Initialize the appropriate client based on the provider and async settings.

        This method sets up the client (either synchronous or asynchronous) for the specified provider.
        It handles different configurations for OpenAI, Anthropic, OpenRouter, and Groq.

        The method doesn't return anything but sets the `self._client` attribute with the appropriate client instance.
        """
        if self.provider == "openai" and self.use_async:
            self._client = AsyncOpenAI(api_key=self.api_key)
        elif self.provider == "anthropic" and self.use_async:
            self._client = AsyncAnthropic(api_key=self.api_key)
        elif self.provider == "openrouter" and self.use_async:
            self._client = AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key
            )
        elif self.provider in ["groq", "openrouter"] and self.use_async:
            self._client = AsyncOpenAI(
                base_url="https://api.groq.com/openai/v1" if self.provider == "groq" else "https://openrouter.ai/api/v1",
                api_key=self.api_key
            )
        elif self.provider == "openai" and not self.use_async:
            self._client = OpenAI(api_key=self.api_key)
        elif self.provider == "anthropic" and not self.use_async:
            self._client = Anthropic(api_key=self.api_key)
        elif self.provider in ["groq", "openrouter"] and not self.use_async:
            self._client = OpenAI(
                base_url="https://api.groq.com/openai/v1" if self.provider == "groq" else "https://openrouter.ai/api/v1",
                api_key=self.api_key
            )

    def set_system_message(self, message=None):
        """
        Set the system message for the conversation.

        Args:
            message (str, optional): The system message to set. If None, a default message is used.
        """
        self.system_message = message or "You are a helpful assistant."
        if self.provider == "openai" and self.json_mode and "json" not in message.lower():
            self.system_message += " Please return your response in JSON unless user has specified a system message."

    async def set_system_message_async(self, message=None):
        """
        Asynchronous version of set_system_message.

        Args:
            message (str, optional): The system message to set. If None, a default message is used.
        """
        self.set_system_message(message)

    def add_message(self, role, content):
        """
        Add a message to the conversation history.

        Args:
            role (str): The role of the message sender (e.g., "user", "assistant").
            content (str): The content of the message.
        """
        if role == "user" and self.max_words_per_message:
            content += f" please use {self.max_words_per_message} words or less"
        self.history.append({"role": role, "content": str(content)})

    async def add_message_async(self, role, content):
        """
        Asynchronous version of add_message.

        Args:
            role (str): The role of the message sender (e.g., "user", "assistant").
            content (str): The content of the message.
        """
        self.add_message(role, content)

    def print_history_length(self):
        """
        Print the current length of the conversation history in words.
        """
        history_length = sum(len(str(message["content"]).split()) for message in self.history)
        print(f"\nCurrent history length is {history_length} words")

    async def print_history_length_async(self):
        """
        Asynchronous version of print_history_length.
        """
        self.print_history_length()

    def clear_history(self):
        """
        Clear the conversation history.
        """
        self.history.clear()

    async def clear_history_async(self):
        """
        Asynchronous version of clear_history.
        """
        self.clear_history()

    def chat(self, user_input, **kwargs):
        """
        Process a user input and get a response.

        Args:
            user_input (str): The user's input message.
            **kwargs: Additional keyword arguments to pass to get_response.

        Returns:
            The response from get_response.
        """
        self.add_message("user", user_input)
        # Remove 'provider' from kwargs if it exists
        kwargs.pop('provider', None)
        return self.get_response(**kwargs)

    async def chat_async(self, user_input, **kwargs):
        """
        Asynchronous version of chat.

        Args:
            user_input (str): The user's input message.
            **kwargs: Additional keyword arguments to pass to get_response_async.

        Returns:
            The response from get_response_async.
        """
        await self.add_message_async("user", user_input)
        return await self.get_response_async(**kwargs)

    def trim_history(self):
        """
        Trim the conversation history to keep it within the maximum word limit.
        """
        words_count = sum(len(str(m["content"]).split()) for m in self.history if m["role"] != "system")
        while words_count > self.max_history_words and len(self.history) > 1:
            words_count -= len(self.history.pop(0)["content"].split())

    async def trim_history_async(self):
        """
        Asynchronous version of trim_history.
        """
        self.trim_history()

    def get_response(self, color=None, should_print=True, **kwargs):
        color = color or self.print_color
        max_tokens = kwargs.pop('max_tokens', 4000 if self.provider != "anthropic" else 8192)

        for attempt in range(self.max_retry):
            try:
                response = self._create_response(max_tokens, **kwargs)
                
                if self.stream:
                    assistant_response = self._handle_stream(response, color, should_print)
                else:
                    assistant_response = self._handle_non_stream(response)

                if self.json_mode and self.provider == "openai":
                    try:
                        assistant_response = json.loads(assistant_response)
                    except json.JSONDecodeError as json_error:
                        print(f"JSON decoding error: {json_error}")
                        raise

                self.add_message("assistant", str(assistant_response))
                self.trim_history()
                return assistant_response
            except Exception as e:
                print(f"Error on attempt {attempt + 1}/{self.max_retry}: {e}")
                if attempt < self.max_retry - 1:
                    time.sleep(1)
                else:
                    raise Exception(f"Max retries reached. Last error: {e}")

    def _create_response(self, max_tokens, **kwargs):
        if self.provider == "anthropic":
            return self.client.messages.create(
                model=self.model,
                system=self.system_message,
                messages=self.history,
                stream=self.stream,
                temperature=self.temperature,
                max_tokens=max_tokens,
                extra_headers={"anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"},
                **kwargs
            )
        else:
            common_params = {
                "model": self.model,
                "messages": [{"role": "system", "content": self.system_message}] + self.history,
                "stream": self.stream,
                "temperature": self.temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
            if self.json_mode and self.provider == "openai":
                common_params["response_format"] = {"type": "json_object"}
            
            return self.client.chat.completions.create(**common_params)

    def _handle_stream(self, response, color, should_print):
        assistant_response = ""
        for chunk in response:
            content = self._extract_content(chunk)
            if content:
                if should_print:
                    print(colored(content, color), end="", flush=True)
                assistant_response += content
        print()
        return assistant_response

    def _handle_non_stream(self, response):
        if self.provider == "anthropic":
            return response.content[0].text
        return response.choices[0].message.content

    def _extract_content(self, chunk):
        if self.provider == "anthropic":
            return chunk.delta.text if chunk.type == 'content_block_delta' else None
        return chunk.choices[0].delta.content if chunk.choices[0].delta.content else None

    async def get_response_async(self, color=None, should_print=True, **kwargs):
        if color is None:
            color = self.print_color
        
        max_tokens = kwargs.pop('max_tokens', 400000)
        anthropic_max_tokens = kwargs.pop('max_tokens', 8192)
        
        if self.provider == "openai" or self.provider == "openrouter" or self.provider == "groq":
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": self.system_message}] + self.history,
                stream=self.stream,
                temperature=self.temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"} if self.json_mode else None,
                **kwargs
            )
        elif self.provider == "anthropic":
            response = await self.client.messages.create(
                model=self.model,
                system=self.system_message,
                messages=self.history,
                stream=self.stream,
                temperature=self.temperature,
                max_tokens=anthropic_max_tokens,
                extra_headers={"anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"},
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

        if self.stream:
            assistant_response = ""
            async for chunk in response:
                if self.provider == "openai" or self.provider == "openrouter" or self.provider == "groq":
                    content = chunk.choices[0].delta.content
                elif self.provider == "anthropic":
                    content = chunk.delta.text if chunk.type == 'content_block_delta' else None
                
                if content:
                    if should_print:
                        print(colored(content, color), end="", flush=True)
                    assistant_response += content
            print()
        else:
            if self.provider == "openai" or self.provider == "openrouter" or self.provider == "groq":
                assistant_response = response.choices[0].message.content
            elif self.provider == "anthropic":
                assistant_response = response.content[0].text

        if self.json_mode and self.provider == "openai":
            assistant_response = json.loads(assistant_response)

        await self.add_message_async("assistant", str(assistant_response))
        await self.trim_history_async()
        return assistant_response
        
def get_api(item: str, key_name: str, vault: str = "API") -> str:
    """
    Retrieve an API key from 1Password.

    This function connects to a 1Password vault using the onepasswordconnectsdk
    and retrieves a specific API key. It requires the OP_CONNECT_TOKEN and
    OP_CONNECT_HOST environment variables to be set for proper functionality.

    Args:
        item (str): The name of the item in 1Password containing the API key.
        key_name (str): The specific field name within the item that holds the API key.
        vault (str, optional): The name of the 1Password vault to search in. Defaults to "API".

    Returns:
        str: The retrieved API key as a string.

    Raises:
        Exception: If there's an error connecting to 1Password or retrieving the key.
            The exception message will include details about the specific error encountered.

    Example:
        >>> api_key = get_api("OpenAI", "API_KEY", "Development")
        >>> print(api_key)
        'sk-1234567890abcdef1234567890abcdef'
    """
    try:
        client = new_client_from_environment()
        item = client.get_item(item, vault)
        for field in item.fields:
            if field.label == key_name:
                return field.value
    except Exception as e:
        raise Exception(f"Connect Error: {e}")


def template_api_json(model: str, render_data: dict, system_messages: str, persona: str, provider: str = "openai") -> dict:
    """
    Get the completion response from the API using the specified model and return it as a JSON object.

    This function sends a request to an AI model API, using a templated system message
    and specified persona. It then processes the response to ensure it's in valid JSON format.

    Args:
        model (str): The name of the AI model to use for the API call (e.g., "gpt-4", "claude-3.5").
        render_data (Dict): A dictionary containing data to render the template. 
            For example: {"name": "John", "age": 30}.
        system_message (str): A Jinja2 template string to be used as the system message.
            This will be rendered with the render_data.
        persona (str): A string describing the persona or role the AI should adopt for this response.

    Returns:
        Dict: The API response parsed as a Python dictionary. The structure of this dictionary
        will depend on the specific response from the AI model.

    Raises:
        json.JSONDecodeError: If the API response cannot be parsed as valid JSON.
        Any exceptions raised by the underlying get_completion_api or json.loads functions.

    Example:
        >>> model = "gpt-4"
        >>> render_data = {"user_name": "Alice", "task": "summarize"}
        >>> system_message = "You are an AI assistant helping {{user_name}} to {{task}} a document."
        >>> persona = "helpful assistant"
        >>> response = template_api_json(model, render_data, system_message, persona)
        >>> print(response)
        {'summary': 'This is a summary of the document...', 'key_points': ['Point 1', 'Point 2']}
    """
    xtemplate = Template(system_messages)
    prompt = xtemplate.render(render_data)
    response = Intelisys(provider=provider, model=model, system_message=persona).chat(prompt)
    response = response.strip("```json\n").strip("```").strip()
    response = json.loads(response)
    return response

def template_api(model: str, render_data: dict, system_messages: str, persona: str, provider: str = "openai") -> str:
    """
    Get the completion response from the API using the specified model.

    This function is similar to template_api_json, but returns the raw string response
    from the AI model instead of attempting to parse it as JSON.

    Args:
        model (str): The name of the AI model to use for the API call (e.g., "gpt-4", "claude-3.5").
        render_data (Dict): A dictionary containing data to render the template. 
            For example: {"name": "John", "age": 30}.
        system_message (str): A Jinja2 template string to be used as the system message.
            This will be rendered with the render_data.
        persona (str): A string describing the persona or role the AI should adopt for this response.

    Returns:
        str: The raw API response as a string. This could be in any format, depending on
        the AI model's output (e.g., plain text, markdown, or even JSON as a string).

    Raises:
        Any exceptions raised by the underlying get_completion_api function.

    Example:
        >>> model = "gpt-4"
        >>> render_data = {"topic": "artificial intelligence"}
        >>> system_message = "Explain {{topic}} in simple terms."
        >>> persona = "friendly teacher"
        >>> response = template_api(model, render_data, system_message, persona)
        >>> print(response)
        "Artificial Intelligence, or AI, is like teaching computers to think and learn..."
    """
    xtemplate = Template(system_messages)
    prompt = xtemplate.render(render_data)
    response = Intelisys(provider=provider, model=model, system_message=persona).chat(prompt)
    return response

def initialize_client() -> OpenAI:
    """
    Initialize the OpenAI client with the API key retrieved from 1Password.

    This function retrieves the OpenAI API key from 1Password using the get_api function,
    then initializes and returns an OpenAI client instance.

    Returns:
        OpenAI: An initialized OpenAI client instance ready for making API calls.

    Raises:
        Exception: If there's an error retrieving the API key or initializing the client.
            This could be due to issues with 1Password access or invalid API keys.

    Example:
        >>> client = initialize_client()
        >>> # Now you can use the client to make OpenAI API calls
        >>> response = client.completions.create(model="text-davinci-002", prompt="Hello, AI!")
    """
    api_key = get_api("OPEN-AI", "Mamba")
    return OpenAI(api_key=api_key)

def create_thread(client: OpenAI):
    """
    Create a new thread using the OpenAI client.

    This function initializes a new conversation thread using the provided OpenAI client.
    Threads are used to maintain context in multi-turn conversations with AI assistants.

    Args:
        client (OpenAI): An initialized OpenAI client object.

    Returns:
        Thread: A new thread object representing the created conversation thread.

    Example:
        >>> client = initialize_client()
        >>> new_thread = create_thread(client)
        >>> print(new_thread.id)
        'thread_abc123...'
    """
    return client.beta.threads.create()

def send_message(client: OpenAI, thread_id: str, reference: str):
    """
    Send a message to the specified thread.

    This function adds a new message to an existing conversation thread. The message
    is sent with the 'user' role, representing input from the user to the AI assistant.

    Args:
        client (OpenAI): An initialized OpenAI client object.
        thread_id (str): The ID of the thread to send the message to.
        reference (str): The content of the message to send.

    Returns:
        Message: The created message object, containing details about the sent message.

    Example:
        >>> client = initialize_client()
        >>> thread_id = "thread_abc123..."
        >>> message = send_message(client, thread_id, "What's the weather like today?")
        >>> print(message.content)
        'What's the weather like today?'
    """
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=reference,
    )

def run_assistant(client: OpenAI, thread_id: str, assistant_id: str):
    """
    Run the assistant for the specified thread.

    This function initiates a new run of the AI assistant on the specified thread.
    A run represents the assistant's process of analyzing the conversation and generating a response.

    Args:
        client (OpenAI): An initialized OpenAI client object.
        thread_id (str): The ID of the thread to run the assistant on.
        assistant_id (str): The ID of the assistant to run.

    Returns:
        Run: The created run object, containing details about the initiated assistant run.

    Example:
        >>> client = initialize_client()
        >>> thread_id = "thread_abc123..."
        >>> assistant_id = "asst_def456..."
        >>> run = run_assistant(client, thread_id, assistant_id)
        >>> print(run.status)
        'queued'
    """
    return client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )

def wait_for_run_completion(client: OpenAI, thread_id: str, run_id: str):
    """
    Wait for the assistant run to complete.

    This function polls the status of a run until it's no longer in a 'queued' or 'in_progress' state.
    It includes a small delay between checks to avoid excessive API calls.

    Args:
        client (OpenAI): An initialized OpenAI client object.
        thread_id (str): The ID of the thread.
        run_id (str): The ID of the run to wait for.

    Returns:
        Run: The completed run object, containing the final status and any output from the assistant.

    Example:
        >>> client = initialize_client()
        >>> thread_id = "thread_abc123..."
        >>> run_id = "run_ghi789..."
        >>> completed_run = wait_for_run_completion(client, thread_id, run_id)
        >>> print(completed_run.status)
        'completed'
    """
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    while run.status in ["queued", "in_progress"]:
        sleep(0.5)  # Add a delay to avoid rapid polling
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run

def get_assistant_responses(client: OpenAI, thread_id: str) -> List[str]:
    """
    Retrieve and clean the assistant's responses from the thread.

    This function fetches all messages in a thread and extracts the content of messages
    sent by the assistant. It returns these responses as a list of strings.

    Args:
        client (OpenAI): An initialized OpenAI client object.
        thread_id (str): The ID of the thread to retrieve responses from.

    Returns:
        List[str]: A list of assistant responses, where each response is a string.

    Example:
        >>> client = initialize_client()
        >>> thread_id = "thread_abc123..."
        >>> responses = get_assistant_responses(client, thread_id)
        >>> for response in responses:
        ...     print(response)
        'Here's the weather forecast for today...'
        'Is there anything else you'd like to know?'
    """
    message_list = client.beta.threads.messages.list(thread_id=thread_id)
    assistant_responses = [
        message.content[0].text.value
        for message in message_list.data
        if message.role == "assistant"
    ]
    return assistant_responses

def get_assistant(reference: str, assistant_id: str) -> List[str]:
    """
    Get the assistant's response for the given reference and assistant ID.

    This function encapsulates the entire process of interacting with an AI assistant:
    creating a thread, sending a message, running the assistant, and retrieving the responses.

    Args:
        reference (str): The reference message to send to the assistant. This is typically
                         the user's question or prompt.
        assistant_id (str): The ID of the assistant to use for generating the response.

    Returns:
        List[str]: A list of assistant responses. Each response is a string containing
                   the assistant's reply to the reference message.

    Example:
        >>> reference = "What are the three laws of robotics?"
        >>> assistant_id = "asst_def456..."
        >>> responses = get_assistant(reference, assistant_id)
        >>> for response in responses:
        ...     print(response)
        '1. A robot may not injure a human being or, through inaction, allow a human being to come to harm...'
    """
    client = initialize_client()
    thread = create_thread(client)
    send_message(client, thread.id, reference)
    run = run_assistant(client, thread.id, assistant_id)
    wait_for_run_completion(client, thread.id, run.id)
    responses = get_assistant_responses(client, thread.id)
    return responses

def get_completion_api(
    prompt: str,
    model_name: str,
    mode: str = "simple",
    system_message: Optional[str] = None
) -> Optional[str]:
    """
    Get the completion response from the API using the specified model.

    Args:
        prompt (str): The prompt to send to the API.
        model_name (str): The name of the model to use for completion. Supported models include:
            'gpt-4o-mini', 'gpt-4', 'gpt-4o', 'claude-3.5', 'gemini-flash', 'llama-3-70b',
            'llama-3.1-large', 'groq-llama', 'groq-fast', 'mistral-large'.
        mode (str, optional): The mode of message sending ('simple' or 'system'). Defaults to "simple".
        system_message (Optional[str], optional): The system message to send if in system mode. Defaults to None.

    Returns:
        Optional[str]: The completion response content, or None if an error occurs.

    Raises:
        ValueError: If an unsupported model or mode is specified.
    """
    try:
        # Model configurations
        model_configs = {
            "gpt-4o-mini": ("OPEN-AI", "Mamba", lambda x: x),
            "gpt-4": ("OPEN-AI", "Mamba", lambda x: x),
            "gpt-4o": ("OPEN-AI", "Mamba", lambda x: x),
            "claude-3.5": ("Anthropic", "CLI-Maya", lambda _: "claude-3-5-sonnet-20240620"),
            "gemini-flash": ("Gemini", "CLI-Maya", lambda _: "gemini/gemini-1.5-flash"),
            "llama-3-70b": ("TogetherAI", "API", lambda _: "together_ai/meta-llama/Llama-3-70b-chat-hf"),
            "llama-3.1-large": ("TogetherAI", "API", lambda _: "together_ai/meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"),
            "groq-llama": ("Groq", "Promptsys", lambda _: "groq/llama3-70b-8192"),
            "groq-fast": ("Groq", "Promptsys", lambda _: "groq/llama3-8b-8192"),
            "mistral-large": ("MistralAI", "API", lambda _: "mistral/mistral-large-latest"),
        }

        if model_name not in model_configs:
            raise ValueError(f"Unsupported model: {model_name}")

        api_name, key_name, model_func = model_configs[model_name]
        try:
            os.environ[f"{api_name.upper()}_API_KEY"] = get_api(api_name, key_name)
        except Exception as api_error:
            raise ValueError(f"Failed to get API key for {api_name}: {api_error}")

        selected_model = model_func(model_name)

        # Select message type
        match mode:
            case "simple":
                print("Message Simple")
                messages = [{"content": prompt, "role": "user"}]
            case "system":
                if system_message is None:
                    raise ValueError("system_message must be provided in system mode")
                messages = [
                    {"content": system_message, "role": "system"},
                    {"content": prompt, "role": "user"},
                ]
            case _:
                raise ValueError(f"Unsupported mode: {mode}")

        # Make the API call
        try:
            response = completion(
                model=selected_model,
                messages=messages,
                temperature=0.1,
            )
        except Exception as completion_error:
            raise RuntimeError(f"API call failed: {completion_error}")

        # Extract and return the response content
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as extract_error:
            raise ValueError(f"Failed to extract content from response: {extract_error}")

    except KeyError as ke:
        print(f"Key error: {str(ke)}")
    except ValueError as ve:
        print(f"Value error: {str(ve)}")
    except RuntimeError as re:
        print(f"Runtime error: {str(re)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    return None

def fix_json(json_string: str) -> str:
    """
    Fix and format a potentially malformed JSON string.

    This function uses an AI model to correct and format a given JSON string.
    It's particularly useful for handling JSON that may have syntax errors or
    formatting issues.

    Args:
        json_string (str): The JSON string to fix and format. This can be a
            malformed or incorrectly formatted JSON string.

    Returns:
        str: The fixed and formatted JSON string. If the input is valid JSON,
            it will be returned in a standardized format. If the input is invalid,
            the function attempts to correct common errors and return a valid JSON string.

    Example:
        >>> malformed_json = "{'key': 'value', 'nested': {'a':1, 'b': 2,}}"
        >>> fixed_json = fix_json(malformed_json)
        >>> print(fixed_json)
        '{"key": "value", "nested": {"a": 1, "b": 2}}'
    """
    prompt = f"You are a JSON formatter, fixing any issues with JSON formats. Review the following JSON: {json_string}. Return a fixed JSON formatted string but do not lead with ```json\n, without making changes to the content."
    return get_completion_api(prompt, "gemini-flash", "system", prompt)
