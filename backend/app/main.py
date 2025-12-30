"""
FastAPI 应用入口文件
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import agent, patients
from app.core.config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("🚀 智能慢病管理系统后端启动中...")
    yield
    logger.info("👋 智能慢病管理系统后端关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="智能慢病管理系统 API",
    description="基于 AI 的慢病管理平台后端（FastAPI + LlamaIndex + DeepSeek）",
    version="0.1.0",
    lifespan=lifespan,
)

# 配置 CORS（允许前端跨域请求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(agent.router)
app.include_router(patients.router)


@app.get("/")
async def root() -> dict:
    """根路径健康检查"""
    return {"message": "智能慢病管理系统 API 运行中", "version": "0.1.0"}


@app.get("/health")
async def health_check() -> dict:
    """健康检查接口"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
    )
