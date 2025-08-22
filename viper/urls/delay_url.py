from starlette.routing import Router

from viper.views import delay_view

delay_url = Router()

delay_url.add_route('/start-task', delay_view.start_task, ['POST'])
delay_url.add_route('/task-status', delay_view.check_task_status, ['POST'])
