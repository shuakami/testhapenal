# 基于最新稳定的 Python 3.13
FROM python:3.13-slim

# 设置环境变量（更快日志输出、pip 无缓存）
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    # 将虚拟环境路径加入 PATH
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# 安装必要系统依赖（curl 用于健康检查；tzdata 便于本地化时间）
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl tzdata ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户，提升安全性
RUN useradd -m -u 1000 appuser

# 创建并启用虚拟环境
RUN python -m venv $VIRTUAL_ENV && pip install --upgrade pip

# 设置工作目录
WORKDIR /app

# 先拷贝依赖声明文件并安装依赖（充分利用 Docker 层缓存）
COPY requirements.txt ./
RUN pip install -r requirements.txt

# 拷贝源代码
COPY src/ ./src

# 为持久化数据准备目录
RUN mkdir -p /data && chown -R appuser:appuser /data /app

# 切换到非 root 用户
USER appuser

# 暴露端口
EXPOSE 8000