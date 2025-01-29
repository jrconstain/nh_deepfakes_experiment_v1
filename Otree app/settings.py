from os import environ
import dj_database_url  # Esto es necesario para gestionar la base de datos en Heroku
import os  # Necesario para usar las variables de entorno

SESSION_CONFIGS = [
    dict(
         name='app',
         app_sequence=['app'],
         num_demo_participants=1,
     ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'es-co'  # Español de Colombia
USE_L10N = True

REAL_WORLD_CURRENCY_CODE = 'COP'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = environ.get('SECRET_KEY', '5746153458085')  # Cambia esto para usar Heroku

# ===========================================
# Aquí es donde debes incluir la configuración de la base de datos y WhiteNoise
# ===========================================

# Configuración de la base de datos para Heroku
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# WhiteNoise para servir archivos estáticos (CSS, JS, etc.)
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise middleware para servir archivos estáticos
    # Tus otros middlewares irían aquí
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ===========================================
# Configura el modo de depuración (DEBUG) en Heroku
# ===========================================

DEBUG = environ.get('DEBUG', 'False') == 'True'  # Asegúrate de tener esto en producción

ALLOWED_HOSTS = ['*']  # Esto permite que tu aplicación sea accesible desde cualquier host