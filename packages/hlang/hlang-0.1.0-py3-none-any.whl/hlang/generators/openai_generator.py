from typing import Optional, Iterable, Literal, Union, List, Mapping

import httpx
import openai
from openai import NotGiven, NOT_GIVEN
from openai.types.chat import ChatCompletionToolParam, ChatCompletionToolChoiceOptionParam, \
    ChatCompletionStreamOptionsParam, completion_create_params

from openlangchain.dataclasses.message import ChatMessage
from openlangchain.generators.generator import ABCChatGenerator


class OpenAIChatGenerator(ABCChatGenerator):
    def __init__(self, model_name: str):
        self.client = openai.Client()
        self.model_name = model_name

    def generate(self,
                 messages: [ChatMessage],
                 frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
                 function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
                 functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
                 logit_bias: Optional[dict[str, int]] | NotGiven = NOT_GIVEN,
                 logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
                 max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
                 n: Optional[int] | NotGiven = NOT_GIVEN,
                 parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
                 presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
                 response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
                 seed: Optional[int] | NotGiven = NOT_GIVEN,
                 service_tier: Optional[Literal["auto", "default"]] | NotGiven = NOT_GIVEN,
                 stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
                 temperature: Optional[float] | NotGiven = NOT_GIVEN,
                 tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
                 tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
                 top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
                 top_p: Optional[float] | NotGiven = NOT_GIVEN,
                 user: str | NotGiven = NOT_GIVEN,

                 extra_headers=None,
                 extra_query: Mapping[str, object] | None = None,
                 extra_body=None,
                 timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
                 ) -> ChatMessage:
        self._prompt_sanity_check(messages)
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_tokens=max_tokens,
            n=n,
            parallel_tool_calls=parallel_tool_calls,
            presence_penalty=presence_penalty,
            response_format=response_format,
            seed=seed,
            service_tier=service_tier,
            stop=stop,
            stream=False,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )
        text = response.response.text
        return ChatMessage.from_assistant(text)

    def stream(self,
               messages: [ChatMessage],
               frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
               function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
               functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
               logit_bias: Optional[dict[str, int]] | NotGiven = NOT_GIVEN,
               logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
               max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
               parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
               presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
               response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
               seed: Optional[int] | NotGiven = NOT_GIVEN,
               service_tier: Optional[Literal["auto", "default"]] | NotGiven = NOT_GIVEN,
               stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
               temperature: Optional[float] | NotGiven = NOT_GIVEN,
               tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
               tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
               top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
               top_p: Optional[float] | NotGiven = NOT_GIVEN,
               user: str | NotGiven = NOT_GIVEN,
               stream_options: Optional[ChatCompletionStreamOptionsParam] | NotGiven = NotGiven,
               extra_headers=None,
               extra_query: Mapping[str, object] | None = None,
               extra_body=None,
               timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
               ) -> Iterable[str]:
        iterator = self.client.chat.completions.create(
            messages=[m.to_dict() for m in messages],
            model=self.model_name,
            frequency_penalty=frequency_penalty,
            function_call=function_call,
            functions=functions,
            logit_bias=logit_bias,
            logprobs=logprobs,
            max_tokens=max_tokens,
            parallel_tool_calls=parallel_tool_calls,
            presence_penalty=presence_penalty,
            response_format=response_format,
            seed=seed,
            service_tier=service_tier,
            stop=stop,
            stream=True,
            stream_options=stream_options,
            temperature=temperature,
            tool_choice=tool_choice,
            tools=tools,
            top_logprobs=top_logprobs,
            top_p=top_p,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout
        )
        for chunk in iterator:
            yield chunk.choices[0].delta.content
