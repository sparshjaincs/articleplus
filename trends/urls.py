from django.urls import path
from . import views
urlpatterns = [
    path("",views.trends,name="trends"),
    path("<keyword>/",views.trending,name="trending")
]