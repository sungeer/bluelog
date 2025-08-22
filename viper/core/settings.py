from pathlib import Path

from starlette.config import Config

from viper.utils.conf_util import ConfigDetector

CURRENT_DIR = Path(__file__).resolve()  # 当前文件 的 绝对路径
BASE_DIR = CURRENT_DIR.parent.parent.parent

config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)

if DEBUG:
    conf_dir = BASE_DIR / 'nacos-data'
    CONF = ConfigDetector(conf_dir)
else:
    CONF = ConfigDetector(
        nacos_addr=config('NACOS_ADDR'),
        namespace=config('NACOS_NAMESPACE')
    )
