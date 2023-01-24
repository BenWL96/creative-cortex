from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500
from cc_app import views

urlpatterns = [
    path('cc-2022-admin/', admin.site.urls),
    path('', include('cc_app.urls')),
    path('baton/', include('baton.urls')),

]

handler404 = views.error_404
handler500 = views.error_500

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)