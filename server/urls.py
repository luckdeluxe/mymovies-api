from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from films import views as film_views

#Api Router
router = routers.DefaultRouter()
router.register('films', film_views.FilmViewSet, basename='Film')
router.register('genres', film_views.GenreViewSet, basename='FilmGenre')

urlpatterns = [
    #Admin Routes
    path('admin/', admin.site.urls),

    #Api routes
    path('api/', include('authentication.urls')),
    path('api/', include(router.urls)),
] 

# Serve static files in development server
if settings.DEBUG:
    urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)
