import argparse
import schedule
import time
from datetime import datetime, timedelta
from loguru import logger
from src.sync_service import SyncService
from src.config import settings
import re
import pytz

def get_yesterday_date():
    """获取昨天的日期，格式为YYYY-MM-DD"""
    # 使用配置的时区
    tz = pytz.timezone(settings.TIMEZONE)
    yesterday = datetime.now(tz) - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def get_matching_indices(prefix: str, date: str):
    """获取匹配指定前缀和日期的索引列表"""
    service = SyncService()
    try:
        # 获取所有索引
        indices = service.es_client.get_all_indices()
        
        # 构建正则表达式模式
        pattern = f"^{prefix}.*{date}$"
        
        # 过滤匹配的索引
        matching_indices = [index for index in indices if re.match(pattern, index)]
        
        return matching_indices
    finally:
        service.es_client.close()

def sync_indices(date: str = None, prefix: str = None):
    """同步所有匹配的索引"""
    try:
        # 如果没有指定日期，使用昨天的日期
        if date is None:
            date = get_yesterday_date()
        
        # 如果没有指定前缀，使用配置的前缀
        if prefix is None:
            prefix = settings.INDEX_PREFIX
        
        # 获取匹配的索引列表
        indices = get_matching_indices(prefix, date)
        
        if not indices:
            logger.warning(f"没有找到匹配的索引，前缀: {prefix}, 日期: {date}")
            return
        
        # 同步每个索引
        service = SyncService()
        for index in indices:
            try:
                logger.info(f"开始同步索引: {index}")
                service.sync_index(index)
            except Exception as e:
                logger.error(f"同步索引 {index} 失败: {str(e)}")
                continue
    except Exception as e:
        logger.error(f"同步过程发生错误: {str(e)}")

def main():
    """主函数"""
    # 设置日志格式
    logger.add("logs/sync_{time}.log", rotation="1 day", retention="7 days")
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='ES数据同步到MySQL工具')
    parser.add_argument('--date', help='指定要同步的日期，格式为YYYY-MM-DD')
    parser.add_argument('--prefix', help='指定要同步的索引前缀')
    parser.add_argument('--schedule', action='store_true', help='是否启动定时任务')
    args = parser.parse_args()
    
    if args.schedule:
        # 设置定时任务，使用配置的执行时间和时区
        schedule.every().day.at(settings.SYNC_TIME).do(sync_indices)
        logger.info(f"同步服务已启动，将在每天 {settings.SYNC_TIME} ({settings.TIMEZONE}) 执行同步任务...")
        
        # 运行定时任务
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    else:
        # 直接执行同步任务
        sync_indices(args.date, args.prefix)

if __name__ == "__main__":
    main() 