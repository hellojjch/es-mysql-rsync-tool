FROM python:3.9-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ /app/src/
COPY main.py /app/

# 设置环境变量
ENV PYTHONPATH=/app

# 创建数据目录
RUN mkdir -p /app/data

# 设置工作目录
WORKDIR /app/data

# 运行同步程序
ENTRYPOINT ["python", "/app/main.py"] 