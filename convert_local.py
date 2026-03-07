"""
将手动下载的 Opus-MT 模型转换为 CTranslate2 INT8 格式。

使用前请先按 MANUAL_DOWNLOAD.md 教程将模型文件下载到 hf_downloads/ 目录。

用法: python convert_local.py
"""
import os
import shutil
import ctranslate2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HF_DIR = os.path.join(BASE_DIR, "hf_downloads")
MODELS_DIR = os.path.join(BASE_DIR, "models")

MODELS = [
    {"name": "opus-mt-zh-en"},
    {"name": "opus-mt-en-es"},
]


def convert_model(name: str):
    local_dir = os.path.join(HF_DIR, name)
    output_dir = os.path.join(MODELS_DIR, name)

    if os.path.isdir(output_dir) and os.path.isfile(os.path.join(output_dir, "model.bin")):
        print(f"已转换，跳过: {output_dir}")
        return

    # 检查本地模型文件
    required = ["config.json", "pytorch_model.bin", "source.spm", "target.spm", "vocab.json"]
    for f in required:
        if not os.path.isfile(os.path.join(local_dir, f)):
            print(f"[ERROR] 缺少文件: {os.path.join(local_dir, f)}")
            print("请按 MANUAL_DOWNLOAD.md 教程下载所有模型文件。")
            return

    print(f"正在转换: {local_dir} → {output_dir}")

    converter = ctranslate2.converters.TransformersConverter(
        model_name_or_path=local_dir,
    )
    converter.convert(
        output_dir=output_dir,
        quantization="int8",
        force=True,
    )

    # 复制 tokenizer 文件
    for filename in ["source.spm", "target.spm", "vocab.json", "tokenizer_config.json"]:
        src = os.path.join(local_dir, filename)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(output_dir, filename))
            print(f"  已复制: {filename}")

    print(f"转换完成: {name}\n")


def main():
    print("=" * 50)
    print("  本地模型转换 (手动下载 → CTranslate2 INT8)")
    print("=" * 50)

    if not os.path.isdir(HF_DIR):
        print(f"\n[ERROR] 未找到 hf_downloads/ 目录。")
        print("请先按 MANUAL_DOWNLOAD.md 教程下载模型文件。")
        return

    for model in MODELS:
        convert_model(model["name"])

    print("=" * 50)
    print("所有模型转换完成!")
    print("现在可以运行 main.py 启动翻译服务了。")


if __name__ == "__main__":
    main()
