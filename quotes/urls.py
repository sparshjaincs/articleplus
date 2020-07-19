from django.urls import path
from . import views
urlpatterns = [
    path("",views.quotes_page,name="quotes"),
    path("editor/",views.editor,name="editor"),
    path("draft/",views.draft,name="draft"),
    path("edit/<title>/",views.edit,name="edit"),
    path("draft/title/<title>/",views.edit_title,name="edit_title"),
    path('delete_quote/<id>/',views.delete,name="delete_quote"),
    path('category/<category>/',views.category,name="category"),
   
]