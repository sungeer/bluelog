from huey import crontab

from viper.delays.log_config import logger
from viper.delays.huey_instance import huey


@huey.periodic_task(crontab(minute='0', hour='3'))  # 每天凌晨3点执行
def scheduled_task():
    logger.info('Scheduled task running...')


@huey.periodic_task(crontab())  # 每分钟执行
def every_minute_task():
    logger.info('Task running every minute...')
