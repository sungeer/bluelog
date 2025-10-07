from viper.cores.core_http import jsonify
from viper.models.model_software import BlessModel
from viper.cores.core_log import logger
from viper.cores.core_before import require_post


@require_post
def get_blesses(request):
    softwares = BlessModel().get_blesses()
    return jsonify(softwares)


urls = {
    '/api/get_softwares': get_blesses,
}
