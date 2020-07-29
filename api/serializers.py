from rest_framework import serializers

class ArticleExtractor(serializers.Serializer):
    title = serializers.CharField(max_length=1000)
    author = serializers.ListField()
    date = serializers.CharField(max_length=40)
    images = serializers.ListField()
    movies = serializers.ListField()
    summary = serializers.CharField(max_length = 10000)
    text = serializers.CharField(max_length = 10000)
    keywords = serializers.ListField()
    urls = serializers.ListField()
    html = serializers.CharField(max_length=30000)


class CategoryExtractor(serializers.Serializer):
    title = serializers.CharField(max_length=1000)
    media = serializers.CharField(max_length=1000)
    author = serializers.ListField()
    date = serializers.CharField(max_length=40)
    images = serializers.ListField()
    movies = serializers.ListField()
    summary = serializers.CharField(max_length = 10000)
    keywords = serializers.ListField()
    link = serializers.CharField(max_length=1000)
 


class Trending_Searches(serializers.Serializer):
    keyword = serializers.CharField(max_length=1000)
    total_searches = serializers.CharField(max_length=1000)
    search_data = serializers.ListField()

