from starlette.applications import Starlette

from viper.core.errors import register_errors
from viper.core.events import register_events
from viper.core.middlewares import register_middlewares
from viper.core.routers import register_routes


app = Starlette(
    routes = register_routes,
    middleware = register_middlewares,
    exception_handlers = register_errors,
    lifespan = register_events
)
