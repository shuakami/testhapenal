"""
配置模块：使用 Pydantic Settings 读取环境变量，提供全局配置对象。
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # 应用相关
    app_name: str = "FastAPI + SQLite（Compose 教学示例）"
    app_env: str = "dev"

    # 数据库连接串（异步 SQLAlchemy 连接 URL）
    database_url: str = "sqlite+aiosqlite:///./app.db"  # 默认开发下使用相对路径

    # 通过 .env 文件读取变量（也支持 Docker Compose env_file 注入）
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# 单例配置对象
settings = Settings()
