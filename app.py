import os

from dash import Dash

from controllers.callbacks import register_callbacks
from views.layout import build_layout


def create_app() -> Dash:
    app = Dash(
        __name__,
        title="Mortalidad Colombia 2019",
        suppress_callback_exceptions=True,
    )
    app.layout = build_layout()
    register_callbacks(app)
    return app


app = create_app()
server = app.server


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8050"))
    debug = os.environ.get("DASH_DEBUG", "true").lower() == "true"
    app.run(debug=debug, host="172.0.0.1", port=port)
