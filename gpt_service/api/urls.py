from django.urls import path

from api import views

urlpatterns = [
    path("request/", views.MakeRequestApi.as_view())
]
