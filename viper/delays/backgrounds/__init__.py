from viper.utils.pools import run_in_thread_pool_delay
from viper.delays.backgrounds import long_task


async def delay_long_task(data):
    await run_in_thread_pool_delay(long_task.long_task, data)
