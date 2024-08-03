# walledeval/llm/openai.py

import openai

from typing import Optional, Union

from walledeval.types import Messages, LLMType
from walledeval.util import transform_messages
from walledeval.llm.core import LLM

__all__ = [
    "Anyscale"
]


class Anyscale(LLM):
    def __init__(self,
                 model_id: str,
                 api_key: str,
                 api_base_url: str = "https://api.endpoints.anyscale.com/v1",
                 system_prompt: str = "",
                 type: Optional[Union[LLMType, int]] = LLMType.NEITHER):
        super().__init__(
            model_id, system_prompt,
            type
        )
        self.client = openai.OpenAI(
            base_url=api_base_url,
            api_key=api_key
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
        message = self.client.completions.create(
            max_tokens=max_new_tokens,
            prompt=text,
            temperature=temperature,
            model=self.name
        )
        output = message.choices[0].text
        return output
