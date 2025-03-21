from django.urls import path
from . import views
app_name = 'page'
urlpatterns = [
    # recipe views
    path('', views.page_story_home, name='page_story_home'),
    path('about/', views.page_story_about, name='page_story_about'),
]