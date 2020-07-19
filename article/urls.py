from django.urls import path

from . import views
urlpatterns = [
    path("",views.homepage,name="homepage"),
     path('signup/', views.signup_view, name="signup"),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('article/',views.article,name="article"),
    path('article/<category>',views.article_category,name="article"),
    path('article/draft/',views.article_draft,name="article_draft"),
    path('article/preview/',views.article_preview,name="article_preview"), 
    path("article/preview/publish/<title>",views.preview_publish,name="preview_publish"),
    path("edit/<title>",views.preview_edit,name="preview_edit"),
    path('profile/',views.profile,name='profile'),
    path('profile/<username>/',views.profile_watch,name='profile_watch'),
    path('profile/save/me/',views.profile_save,name='profile_save'),
    path('author/follow/',views.follow,name="follow"),
    path('article-section',views.article_section,name="article_section"),
    path('article/<username>/<title>/',views.article_read,name='article_read'),
    path('article/like/',views.like,name="like"),
    path('my_article/save/',views.save_fav,name="save_fav"),
    path('article/dislike/',views.dislike,name="dislike"),
    path('delete/<title>',views.delete,name="delete"),
    path('read/author/<username>',views.read_author,name="read_author"),
  
    path('article/preview/edit/<title>/',views.editor_preview,name="editor_preview"),
    path('article/draft/title/<title>/',views.draft_version2,name="draft_version2"),
    path('dictionary/<keyword>/',views.dictionary,name="dictionary"),
    path('bookmarks/',views.my_bookmarks,name="bookmarks"),











    #----------------------AJAX----------------------
    path('subscribe/',views.subscribe,name="subscribe"),
    path('mute/',views.mute,name="mute")
]