from django.urls import path
from . import views
urlpatterns = [
    path("",views.api,name="api"),
    path('extract_article/',views.extractor.as_view(),name="article_extractor"),
    path('keyword_article/',views.article_category.as_view(),name="article_category"),
    path('top_searches/',views.searches.as_view(),name="searches"),
]
