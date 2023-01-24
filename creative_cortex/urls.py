from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('cc-2022-admin/', admin.site.urls),
    path('', include('cc_app.urls')),
    path('baton/', include('baton.urls')),

]

handler404 = 'cc_app.views.error404'
handler500 = 'cc_app.views.error500'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)