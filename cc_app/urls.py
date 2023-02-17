from django.urls import path

from . import views

# path('404error/', views.Error_404, name="error_404"),
# path('500error/', views.Error_500, name="error_500"),

urlpatterns = [
	path('', views.Landing_Page, name="landing_page"),
	path('comics/', views.Comics, name="comics"),
	path('comics/<slug:comic_param>/', views.Comic_Detail, name="comic-detail"),
	path('comics/<slug:comic_param>/vol=<int:volume_param>&cha=<int:chapter_param>&page=<int:page_param>/', views.Pages, name="pages"),
	path('links/', views.Links, name="links"),
	path('about-us/', views.About_Us, name="about_us"),
	path('gallery/', views.Gallery, name="gallery"),
]
