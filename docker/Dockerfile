FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 创建必要的目录
RUN mkdir -p /app/data /app/logs

# 设置目录权限
RUN chmod 755 /app/data /app/logs

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ /app/src/
COPY main.py /app/

# 设置环境变量
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:9200/_cluster/health || exit 1

# 设置工作目录
WORKDIR /app

# 设置入口点
ENTRYPOINT ["python", "/app/main.py", "--schedule"] 