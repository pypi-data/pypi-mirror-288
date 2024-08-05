"""
URL configuration for django_axe project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django_axe.views import home, report, reset, store

app_name = "django_axe"

urlpatterns = (
    [
        path(route="", view=home, name="home"),
        path("django_axe/", include("django_axe.reports.urls", namespace="django_axe")),
        path(route="store/", view=store, name="store"),
        path(route="report/", view=report, name="report"),
        path(route="reset/", view=reset, name="reset"),
    ]
    + static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
