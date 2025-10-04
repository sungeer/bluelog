import sys

from loguru import logger

from viper import settings

log_path = settings.log_path

logger.remove()

logger.add(
    log_path,
    rotation='00:00',  # 每天零点新文件
    retention='10 days',  # 保留时长或数量
    format='{time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {message}',
    encoding='utf-8',
    enqueue=True,  # 启用异步日志处理
    level='INFO',
    diagnose=False,  # 关闭变量值
    backtrace=False,  # 关闭完整堆栈跟踪
    colorize=False
)

if settings.with_debug:
    logger.add(
        sink=sys.stdout,  # 输出到标准输出流
        format='{time:YYYY-MM-DD HH:mm:ss.SSS} - {level} - {message}',  # 日志格式
        level='DEBUG',
        diagnose=False,
        backtrace=False,
        colorize=False,
        enqueue=True
    )
