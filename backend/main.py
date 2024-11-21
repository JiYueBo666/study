from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.endpoints import users, auth, articles

app = FastAPI(title="Blog API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(articles.router, prefix="/api/v1/articles")


@app.get("/")
async def root():
    return {"message": "Welcome to Blog API"}
