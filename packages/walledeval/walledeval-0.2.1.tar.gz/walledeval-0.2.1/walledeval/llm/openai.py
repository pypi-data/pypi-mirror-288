# walledeval/llm/openai.py

import openai

from typing import Optional, Union

from walledeval.types import Messages, LLMType
from walledeval.util import transform_messages
from walledeval.llm.core import LLM

__all__ = [
    "OpenAI"
]


class OpenAI(LLM):
    def __init__(self,
                 model_id: str,
                 api_key: str,
                 system_prompt: str = "",
                 type: Optional[Union[LLMType, int]] = LLMType.NEITHER):
        super().__init__(
            model_id, system_prompt,
            type
        )
        self.client = openai.OpenAI(api_key=api_key)

    @classmethod
    def gpt4o(cls, api_key: str, system_prompt: str = ""):
        return cls(
            "gpt-4o",
            api_key, system_prompt
        )

    @classmethod
    def gpt4turbo(cls, api_key: str, system_prompt: str = ""):
        return cls(
            "gpt-4-turbo",
            api_key, system_prompt
        )

    @classmethod
    def gpt4(cls, api_key: str, system_prompt: str = ""):
        return cls(
            "gpt-4",
            api_key, system_prompt
        )
    
    @classmethod
    def gpt35turbo(cls, api_key: str, system_prompt: str = ""):
        return cls(
            "gpt-3.5-turbo",
            api_key, system_prompt
        )

    def chat(self,
             text: Messages,
             max_new_tokens: int = 1024,
             temperature: float = 0.1) -> str:
        messages = transform_messages(text, self.system_prompt)

        message = self.client.chat.completions.create(
            max_tokens=max_new_tokens,
            messages=messages,
            temperature=temperature,
            model=self.name
        )
        output = message.choices[0].message.content
        return output

    def complete(self,
                 text: str,
                 max_new_tokens: int = 1024,
                 temperature: float = 0.1) -> str:
        text = f"Continue writing: {text}"
        
        return self.chat(text, max_new_tokens=max_new_tokens, temperature=temperature)

