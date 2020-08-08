from django.conf import settings
import django

from articleplus.settings import DATABASES, INSTALLED_APPS,STATIC_ROOT,STATIC_URL
settings.configure(DATABASES=DATABASES, INSTALLED_APPS=INSTALLED_APPS,STATIC_ROOT = STATIC_ROOT,STATIC_URL="/static/")
django.setup()

from article.models import *
from django.contrib.auth.models import User
from nltk.tokenize import word_tokenize
import nltk
from newscatcher import Newscatcher
from newspaper import Article
import string

nc = Newscatcher(website = 'nytimes.com')
results = nc.get_news()

for i in results['articles'][:30]:
    if not Articles.objects.filter(title = i['title']).exists():
        try:
            title = i['title']
            link = i['link']
            summary = i['summary']
            image = i['media_content'][0]['url']
            tags = []
            token = word_tokenize(i['title'].translate(str.maketrans(" "," ",string.punctuation)))
            tok = nltk.pos_tag(token)
    
            for i in tok:
                if i[1] in ['NN','NNP','NNS']:
                    tags.append(i[0])
            tags = ",".join(tags)
            cate = 'News' 
            article = Article(link)
            article.download()
            article.parse()
            text = article.text
            l = "/article/admin/"+title.replace(" ","_")
            ins = Articles(user_name2 = User.objects.get(username = 'admin'),title = title,author = 'admin',
            category = Categories.objects.get(category_name = cate),image2 = image,link = l, description = summary,
            content = text,tags = tags,other= link)
            ins.save()
        except:
            pass


nc = Newscatcher(website = 'moneycontrol.com')
results = nc.get_news()

for i in results['articles'][:30]:
    if not Articles.objects.filter(title = i['title']).exists():
        try:
            title = i['title']
            link = i['link']
            summary = i['summary'].split("/>")[-1]
            image = i['summary'].split('"')[1]
            tags = []
            token = word_tokenize(i['title'].translate(str.maketrans(" "," ",string.punctuation)))
            tok = nltk.pos_tag(token)
    
            for i in tok:
                if i[1] in ['NN','NNP','NNS']:
                    tags.append(i[0])
            tags = ",".join(tags)
            cate = 'Business'
            article = Article(link)
            article.download()
            article.parse()
            text = article.text
            l = "/article/admin/"+title.replace(" ","_") 
            ins = Articles(user_name2 = User.objects.get(username = 'admin'),title = title,author = 'admin',
            category = Categories.objects.get(category_name = cate),image2 = image,link = l, description = summary,
            tags = tags,content=text,other = link)
            ins.save()
        except:
            pass
            