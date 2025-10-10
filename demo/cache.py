import os
import re
import secrets
from typing import Dict, Optional

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.serving import run_simple
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from jinja2 import Environment, FileSystemLoader, select_autoescape

# -----------------------------
# In-memory storage
# -----------------------------
URL_MAP: Dict[str, str] = {}

# -----------------------------
# Configuration
# -----------------------------
HOST = "127.0.0.1"
PORT = 5000
DEBUG = True
_HOST_RE = re.compile(r"^[a-z0-9.-]+(:\d+)?$", re.IGNORECASE)

# -----------------------------
# Jinja2 setup
# -----------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


# -----------------------------
# Utilities
# -----------------------------
def is_valid_url(url: str) -> bool:
    if not url:
        return False
    parsed = url_parse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    if not parsed.netloc or not _HOST_RE.match(parsed.netloc):
        return False
    return True


def generate_short_id(length: int = 6) -> str:
    while True:
        token = secrets.token_urlsafe(8)[:length]
        if token not in URL_MAP:
            return token


def render_template(name: str, status: int = 200, **context) -> Response:
    tmpl = jinja_env.get_template(name)
    html = tmpl.render(**context)
    return Response(html, status=status, content_type="text/html; charset=utf-8")


def create_url_map() -> Map:
    return Map(
        rules=[
            Rule("/", endpoint="index", methods=["GET"]),
            Rule("/add", endpoint="create_short_link", methods=["POST"]),
            Rule("/<short_id>", endpoint="follow_short_link", methods=["GET"]),
            Rule("/<short_id>/delete", endpoint="delete_short_link", methods=["POST"]),
        ],
        strict_slashes=False,
    )


# -----------------------------
# Views
# -----------------------------
def index_view(request: Request, adapter) -> Response:
    # Build list of items for template
    items = []
    for short_id, target in sorted(URL_MAP.items()):
        items.append(
            {
                "short_id": short_id,
                "short_url": adapter.build("follow_short_link", {"short_id": short_id}),
                "delete_url": adapter.build("delete_short_link", {"short_id": short_id}),
                "target": target,
            }
        )
    return render_template(
        "index.html",
        title="Shorty",
        items=items,
        add_url=adapter.build("create_short_link"),
    )


def create_short_link_view(request: Request, adapter) -> Response:
    if request.method != "POST":
        raise MethodNotAllowed(valid_methods=["POST"])
    url = (request.form.get("url") or "").strip()
    if not is_valid_url(url):
        return render_template("error.html", title="Invalid URL", code=400,
                               message=f"{url!r} is not a valid http(s) URL.", status=400)

    # Reuse if exists
    for sid, target in URL_MAP.items():
        if target == url:
            return render_template(
                "created.html",
                title="Already exists",
                short_url=adapter.build("follow_short_link", {"short_id": sid}),
                target=url,
                back_url=adapter.build("index"),
                status=200,
            )

    short_id = generate_short_id()
    URL_MAP[short_id] = url
    return render_template(
        "created.html",
        title="Created",
        short_url=adapter.build("follow_short_link", {"short_id": short_id}),
        target=url,
        back_url=adapter.build("index"),
        status=201,
    )


def delete_short_link_view(request: Request, adapter, short_id: str) -> Response:
    if request.method != "POST":
        raise MethodNotAllowed(valid_methods=["POST"])
    if short_id in URL_MAP:
        del URL_MAP[short_id]
        return redirect(adapter.build("index"))
    raise NotFound()


def follow_short_link_view(request: Request, adapter, short_id: str) -> Response:
    target = URL_MAP.get(short_id)
    if not target:
        raise NotFound()
    return redirect(target)


def dispatch_request(request: Request, url_map: Map) -> Response:
    adapter = url_map.bind_to_environ(request.environ)
    try:
        endpoint, values = adapter.match()
        if endpoint == "index":
            return index_view(request, adapter)
        elif endpoint == "create_short_link":
            return create_short_link_view(request, adapter)
        elif endpoint == "follow_short_link":
            return follow_short_link_view(request, adapter, values.get("short_id"))
        elif endpoint == "delete_short_link":
            return delete_short_link_view(request, adapter, values.get("short_id"))
        else:
            raise NotFound()
    except HTTPException as e:
        if isinstance(e, NotFound):
            return render_template("error.html", title="Not Found", code=404,
                                   message="The requested resource was not found.", status=404)
        if isinstance(e, MethodNotAllowed):
            allow = ", ".join(e.valid_methods or [])
            return render_template("error.html", title="Method Not Allowed", code=405, message=f"Allow: {allow}",
                                   status=405)
        return e.get_response()


def application(environ, start_response):
    request = Request(environ)
    response = dispatch_request(request, application.url_map)
    return response(environ, start_response)


application.url_map = create_url_map()


def with_static(app):
    static_path = os.path.join(os.path.dirname(__file__), "static")
    if os.path.isdir(static_path):
        return SharedDataMiddleware(app, {"/static": static_path})
    return app


def main():
    app = with_static(application)
    run_simple(HOST, PORT, app, use_debugger=DEBUG, use_reloader=DEBUG)


if __name__ == "__main__":
    main()
