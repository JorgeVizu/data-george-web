from flask_babel import lazy_gettext as _l
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileSize
from wtforms import (
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
    widgets,
)
from wtforms.validators import DataRequired, Email, Length, Optional


class MultiCheckboxField(SelectMultipleField):
    """Renderiza una lista de checkboxes en lugar de un multi-select."""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ContactForm(FlaskForm):
    nombre = StringField(
        _l("Nombre"),
        validators=[
            DataRequired(message=_l("Este campo es obligatorio.")),
            Length(max=80, message=_l("Máximo 80 caracteres.")),
        ],
        render_kw={"placeholder": _l("Tu nombre")},
    )

    empresa = StringField(
        _l("Empresa"),
        validators=[
            Optional(),
            Length(max=120, message=_l("Máximo 120 caracteres.")),
        ],
        render_kw={"placeholder": _l("Nombre de tu empresa")},
    )

    email = StringField(
        _l("Email"),
        validators=[
            DataRequired(message=_l("Este campo es obligatorio.")),
            Email(message=_l("Introduce un email válido.")),
            Length(max=120, message=_l("Máximo 120 caracteres.")),
        ],
        render_kw={"placeholder": _l("tu@email.com")},
    )

    tipo_empresa = SelectField(
        _l("Tipo de empresa"),
        choices=[
            ("", _l("Selecciona una opción")),
            ("industria", _l("Industria")),
            ("servicios", _l("Servicios")),
            ("retail", _l("Retail / Comercio")),
            ("logistica", _l("Logística")),
            ("tecnologia", _l("Tecnología")),
            ("otro", _l("Otro")),
        ],
        validators=[Optional()],
    )

    tamano_empresa = SelectField(
        _l("Tamaño de empresa"),
        choices=[
            ("", _l("Selecciona una opción")),
            ("1_10", _l("1-10 empleados")),
            ("10_50", _l("10-50 empleados")),
            ("50_plus", _l("Más de 50 empleados")),
        ],
        validators=[Optional()],
    )

    servicio = SelectField(
        _l("Servicio principal de interés"),
        choices=[
            ("", _l("Selecciona una opción")),
            ("dashboard", _l("Dashboard de negocio")),
            ("automatizacion", _l("Automatización de tareas")),
            ("procesos", _l("Análisis y mejora de procesos")),
            ("finanzas", _l("Análisis financiero y control de costes")),
            ("atencion", _l("Analítica de atención al cliente")),
            ("marketing", _l("Analítica comercial y marketing")),
            ("otro", _l("Otro / No lo tengo claro")),
        ],
        validators=[Optional()],
    )

    necesidades = MultiCheckboxField(
        _l("¿Qué necesitas?"),
        choices=[
            ("dashboard", _l("Dashboards / BI")),
            ("automatizacion", _l("Automatización")),
            ("finanzas", _l("Análisis financiero")),
            ("costes", _l("Control de costes")),
            ("marketing", _l("Marketing / publicidad")),
            ("atencion", _l("Atención al cliente")),
            ("procesos", _l("Procesos / operaciones")),
            ("otro", _l("Otro")),
        ],
        validators=[Optional()],
    )

    herramientas = MultiCheckboxField(
        _l("¿Qué herramientas utilizas actualmente?"),
        choices=[
            ("excel", _l("Excel")),
            ("erp_crm", _l("ERP / CRM")),
            ("sql", _l("SQL / Base de datos")),
            ("bi", _l("Power BI / Tableau / similar")),
            ("manual", _l("Procesos manuales")),
            ("ninguna", _l("No tengo un sistema claro")),
        ],
        validators=[Optional()],
    )

    urgencia = SelectField(
        _l("Nivel de urgencia"),
        choices=[
            ("", _l("Selecciona una opción")),
            ("explorando", _l("Solo estoy explorando opciones")),
            ("1_3_meses", _l("Quiero resolverlo en 1-3 meses")),
            ("urgente", _l("Es una necesidad urgente")),
        ],
        validators=[Optional()],
    )

    mensaje = TextAreaField(
        _l("Cuéntame tu caso"),
        validators=[
            DataRequired(message=_l("Este campo es obligatorio.")),
            Length(max=3000, message=_l("Máximo 3000 caracteres.")),
        ],
        render_kw={
            "placeholder": _l(
                "Describe brevemente qué quieres mejorar, qué problema tienes o qué tipo de ayuda estás buscando."
            )
        },
    )

    archivo = FileField(
        _l("Archivo opcional"),
        validators=[
            Optional(),
            FileAllowed(
                ["csv", "xlsx", "xls"],
                _l("Solo se permiten archivos CSV o Excel."),
            ),
            FileSize(
                max_size=10 * 1024 * 1024,
                message=_l("El archivo no puede superar 10 MB."),
            ),
        ],
    )

    submit = SubmitField(_l("Enviar solicitud"))