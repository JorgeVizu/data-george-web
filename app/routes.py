from __future__ import annotations

import mimetypes
from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_babel import _
from flask_mail import Message
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from . import mail
from .forms import ContactForm

bp = Blueprint("main", __name__)

SUPPORTED_LANGUAGES = ("es", "en", "fr")


def safe_lang(lang: str | None) -> str:
    """Devuelve un idioma soportado o 'es' por defecto."""
    if lang in SUPPORTED_LANGUAGES:
        return lang
    return "es"


def get_best_lang() -> str:
    """Detecta el mejor idioma según el navegador."""
    return request.accept_languages.best_match(SUPPORTED_LANGUAGES) or "es"


def get_upload_dir() -> Path:
    """Obtiene y crea el directorio de subida si no existe."""
    upload_dir = Path(current_app.config.get("UPLOAD_FOLDER", "uploads"))
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def save_uploaded_file(file: FileStorage | None) -> tuple[Path | None, str | None]:
    """Guarda un archivo subido de forma segura y devuelve ruta + nombre."""
    if not file or not file.filename:
        return None, None

    safe_name = secure_filename(file.filename)
    if not safe_name:
        return None, None

    upload_dir = get_upload_dir()
    file_path = upload_dir / safe_name
    file.save(file_path)

    return file_path, safe_name


def build_contact_email_body(form: ContactForm, saved_filename: str | None) -> str:
    """Construye el cuerpo del email recibido desde el formulario."""
    necesidades = ", ".join(form.necesidades.data) if form.necesidades.data else "No especificado"
    herramientas = ", ".join(form.herramientas.data) if form.herramientas.data else "No especificado"

    return f"""
Nuevo contacto desde la web de DATA GEORGE

Nombre: {form.nombre.data}
Empresa: {form.empresa.data or 'No especificada'}
Email: {form.email.data}
Tipo de empresa: {form.tipo_empresa.data or 'No especificado'}
Tamaño de empresa: {form.tamano_empresa.data or 'No especificado'}
Servicio principal: {form.servicio.data or 'No especificado'}
Necesidades: {necesidades}
Herramientas actuales: {herramientas}
Urgencia: {form.urgencia.data or 'No especificada'}

Mensaje:
{form.mensaje.data}

Archivo adjunto:
{saved_filename or 'No adjunto'}
""".strip()


def attach_file_to_message(msg: Message, file_path: Path | None, filename: str | None) -> None:
    """Adjunta un archivo al mensaje si existe."""
    if not file_path or not filename or not file_path.exists():
        return

    mime_type, _ = mimetypes.guess_type(filename)
    mime_type = mime_type or "application/octet-stream"

    with file_path.open("rb") as f:
        msg.attach(
            filename=filename,
            content_type=mime_type,
            data=f.read(),
        )


@bp.get("/")
def root():
    return redirect(url_for("main.home", lang=get_best_lang()))


@bp.get("/<lang>/")
def home(lang: str):
    lang = safe_lang(lang)
    return render_template("home.html", lang=lang)


@bp.get("/<lang>/servicios")
def servicios(lang: str):
    lang = safe_lang(lang)
    return render_template("servicios.html", lang=lang)


@bp.get("/<lang>/proyectos")
def proyectos(lang: str):
    lang = safe_lang(lang)
    return render_template("proyectos.html", lang=lang)


@bp.get("/<lang>/sobre-mi")
def sobre_mi(lang: str):
    lang = safe_lang(lang)
    return render_template("sobre_mi.html", lang=lang)


@bp.route("/<lang>/contacto", methods=["GET", "POST"])
def contacto(lang: str):
    lang = safe_lang(lang)
    form = ContactForm()

    if form.validate_on_submit():
        saved_filepath, saved_filename = save_uploaded_file(form.archivo.data)

        subject = f"Nuevo lead desde DATA GEORGE - {form.nombre.data}"
        body = build_contact_email_body(form, saved_filename)

        msg = Message(
            subject=subject,
            recipients=[current_app.config["CONTACT_RECEIVER"]],
            body=body,
            reply_to=form.email.data,
        )

        attach_file_to_message(msg, saved_filepath, saved_filename)

        try:
            mail.send(msg)
            flash(
                _("¡Gracias! He recibido tu mensaje y te responderé lo antes posible."),
                "success",
            )
            return redirect(url_for("main.thanks", lang=lang))

        except Exception:
            current_app.logger.exception("Error enviando email de contacto")
            flash(
                _("Ha ocurrido un problema al enviar el formulario. Inténtalo de nuevo en unos minutos."),
                "danger",
            )

    return render_template("contacto.html", lang=lang, form=form)


@bp.get("/<lang>/thanks")
def thanks(lang: str):
    lang = safe_lang(lang)
    return render_template("thanks.html", lang=lang)