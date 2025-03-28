from django.urls import path
from . import views
app_name = 'page'
urlpatterns = [
    # recipe views
    path('', views.homeview, name='homeview'),
    path('about/', views.aboutview, name='aboutview'),
    path('product/', views.productview, name='productview'),
    path('upload/', views.uploadview, name='uploadview'),
    path('faq/', views.faqview, name='faqview'),
    path('privacypolicy/', views.privacypolicyview, name='privacypolicyview'),
    path('contact/', views.contactview, name='contactview'),
    path('logout', views.logout, name='logout'),
    path('login/', views.login, name='login'),
]