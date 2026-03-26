from pathlib import Path

from django.utils.translation import gettext_lazy as _
import environ

from lyceum.utils import str_to_bool_allow_reverse

BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

environ.Env.read_env(PROJECT_ROOT / ".env")

SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default="fake-secret",
)

DEBUG = env.bool("DJANGO_DEBUG", default=False)

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
    default=["*"],
)

DJANGO_ALLOW_REVERSE = env.str(
    "DJANGO_ALLOW_REVERSE",
    default=None,
)

ALLOW_REVERSE = str_to_bool_allow_reverse(DJANGO_ALLOW_REVERSE)

DJANGO_MAIL = env.str("DJANGO_MAIL", default="noreply@example.com")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST", default="smtp.yandex.ru")
EMAIL_PORT = env.int("EMAIL_PORT", default=465)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=True)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")

SITE_ID = 2

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_ckeditor_5",
    "sorl.thumbnail",
    "about.apps.AboutConfig",
    "catalog.apps.CatalogConfig",
    "core.apps.CoreConfig",
    "feedback.apps.FeedbackConfig",
    "homepage.apps.HomepageConfig",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "lyceum.middleware.ReverseRussianEveryTenthMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INSTALLED_APPS += ["debug_toolbar"]
    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "lyceum.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "lyceum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation." "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]

LOCALE_PATHS = (BASE_DIR / "locale",)

LANGUAGE_CODE = "ru-RU"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static_dev",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": ["bold", "italic", "|", "alignment", "|", "undo", "redo"],
        "alignment": {"options": ["left", "center", "right"]},
        "height": "300px",
        "width": "100%",
        "language": "ru",
    },
}

CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

CKEDITOR_5_UPLOAD_FILE_VIEW_NAME = "ck_editor_5_upload_file"
