from pydantic import BaseModel


class TranslateRequest(BaseModel):
    q: list[str]
    source: str = "zh"
    target: str = "es"
    format: str = "text"


class TranslateResponse(BaseModel):
    translatedText: list[str]
