from django.urls import path

from . import views
urlpatterns = [ 
    path("",views.stories,name="stories"),

    path('category/<category>/',views.category,name="story_category"),
    path("text-editor/",views.text,name="stories_text"),
    path("draft/",views.stories_draft,name="stories_draft"),
    path('draft/title/<title>/',views.story_draft,name="story_draft"),
    path('preview/edit/<title>/',views.story_preview,name="story_preview"),
    path('preview/',views.preview,name="preview"),
    path("preview/publish/<title>",views.preview_publish,name="preview_publish"),
    path("edit/<title>",views.preview_edit,name="preview_edit"),
    path('like/',views.like,name='story_like'),
    path('dislike/',views.dislike,name='story_dislike'),
    path('saving/',views.save_fav,name='story_save'),
    path('delete_story/<title>/',views.delete,name='delete'),
    path('<username>/<title>/',views.stories_read,name='story_read'),
    
]