"""
核心配置模块

使用 Pydantic Settings 管理环境变量配置
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""

    # DeepSeek API 配置
    deepseek_api_key: str

    # 数据库配置
    neon_db_url: str

    # 应用配置
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    # CORS 配置
    allowed_origins: str = "http://localhost:3000"

    class Config:
        """Pydantic 配置"""

        env_file = ".env"
        case_sensitive = False


# 全局配置实例
settings = Settings()
