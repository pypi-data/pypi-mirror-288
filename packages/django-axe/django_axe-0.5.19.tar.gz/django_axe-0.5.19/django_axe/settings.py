import os
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-y9e0ymlzg6fnuaowm5m_to)@euvh-r%3hlwh+x1zh%w^i+8e_j"
DEBUG = os.environ.get("DEBUG", True)
ALLOWED_HOSTS = ["0.0.0.0", "localhost"]
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django_axe.apps.DjangoAxeConfig",
]
MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]
ROOT_URLCONF = "django_axe.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "django_axe", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
            ],
        },
    },
]
WSGI_APPLICATION = "django_axe.wsgi.application"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "django_axe", "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "django_axe", "media")
DJANGO_AXE_REPORT_PATH = os.path.join(MEDIA_ROOT, "django_axe_report.json")
DJANGO_AXE_APP_NAMESPACE = ""
DJANGO_AXE_ENABLED = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[{levelname}] [{asctime}] [{module}] [{filename}:{lineno}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "simple",
        },
    },
    "loggers": {
        "django_axe": {
            "handlers": ["console"],
            "propagate": True,
        },
    },
}

DJANGO_AXE_APP_TAGS = {
    "wcag2a": "WCAG 2.0 Level A",
    "wcag2aa": "WCAG 2.0 Level AA",
    "wcag2aaa": "WCAG 2.0 Level AAA",
    "wcag21a": "WCAG 2.1 Level A",
    "wcag21aa": "WCAG 2.1 Level AA",
    "wcag22aa": "WCAG 2.2 Level AA",
    "best-practice": "Common accessibility best practices",
    "wcag2a-obsolete": "WCAG 2.0 Level A, no longer required for conformance",
    "wcag": "WCAG success criterion e.g. wcag111 maps to SC 1.1.1",
    "ACT W3C": "approved Accessibility Conformance Testing rules",
    "section508": "Old Section 508 rules",
    "section508.*.*": "Requirement in old Section 508",
    "TTv5": "Trusted Tester v5 rules",
    "TT": "Test ID in Trusted Tester",
    "EN-301-549": "Rule required under EN 301 549",
    "EN-9": "Section in EN 301 549 listing the requirement",
    "experimental": "Cutting-edge rules, disabled by default",
    "cat": "Category mappings used by Deque (see below)",
}
