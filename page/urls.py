from django.urls import path
from . import views
app_name = 'page'
urlpatterns = [
    # recipe views
    path('', views.homeview, name='homeview'),
    path('about/', views.aboutview, name='aboutview'),
]