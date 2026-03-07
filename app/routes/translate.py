from fastapi import APIRouter, HTTPException

from app import translator
from app.schemas import TranslateRequest, TranslateResponse

router = APIRouter()


def translate_batch(texts: list[str], source: str, target: str) -> list[str]:
    src = source.strip().lower()
    tgt = target.strip().lower()

    if src == "zh" and tgt == "es":
        en_texts = translator.zh_en.translate(texts)
        return translator.en_es.translate(en_texts)
    elif src == "zh" and tgt == "en":
        return translator.zh_en.translate(texts)
    elif src == "en" and tgt == "es":
        return translator.en_es.translate(texts)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的语言对: {src}→{tgt}。支持: zh→es, zh→en, en→es",
        )


@router.post("/translate", response_model=TranslateResponse)
async def translate(req: TranslateRequest):
    results = translate_batch(req.q, req.source, req.target)
    return TranslateResponse(translatedText=results)


@router.get("/health")
async def health():
    return {"status": "ok", "models_loaded": translator.models_loaded()}


@router.get("/languages")
async def languages():
    return {
        "supported_pairs": ["zh→es", "zh→en", "en→es"],
        "source": ["zh", "en"],
        "target": ["en", "es"],
    }
