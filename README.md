# translate-server

离线中西翻译服务，基于 [Opus-MT](https://github.com/Helsinki-NLP/Opus-MT) 模型，通过 **zh→en→es** 两步翻译链实现中文到西班牙语翻译。使用 CTranslate2 INT8 量化推理，无需 GPU，无需联网。

## 支持的语言对

| 源语言 | 目标语言 | 模型 |
|--------|---------|------|
| zh | en | opus-mt-zh-en |
| en | es | opus-mt-en-es |
| zh | es | opus-mt-zh-en → opus-mt-en-es（链式） |

## 项目结构

```
translate-server/
├── main.py                    # 入口：启动 uvicorn
├── convert_local.py           # 模型转换工具
├── requirements.txt
├── build.bat                  # PyInstaller 打包脚本
├── translate-server.spec
├── docs/
│   └── MANUAL_DOWNLOAD.md     # 手动下载模型教程
├── models/                    # CTranslate2 INT8 模型（需转换生成）
└── app/
    ├── __init__.py            # FastAPI 应用工厂
    ├── config.py              # 配置常量
    ├── translator.py          # 翻译引擎
    ├── schemas.py             # 请求/响应模型
    └── routes/
        └── translate.py       # API 路由
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 下载并转换模型

按 [docs/MANUAL_DOWNLOAD.md](docs/MANUAL_DOWNLOAD.md) 教程将模型文件下载到 `hf_downloads/` 目录，然后运行转换：

```bash
python convert_local.py
```

转换后会在 `models/` 目录生成 INT8 量化模型。

### 3. 启动服务

```bash
python main.py
```

服务启动后监听 `http://127.0.0.1:6000`。

## API

### POST /translate

翻译文本。

**请求：**

```json
{
  "q": ["苹果手机", "蓝牙耳机"],
  "source": "zh",
  "target": "es"
}
```

**响应：**

```json
{
  "translatedText": ["Teléfono Apple.", "Auriculares Bluetooth."]
}
```

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| q | list[str] | — | 待翻译文本列表 |
| source | str | `"zh"` | 源语言 |
| target | str | `"es"` | 目标语言 |

### GET /health

健康检查。

```json
{"status": "ok", "models_loaded": true}
```

### GET /languages

返回支持的语言对。

## 打包

使用 PyInstaller 打包为独立可执行文件：

```bash
build.bat
```

输出目录：`dist/translate-server/`
