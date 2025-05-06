from django.urls import path
from .views import PredictView

app_name = 'api'
urlpatterns = [
    path("predict/", PredictView.as_view(), name="predict"),
]
