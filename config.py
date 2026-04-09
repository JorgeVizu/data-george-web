import os


class Config:
    # ==============================
    # 🔐 SEGURIDAD
    # ==============================
    SECRET_KEY = os.environ.get("SECRET_KEY")

    if not SECRET_KEY:
        raise ValueError("⚠️ SECRET_KEY no definido en variables de entorno")

    # ==============================
    # 🌍 IDIOMAS
    # ==============================
    BABEL_DEFAULT_LOCALE = "es"
    LANGUAGES = ["es", "en", "fr"]

    # ==============================
    # 📧 EMAIL (SMTP)
    # ==============================
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"

    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    if not MAIL_USERNAME or not MAIL_PASSWORD:
        raise ValueError("⚠️ MAIL_USERNAME o MAIL_PASSWORD no configurados")

    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        MAIL_USERNAME
    )

    CONTACT_RECEIVER = os.environ.get(
        "CONTACT_RECEIVER",
        MAIL_USERNAME
    )

    # ==============================
    # 📁 SUBIDA DE ARCHIVOS
    # ==============================
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB límite global

    ALLOWED_EXTENSIONS = {"csv", "xlsx", "xls"}

    # ==============================
    # ⚙️ DEBUG / ENTORNO
    # ==============================
    FLASK_ENV = os.environ.get("FLASK_ENV", "production")
    DEBUG = FLASK_ENV == "development"

    # ==============================
    # 🛡️ SEGURIDAD WEB (IMPORTANTE)
    # ==============================
    SESSION_COOKIE_SECURE = True  # solo HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

    # ==============================
    # 🧠 LOGGING (muy útil en producción)
    # ==============================
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")