from django.urls import path
from . import views
urlpatterns = [
    path("",views.poetries_page,name="poetries"),
]