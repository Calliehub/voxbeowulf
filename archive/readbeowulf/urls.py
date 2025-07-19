from django.conf import settings

from django.conf.urls.static import static
from django.urls import include, path

from django.contrib import admin

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("read/lines/<int:start>-<int:end>/", views.read_lines, name="read_lines"),
    path("read/fitt/<int:fitt>/", views.read_fitt, name="read_fitt"),
    path("vocab/lines/<int:start>-<int:end>/", views.vocab_lines, name="vocab_lines"),
    path("vocab/fitt/<int:fitt>/", views.vocab_fitt, name="vocab_fitt"),
    path("lemma/<str:lemma>/", views.lemma, name="lemma"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
