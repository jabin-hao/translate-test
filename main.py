import uvicorn

from app import create_app
from app.config import APP_HOST, APP_PORT

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("  离线翻译服务 v1.0 (zh→es)")
    print(f"  http://127.0.0.1:{APP_PORT}")
    print("  API: POST /translate")
    print("=" * 50)
    uvicorn.run(app, host=APP_HOST, port=APP_PORT, log_level="info")
