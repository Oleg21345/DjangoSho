from django.contrib import admin
from django.urls import path, include
from conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from api.swagger_schema import urlpatterns as url_swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('api/', include("api.urls")),
    path("i18n/", include("django.conf.urls.i18n"))
]

urlpatterns += url_swagger

urlpatterns += i18n_patterns(
    path("", include("shop.urls"))
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
