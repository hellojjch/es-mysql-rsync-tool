import argparse
from loguru import logger
from .sync_service import SyncService

def main():
    parser = argparse.ArgumentParser(description='ES数据同步到MySQL工具')
    parser.add_argument('--index', required=True, help='要同步的ES索引名称')
    args = parser.parse_args()
    
    try:
        logger.info(f"开始同步索引: {args.index}")
        sync_service = SyncService()
        sync_service.sync_index(args.index)
        logger.info("同步完成")
    except Exception as e:
        logger.error(f"同步失败: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main() 