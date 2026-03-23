"""
Vercel Python 运行时入口：需暴露 ASGI 应用变量 `app`。

说明：主界面是 Streamlit（本地/容器用 `streamlit run app.py`），无法在 Vercel Serverless
上直接跑完整问答 + Chroma。此处仅提供健康检查与说明，便于通过构建与边缘路由。
"""

from fastapi import FastAPI

app = FastAPI(title="LiHelper API", version="0.1.0")


@app.get("/")
async def root():
    return {
        "service": "LiHelper",
        "hint": "Web UI 请使用 Streamlit Cloud / Docker / VPS 部署 streamlit run app.py",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
