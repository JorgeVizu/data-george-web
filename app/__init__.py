from __future__ import annotations

from flask import Flask, request, url_for
from flask_babel import Babel
from flask_mail import Mail

from config import Config

babel = Babel()
mail = Mail()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    def select_locale() -> str:
        """
        Selecciona el idioma activo.

        Prioridad:
        1. Idioma presente en la URL: /<lang>/
        2. Idioma preferido del navegador
        3. Idioma por defecto de la app
        """
        view_args = getattr(request, "view_args", None) or {}
        lang = view_args.get("lang")

        if lang in app.config["LANGUAGES"]:
            return lang

        return (
            request.accept_languages.best_match(app.config["LANGUAGES"])
            or app.config["BABEL_DEFAULT_LOCALE"]
        )

    babel.init_app(app, locale_selector=select_locale)
    mail.init_app(app)

    @app.context_processor
    def inject_i18n_helpers():
        def switch_lang_url(new_lang: str) -> str:
            """
            Devuelve la URL equivalente en otro idioma, manteniendo
            el endpoint actual y los query params cuando sea posible.
            """
            if new_lang not in app.config["LANGUAGES"]:
                new_lang = app.config["BABEL_DEFAULT_LOCALE"]

            endpoint = request.endpoint
            if not endpoint:
                return url_for("main.home", lang=new_lang)

            view_args = dict(getattr(request, "view_args", {}) or {})
            view_args["lang"] = new_lang

            query_args = dict(request.args)

            try:
                return url_for(endpoint, **view_args, **query_args)
            except Exception:
                return url_for("main.home", lang=new_lang)

        return {
            "switch_lang_url": switch_lang_url,
        }

    from .routes import bp
    app.register_blueprint(bp)

    return app