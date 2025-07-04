# Ficheiro: core/settings.py

from pathlib import Path
import os
import dj_database_url  # <- 1. Importações para deploy

BASE_DIR = Path(__file__).resolve().parent.parent

# --- 2. Configurações Dinâmicas de Segurança ---
# Lê a SECRET_KEY do ambiente do servidor. Usa uma chave local insegura apenas se não encontrar.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-sua-chave-local-insegura')

# Desativa o modo DEBUG automaticamente quando estiver no Render
DEBUG = 'RENDER' not in os.environ

# --- 3. Configuração de Hosts Permitidos ---
ALLOWED_HOSTS = []
# Pega o nome do host do Render automaticamente, se existir
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # <- 4. WhiteNoise para arquivos estáticos
    'django.contrib.staticfiles',
    
    # Nossas apps
    'accounts', 'dashboard', 'products', 'users', 'categories',
    'suppliers', 'customers', 'inventory', 'sales', 'finance', 'production','logs',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <- 5. Middleware do WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'logs.middleware.RequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dashboard.context_processors.notifications_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# --- 6. Configuração de Banco de Dados Dinâmica ---
# Usa a URL do banco de dados do Render se disponível, senão usa o SQLite local.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Recife'
USE_I18N = True
USE_TZ = True

# --- 7. Configuração de Arquivos Estáticos para Produção ---
STATIC_URL = 'static/'
# Esta pasta será usada pelo comando 'collectstatic' para juntar todos os arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Habilita o WhiteNoise para servir os arquivos de forma eficiente
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Nossas Configurações Customizadas ---
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = 'accounts:login'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# --- 8. Configurações de Segurança Adicionais para Produção ---
if 'RENDER' in os.environ:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True