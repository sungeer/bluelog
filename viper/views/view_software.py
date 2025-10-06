from viper.cores.core_http import jsonify
from viper.models.model_software import SoftwareModel
from viper.cores.core_log import logger


def get_softwares(request):
    softwares = SoftwareModel().get_softwares()
    return jsonify(softwares)


urls = {
    '/api/get_softwares': get_softwares,
}
