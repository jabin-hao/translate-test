import os
import sys

import ctranslate2
import sentencepiece as spm

from app.config import MODELS_DIR


class OpusMTTranslator:
    """封装单个 Opus-MT CTranslate2 模型"""

    def __init__(self, model_dir: str):
        self.model_dir = model_dir
        self.translator = ctranslate2.Translator(
            model_dir, device="cpu", inter_threads=os.cpu_count() or 4
        )
        self.sp_source = spm.SentencePieceProcessor(
            os.path.join(model_dir, "source.spm")
        )
        self.sp_target = spm.SentencePieceProcessor(
            os.path.join(model_dir, "target.spm")
        )

    def translate(self, texts: list[str]) -> list[str]:
        tokenized = [self.sp_source.encode(t, out_type=str) + ["</s>"] for t in texts]
        results = self.translator.translate_batch(
            tokenized, max_decoding_length=256, beam_size=4
        )
        return [self.sp_target.decode(r.hypotheses[0]) for r in results]


# ---------- 全局模型实例 ----------
zh_en: OpusMTTranslator | None = None
en_es: OpusMTTranslator | None = None


def load_models():
    """加载所有翻译模型，失败则退出进程"""
    global zh_en, en_es

    zh_en_dir = os.path.join(MODELS_DIR, "opus-mt-zh-en")
    en_es_dir = os.path.join(MODELS_DIR, "opus-mt-en-es")

    for d in [zh_en_dir, en_es_dir]:
        if not os.path.isdir(d):
            print(f"[ERROR] 模型目录不存在: {d}")
            print("请先运行 convert_local.py 下载并转换模型")
            sys.exit(1)

    print("正在加载模型 opus-mt-zh-en ...")
    zh_en = OpusMTTranslator(zh_en_dir)
    print("正在加载模型 opus-mt-en-es ...")
    en_es = OpusMTTranslator(en_es_dir)
    print("所有模型加载完成!")


def models_loaded() -> bool:
    return zh_en is not None and en_es is not None
