import asyncio


async def stream_data():
    for i in range(5):
        await asyncio.sleep(1)
        yield {'progress': i * 20, 'info': f'step {i}'}
    yield {'progress': '', 'info': 'finish'}
