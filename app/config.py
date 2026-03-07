import os
import sys


def get_base_dir() -> str:
    """获取程序根目录（兼容 PyInstaller 打包后）"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_DIR = get_base_dir()
MODELS_DIR = os.path.join(BASE_DIR, "models")

APP_TITLE = "离线翻译服务 (zh→es)"
APP_VERSION = "1.0.0"
APP_HOST = "0.0.0.0"
APP_PORT = 6000
