import sys
from pathlib import Path

from loguru import logger

from viper.core import settings

log_dir = Path(settings.BASE_DIR) / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

access_path = log_dir / 'access.log'
error_path = log_dir / 'error.log'

logger.remove()

logger.add(
    access_path,
    rotation='10MB',
    format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}',
    encoding='utf-8',
    enqueue=True,  # 启用异步日志处理
    level='DEBUG',
    diagnose=False,  # 关闭变量值
    backtrace=False,  # 关闭完整堆栈跟踪
    colorize=False,
    filter=lambda record: record["level"].no < 40  # 过滤掉 ERROR 及以上级别的日志
)

logger.add(
    error_path,
    rotation='10MB',  # 日志文件达到 10MB 时轮转
    format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}',
    encoding='utf-8',
    enqueue=True,
    diagnose=False,
    backtrace=False,
    colorize=False,
    level='ERROR'
)

logger.add(
    sink=sys.stdout,  # 输出到标准输出流
    format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}',  # 日志格式
    level='DEBUG',
    diagnose=False,
    backtrace=False,
    colorize=False,
    filter=lambda record: record["level"].no < 40,
    enqueue=True
)

logger.add(
    sink=sys.stderr,  # 输出到标准错误流
    format='{time:YYYY-MM-DD HH:mm:ss} - {level} - {message}',
    level='ERROR',
    diagnose=False,
    backtrace=False,
    colorize=False,
    enqueue=True
)