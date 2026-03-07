# 手动下载模型教程

`download_model.py` 会自动下载并转换模型，但如果网络太慢，可以按以下步骤手动操作。

---

## 步骤总览

1. 从镜像站手动下载两个 HuggingFace 模型
2. 运行本地转换脚本，将模型转为 CTranslate2 INT8 格式

---

## 第 1 步：手动下载模型文件

需要下载 **两个模型**，每个模型需要下载几个关键文件。

### 模型 1：opus-mt-zh-en（中→英）

在浏览器中逐个下载以下文件：

| 文件 | 下载链接（HF 镜像） |
|---|---|
| config.json | https://hf-mirror.com/Helsinki-NLP/opus-mt-zh-en/resolve/main/config.json |
| pytorch_model.bin | https://hf-mirror.com/Helsinki-NLP/opus-mt-zh-en/resolve/main/pytorch_model.bin |
| source.spm | https://hf-mirror.com/Helsinki-NLP/opus-mt-zh-en/resolve/main/source.spm |
| target.spm | https://hf-mirror.com/Helsinki-NLP/opus-mt-zh-en/resolve/main/target.spm |
| vocab.json | https://hf-mirror.com/Helsinki-NLP/opus-mt-zh-en/resolve/main/vocab.json |
| tokenizer_config.json | https://hf-mirror.com/Helsinki-NLP/opus-mt-zh-en/resolve/main/tokenizer_config.json |

下载后放到这个目录：
```
translate-server/
  hf_downloads/
    opus-mt-zh-en/
      config.json
      pytorch_model.bin
      source.spm
      target.spm
      vocab.json
      tokenizer_config.json
```

### 模型 2：opus-mt-en-es（英→西）

| 文件 | 下载链接（HF 镜像） |
|---|---|
| config.json | https://hf-mirror.com/Helsinki-NLP/opus-mt-en-es/resolve/main/config.json |
| pytorch_model.bin | https://hf-mirror.com/Helsinki-NLP/opus-mt-en-es/resolve/main/pytorch_model.bin |
| source.spm | https://hf-mirror.com/Helsinki-NLP/opus-mt-en-es/resolve/main/source.spm |
| target.spm | https://hf-mirror.com/Helsinki-NLP/opus-mt-en-es/resolve/main/target.spm |
| vocab.json | https://hf-mirror.com/Helsinki-NLP/opus-mt-en-es/resolve/main/vocab.json |
| tokenizer_config.json | https://hf-mirror.com/Helsinki-NLP/opus-mt-en-es/resolve/main/tokenizer_config.json |

下载后放到：
```
translate-server/
  hf_downloads/
    opus-mt-en-es/
      config.json
      pytorch_model.bin
      source.spm
      target.spm
      vocab.json
      tokenizer_config.json
```

> **提示**：`pytorch_model.bin` 是最大的文件（每个约 300MB），其他文件都很小。
> 如果浏览器下载慢，也可以用下载工具（如 IDM、aria2）下载。

---

## 第 2 步：转换为 CTranslate2 格式

文件全部下载好后，运行转换脚本：

```bash
python convert_local.py
```

转换完成后，目录结构如下：
```
translate-server/
  models/
    opus-mt-zh-en/    ← CTranslate2 INT8 格式（约 70-80MB）
      model.bin
      source.spm
      target.spm
      vocab.json
      ...
    opus-mt-en-es/    ← CTranslate2 INT8 格式（约 70-80MB）
      model.bin
      source.spm
      target.spm
      vocab.json
      ...
```

---

## 第 3 步：启动服务

```bash
python main.py
```

访问 http://127.0.0.1:8000/health 确认服务正常运行。

---

## 备选：用 PowerShell 批量下载

如果希望用命令行下载，可以在项目根目录执行：

```powershell
# 创建目录
New-Item -ItemType Directory -Force -Path hf_downloads/opus-mt-zh-en
New-Item -ItemType Directory -Force -Path hf_downloads/opus-mt-en-es

# 下载 opus-mt-zh-en
$base1 = "https://hf-mirror.com/Helsinki-NLP/opus-mt-zh-en/resolve/main"
foreach ($f in @("config.json","pytorch_model.bin","source.spm","target.spm","vocab.json","tokenizer_config.json")) {
    Write-Host "下载 opus-mt-zh-en/$f ..."
    Invoke-WebRequest -Uri "$base1/$f" -OutFile "hf_downloads/opus-mt-zh-en/$f"
}

# 下载 opus-mt-en-es
$base2 = "https://hf-mirror.com/Helsinki-NLP/opus-mt-en-es/resolve/main"
foreach ($f in @("config.json","pytorch_model.bin","source.spm","target.spm","vocab.json","tokenizer_config.json")) {
    Write-Host "下载 opus-mt-en-es/$f ..."
    Invoke-WebRequest -Uri "$base2/$f" -OutFile "hf_downloads/opus-mt-en-es/$f"
}

Write-Host "下载完成！接下来运行: python convert_local.py"
```
