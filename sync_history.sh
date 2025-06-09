#!/bin/bash

# 设置日志文件
LOG_FILE="logs/sync_history_$(date +%Y%m%d_%H%M%S).log"

# 确保日志目录存在
mkdir -p logs

# 记录开始时间
echo "开始执行历史数据同步: $(date)" | tee -a "$LOG_FILE"

# 设置起始日期和结束日期
START_DATE="2025-03-20"
END_DATE=$(date -d "yesterday" +%Y-%m-%d)

# 将日期转换为时间戳
START_TIMESTAMP=$(date -d "$START_DATE" +%s)
END_TIMESTAMP=$(date -d "$END_DATE" +%s)

# 遍历日期
current_timestamp=$START_TIMESTAMP
while [ $current_timestamp -le $END_TIMESTAMP ]; do
    current_date=$(date -d "@$current_timestamp" +%Y-%m-%d)
    echo "开始同步日期: $current_date" | tee -a "$LOG_FILE"
    
    # 执行同步命令
    python main.py --date "$current_date" --prefix test 2>&1 | tee -a "$LOG_FILE"
    
    # 检查同步是否成功
    if [ $? -eq 0 ]; then
        echo "日期 $current_date 同步成功" | tee -a "$LOG_FILE"
    else
        echo "日期 $current_date 同步失败" | tee -a "$LOG_FILE"
    fi
    
    # 增加一天
    current_timestamp=$((current_timestamp + 86400))
    
    # 添加延时，避免请求过于频繁
    sleep 5
done

# 记录结束时间
echo "历史数据同步完成: $(date)" | tee -a "$LOG_FILE" 