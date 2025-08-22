import time

from viper.delays.log_config import logger
from viper.delays.huey_instance import huey


@huey.task()
def long_task(data: str):
    logger.info('Starting long-running task...')
    time.sleep(5)
    logger.info('Long-running task completed!')
    return f'Processed data: {data}'
