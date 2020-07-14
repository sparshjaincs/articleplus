from django.urls import path
from . import views
urlpatterns = [
    path("",views.quotes_page,name="quotes"),
    path("editor/",views.editor,name="editor"),
]