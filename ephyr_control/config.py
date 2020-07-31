from typing import Dict, Optional, Iterable, Literal

from pydantic import BaseModel

__all__ = ["MixClientSettings"]


class ZMQConfig(BaseModel):
    host: str
    port: int


class StreamConfig(BaseModel):
    delay: str
    volume: float
    zmq: ZMQConfig

    @property
    def ip_address(self) -> str:
        return f"{self.zmq.host}:{self.zmq.port}"


class PushStreamRTMP(BaseModel):
    url: str


class LangStreamConfig(BaseModel):
    org: StreamConfig
    trn: StreamConfig

    def __getattr__(self, item) -> StreamConfig:
        return self.__dict__[item]


class SpecificStream(BaseModel):
    ru: Optional[LangStreamConfig]
    en: Optional[LangStreamConfig]
    es: Optional[LangStreamConfig]
    de: Optional[LangStreamConfig]
    it: Optional[LangStreamConfig]
    fr: Optional[LangStreamConfig]
    lv: Optional[LangStreamConfig]
    uk: Optional[LangStreamConfig]
    cs: Optional[LangStreamConfig]
    ro: Optional[LangStreamConfig]
    ja: Optional[LangStreamConfig]
    push: PushStreamRTMP

    @property
    def available_languages(self):
        return [lang_code for lang_code, f_val in self]

    def __iter__(self):
        yield from (
            (f_name, f_val)
            for f_name, f_val in self.__dict__.items()
            if f_name != "push" and getattr(self, f_name)
        )

    def __dir__(self) -> Iterable[str]:
        return ["push"] + self.available_languages


class MixClientSettings(BaseModel):
    __root__: Dict[str, SpecificStream]

    def __iter__(self):
        yield from ((f_name, f_val) for f_name, f_val in self.__root__.items())

    def __getattr__(self, item):
        return self.__root__[item]

    def __getitem__(self, item):
        return self.__root__[item]

    def __dir__(self) -> Iterable[str]:
        return list(self.__root__.keys())
