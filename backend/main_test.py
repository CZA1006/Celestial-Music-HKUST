from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="28星宿API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "28星宿天体音乐生成器 API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/api/health")
def health():
    return {"status": "healthy"}

@app.get("/api/test")
def test():
    return {"message": "API测试成功"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main_test:app", host="0.0.0.0", port=port)
