from __future__ import annotations
from typing import Mapping
from groq import DEFAULT_MAX_RETRIES, NOT_GIVEN, Groq, NotGiven, Timeout
from httpx import URL, Client
# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Iterable, Optional, overload
from typing_extensions import Literal

import httpx

from groq._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from groq._utils import (
    maybe_transform,
    async_maybe_transform,
)
from groq._compat import cached_property
from groq._resource import SyncAPIResource, AsyncAPIResource
from groq._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from groq._streaming import Stream, AsyncStream
from groq.types.chat import completion_create_params
from groq._base_client import (
    make_request_options,
)
from groq.types.chat.chat_completion import ChatCompletion
from groq.types.chat.chat_completion_chunk import ChatCompletionChunk
from groq.types.chat.chat_completion_tool_param import ChatCompletionToolParam
from groq.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from groq.types.chat.chat_completion_tool_choice_option_param import ChatCompletionToolChoiceOptionParam

class GroqAgent():
    '''
    Create a GroqAgent object to interact with the Groq API.
    Automatically handles chat for the agent.
    '''
    
    def __init__(self,
        *,
        api_key: str | None = None,
        base_url: str | URL | None = None,
        timeout: float | Timeout | NotGiven | None = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: Client | None = None,
        _strict_response_validation: bool = False
    ):
        self.client: Groq = Groq(api_key=api_key, base_url=base_url, timeout=timeout, max_retries=max_retries,
            default_headers=default_headers, default_query=default_query, http_client=http_client,
            _strict_response_validation=_strict_response_validation)
        self.chat_history: Iterable[ChatCompletionMessageParam] = []

    def ChatSettings(self,
        *,
        model: str | None = 'llama3-70b-8192',
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        function_call: Optional[completion_create_params.FunctionCall] | NotGiven = NOT_GIVEN,
        functions: Optional[Iterable[completion_create_params.Function]] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        parallel_tool_calls: Optional[bool] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: Optional[completion_create_params.ResponseFormat] | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str], None] | NotGiven = NOT_GIVEN,
        stream: Optional[Literal[False]] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: Optional[ChatCompletionToolChoiceOptionParam] | NotGiven = NOT_GIVEN,
        tools: Optional[Iterable[ChatCompletionToolParam]] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: Optional[str] | NotGiven = NOT_GIVEN,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ):
        '''
        Set the chat settings for the agent. Parameters are using in the 'client.chat.completions.create' method.
        '''
        if model is not None:
            self.model = model
        if frequency_penalty is not None:
            self.frequency_penalty = frequency_penalty
        if function_call is not None:
            self.function_call = function_call
        if functions is not None:
            self.functions = functions
        if logit_bias is not None:
            self.logit_bias = logit_bias
        if logprobs is not None:
            self.logprobs = logprobs
        if max_tokens is not None:
            self.max_tokens = max_tokens
        if n is not None:
            self.n = n
        if parallel_tool_calls is not None:
            self.parallel_tool_calls = parallel_tool_calls
        if presence_penalty is not None:
            self.presence_penalty = presence_penalty
        if response_format is not None:
            self.response_format = response_format
        if seed is not None:
            self.seed = seed
        if stop is not None:
            self.stop = stop
        if stream is not None:
            self.stream = stream
        if temperature is not None:
            self.temperature = temperature
        if tool_choice is not None:
            self.tool_choice = tool_choice
        if tools is not None:
            self.tools = tools
        if top_logprobs is not None:
            self.top_logprobs = top_logprobs
        if top_p is not None:
            self.top_p = top_p
        if user is not None:
            self.user = user
        if extra_headers is not None or not hasattr(self, 'extra_headers'):
            self.extra_headers = extra_headers
        if extra_query is not None or not hasattr(self, 'extra_query'):
            self.extra_query = extra_query
        if extra_body is not None or not hasattr(self, 'extra_body'):
            self.extra_body = extra_body
        if timeout is not None:
            self.timeout = timeout

    def SystemPrompt(self, prompt: str):
        '''
        Use this method to add a system prompt to the chat history. Altering how the agent responds.
        example: 'Respond as a personal assistant.' or 'Respond as a customer service agent.'
        '''
        self.chat_history.append({
            "role": "system",
            "content": prompt
        })

    def Chat(self, message: str):
        '''
        Chat with the agent. The agent will respond to the message.
        '''
        self.chat_history.append({
            "role": "user",
            "content": message
        })
        chat_completion = self.client.chat.completions.create(
            messages=self.chat_history,
            model=self.model, frequency_penalty=self.frequency_penalty, function_call=self.function_call,
            functions=self.functions, logit_bias=self.logit_bias, logprobs=self.logprobs, max_tokens=self.max_tokens,
            n=self.n, parallel_tool_calls=self.parallel_tool_calls, presence_penalty=self.presence_penalty,
            response_format=self.response_format, seed=self.seed, stop=self.stop, stream=self.stream, temperature=self.temperature,
            tool_choice=self.tool_choice, tools=self.tools, top_logprobs=self.top_logprobs, top_p=self.top_p,
            user=self.user, extra_headers=self.extra_headers, extra_query=self.extra_query, extra_body=self.extra_body,
            timeout=self.timeout
        )
        response_message = chat_completion.choices[0].message
        self.chat_history.append(response_message)
        return response_message.content
        