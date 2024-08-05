import json
import os
from dataclasses import dataclass, field
from typing import List

import requests
from edi_core.ai.writesonic import *


@dataclass(kw_only=True)
class ChatSonicConfig:
    api_key: str = os.environ.get("SONIC_KEY")
    base_url: str = WRITESONIC_BASE_URL
    path: str = CHATSONIC_URL_PATH
    engine: str = WRITESONIC_ENGINE_PREMIUM
    language: str = WRITESONIC_LANGUAGE_ENGLISH
    enable_memory: bool = False
    enable_google_results: bool = False

    def __post_init__(self):
        if not self.api_key:
            raise ValueError("token is required")
        if self.engine not in WRITESONIC_ENGINES:
            raise ValueError("engine is invalid")
        if self.language not in WRITESONIC_LANGUAGES:
            raise ValueError("language is invalid")

    def get_request_url(self):
        return f'{self.base_url}{self.path}'


@dataclass
class ChatSonicPayload:
    @dataclass
    class Message:
        is_sent: bool
        message: str

    input_text: str
    history_data: List[Message] = field(default_factory=list)
    enable_memory: bool = False
    enable_google_results: bool = False

    def push_response(self, message: str):
        message_sent = self.Message(is_sent=True, message=self.input_text)
        message_received = self.Message(is_sent=False, message=message)
        self.history_data.append(message_sent)
        self.history_data.append(message_received)
        self.input_text = ''

    def set_config(self, config: ChatSonicConfig):
        self.enable_memory = config.enable_memory
        self.enable_google_results = config.enable_google_results

    def to_json(self):
        return json.dumps(self.__dict__)


@dataclass
class ChatSonicResponse:
    message: str
    image_urls: List[str] = field(default_factory=list)

    @staticmethod
    def from_json(json_data):
        return ChatSonicResponse(
            message=json_data['message'],
            image_urls=json_data['image_urls']
        )


class ChatSonic:
    _config: ChatSonicConfig
    _session = requests.Session()

    def __init__(self, config: ChatSonicConfig):
        self._config = config

    def call(self, payload: ChatSonicPayload) -> (ChatSonicResponse, ChatSonicPayload):
        url = self._config.get_request_url()

        raw_response = self._session.post(
            url=url,
            headers=self.get_request_headers(),
            params=self.get_request_params(),
            data=payload.to_json()
        )

        raw_response.raise_for_status()

        response = ChatSonicResponse.from_json(raw_response.json())
        payload.push_response(response.message)

        return response, payload

    def chat(self, message: str) -> ChatSonicPayload:
        payload = ChatSonicPayload(input_text=message);
        payload.set_config(self._config)
        return self.call(payload)

    def get_request_headers(self):
        return {'X-API-KEY': self._config.api_key}

    def get_request_params(self):
        return {
            'engine': self._config.engine,
            'language': self._config.language
        }
