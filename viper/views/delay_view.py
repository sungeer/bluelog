from viper.utils.resp_util import jsonify
from viper.delays.backgrounds import delay_long_task
from viper.delays.huey_instance import huey


async def start_task(request):
    data = await request.json()
    input_data = data.get('input', 'default')
    task = await delay_long_task(input_data)
    message = {'status': 'task started', 'task_id': task.id}
    return jsonify(message)


async def check_task_status(request):
    # task_id = request.path_params['task_id']  # get method /task-status/{task_id}
    data = await request.json()
    task_id = data['task_id']
    result = huey.result(task_id)
    if result is None:
        return jsonify({'status': 'pending or failed'})
    return jsonify({'status': 'completed', 'result': result})
