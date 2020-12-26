from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

urlpatterns = [
    path('', admin.site.urls),
    path("select2/", include("django_select2.urls")),
    url(r"^api-auth/", include("rest_framework.urls")),
    path("api/", include("accounts.urls")),
    path("api/", include("item.urls")),
    path("api/", include("item_group.urls")),
    path("api/", include("cart.urls")),
    path("api/", include("transaction.urls")),
    path("api/", include("reviews.urls")),
    path("api/", include("homepage_content.urls")),
    path("api/", include("log.urls")),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
