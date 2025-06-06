# ES to MySQL 数据同步工具

这是一个用于将 Elasticsearch 数据同步到 MySQL 的工具，支持自动创建表结构、断点续传和容器化部署。

## 功能特点

- 根据 ES 索引 mapping 自动创建 MySQL 表结构
- 支持断点续传，确保数据同步的可靠性
- 提供 Docker 容器化部署方案
- 支持批量数据同步，提高同步效率
- 详细的日志记录

## 环境要求

- Python 3.9+
- Elasticsearch 8.x
- MySQL 8.x
- Docker & Docker Compose (用于容器化部署)

## 快速开始

1. 克隆项目并进入项目目录：
```bash
git clone <repository-url>
cd es-to-mysql
```

2. 配置环境变量：
创建 `.env` 文件并配置以下参数：
```
ES_HOST=your_es_host
ES_PORT=9200
ES_USERNAME=your_es_username
ES_PASSWORD=your_es_password

MYSQL_HOST=your_mysql_host
MYSQL_PORT=3306
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=es_sync
```

3. 使用 Docker Compose 启动服务：
```bash
docker-compose up -d
```

4. 执行同步：
```bash
docker-compose exec es-sync python -m src.main --index your_index_name
```

## 配置说明

- `BATCH_SIZE`: 每批同步的数据量
- `SCROLL_TIMEOUT`: ES scroll API 的超时时间
- `CHECKPOINT_FILE`: 断点续传的检查点文件路径

## 注意事项

1. 确保 ES 和 MySQL 服务正常运行
2. 检查网络连接是否正常
3. 确保有足够的磁盘空间
4. 建议在同步大量数据时适当调整 `BATCH_SIZE`

## 故障排除

1. 如果同步中断，检查日志文件
2. 确保 ES 和 MySQL 的连接信息正确
3. 检查磁盘空间是否充足
4. 查看网络连接是否正常

## 许可证

MIT License 

# es-mysql-rsync-tool
