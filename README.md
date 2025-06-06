# ES to MySQL 同步工具

本工具用于将 Elasticsearch 指定前缀和日期的索引数据同步到 MySQL，并支持定时任务和命令行参数灵活控制。

## 环境依赖

- Python 3.8+
- Docker（可选，推荐用于生产环境）
- 推荐使用虚拟环境

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

所有配置均通过 `.env` 文件或环境变量进行管理，示例：

```env
# ES配置
ES_HOST=localhost
ES_PORT=9200
ES_USERNAME=
ES_PASSWORD=

# MySQL配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=es_sync

# 同步配置
BATCH_SIZE=1000
SCROLL_TIMEOUT=5m
CHECKPOINT_FILE=checkpoint.json

# 索引配置
INDEX_PREFIX=test
SYNC_TIME=02:00
TIMEZONE=Asia/Shanghai
```

- `INDEX_PREFIX`：要同步的索引前缀
- `SYNC_TIME`：定时任务执行时间（24小时制，如 `02:00`）
- `TIMEZONE`：时区（如 `Asia/Shanghai`）

## 使用方法

### 1. 命令行同步

**指定日期和前缀：**
```bash
python main.py --date 2025-03-20 --prefix test
```

**只指定日期（前缀用配置文件默认值）：**
```bash
python main.py --date 2025-03-20
```

**只指定前缀（日期用昨天）：**
```bash
python main.py --prefix test
```

**什么都不指定（用默认前缀和昨天日期）：**
```bash
python main.py
```

### 2. 启动定时任务

每天定时自动同步（时间和前缀由 `.env` 配置）：

```bash
python main.py --schedule
```

### 3. Docker 运行（可选）

构建镜像并启动：

```bash
docker-compose build
docker-compose up -d
```

## 日志

日志文件保存在 `logs/` 目录下，按天轮转，保留最近 7 天。

## 常见问题

- **时区问题**：请确保 `.env` 中 `TIMEZONE` 设置为你服务器的本地时区，否则日期可能不准确。
- **索引匹配规则**：默认匹配 `{前缀}.*{日期}` 结尾的索引，如 `test-2025-03-20`、`test_log_2025-03-20`。
- **参数优先级**：命令行参数优先于 `.env` 配置。

## 贡献

欢迎提交 issue 和 PR！

# es-mysql-rsync-tool
