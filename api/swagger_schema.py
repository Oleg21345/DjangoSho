from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView
from django.urls import reverse_lazy


schema_view = get_schema_view(
    openapi.Info(
        title="Магазиник",
        default_version='v 0.0.1',
        description="Документация по API к DjangoShop",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="khasan@uzmobile.uz"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)


class SwaggerAPIDock(TemplateView):
    template_name = "swagger/swagger_ui.html"
    extra_context = {
        "schema_url": reverse_lazy('schema-json', kwargs={'format': '.json'})
    }



urlpatterns = [
    path("swagger-ui/", SwaggerAPIDock.as_view(), name="swagger-ui"),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=1),
        name='schema-json'),


]