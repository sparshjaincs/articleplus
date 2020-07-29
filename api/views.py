from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
import requests
from bs4 import BeautifulSoup
import nltk
from newspaper import Article
import datetime
import json
import re
from GoogleNews import GoogleNews
from pytrends.request import TrendReq 
# Create your views here.
def api(request):
    return render(request,'api/api.html')

def instance(url):
    try:
        article = Article(url)
        article.download()
        html = article.html
        article.parse()
        authors = article.authors
        if  article.publish_date is None:
            publish_date = " "
        else:
            publish_date = article.publish_date.strftime("%D")

        images = article.top_image
        movies = article.movies
        article.nlp()
        summary = article.summary.replace("\n"," ").replace("\t"," ")
        keywords = article.keywords
        text = article.text.replace("\n"," ").replace("\t"," ")
        urls = article.url
        title = article.title
        dictionary = dict()
        dictionary['html'] = html
        dictionary['title'] = title
        dictionary['author'] = authors
        dictionary['date'] = publish_date
        dictionary['images'] = [images]
        dictionary['movies'] = movies

        dictionary['summary'] = summary
        dictionary['text'] = text
        dictionary['keywords'] = keywords
        dictionary['urls'] = [urls]
        return dictionary
    except:
        raise serializers.ValidationError('Bad Request or Invalid URL')

def matcher(url):
    mst = r"(?i)\b((?:https?://|www\d{3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    if re.match(mst,url):
        return True
    else:
        return False
class extractor(APIView):
    def get(self,request):
            url = request.GET.get('url')
            if url is not None and matcher(url):
                dictionary = instance(url)
                data = ArticleExtractor([dictionary],many=True)
                return Response(data.data)
            else:
                content = "Invalid URL"
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
      
    def put(self):
        pass
    

def google_search(keyword,page=1):
    googlenews = GoogleNews()
    googlenews = GoogleNews(lang='en')
    googlenews.search(keyword)
    googlenews.getpage(int(page))
    data = googlenews.result()

    my_list=[]

    if data :
        for i in data[:5]:
            dictionary = dict()
            dictionary['title'] = i['title']
            dictionary['media'] = i['media']
            dictionary['link'] = i['link']
            
            article = Article(i['link'])
            article.download()
            article.parse()
            dictionary['author'] = article.authors
            dictionary['date'] = i['date']
            dictionary['movies'] = article.movies
            images = article.top_image
            dictionary['images'] = [images]
            article.nlp()
            dictionary['summary'] = article.summary.replace("\n"," ").replace("\t"," ")
            dictionary['keywords'] = article.keywords
    
            my_list.append(dictionary)
    return my_list
class article_category(APIView):
    def get(self,request):
        category = request.GET.get('keyword')
        page = request.GET.get('page')
        if page is None:
            page=1
        else:
            page = int(page)
        if category is not None:
            data = google_search(category,page)
            ins = CategoryExtractor(data,many=True)
            return Response(ins.data)
        else:
            
            content = "Invalid Category"
            return Response(content, status=status.HTTP_400_BAD_REQUEST)




def trendy(number=1):
    try:
        pytrend = TrendReq()
        df1 = pytrend.trending_searches(pn='india').values.tolist()
        if number >= len(df1):
            number = len(df1)
        elif number <=1:
            number=1
        y=[]
        for i in df1[:number]:
            d=dict()
            pytrend.build_payload(kw_list=[i[0]])
        
            df4 = pytrend.interest_by_region()
            _sum = df4.sum(axis=0, skipna = True)[i[0]]
            d['keyword'] = i[0]
            d['total_searches'] = str(_sum) + "K+ Searches"
            d['search_data'] = df4.reset_index().values.tolist() 
          
            
            y.append(d)
        return y
    except:
        raise serializers.ValidationError('Internal Server Error')
class searches(APIView):
    def get(self,request):
        number = request.GET.get('Qty')
        if number is not None:
            number = int(number)
        else:
            number =1
        
        data = trendy(number)
        ins = Trending_Searches(data,many=True)
        return Response(ins.data)
        
            
    
        