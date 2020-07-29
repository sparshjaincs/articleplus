from django.shortcuts import render
from pytrends.request import TrendReq
import datetime
from GoogleNews import GoogleNews

# Create your views here.
def trends(request):
    context = dict()
    pytrend = TrendReq()
    now = datetime.datetime.now()
    df1 = pytrend.trending_searches(pn='india').values.tolist()
    df =  df1[4:8]
    df2 = df1[:4]
    dff = df1[8:]
    z = []
    for i in dff:
        pytrend.build_payload(kw_list=[i[0]])
        df6 = pytrend.interest_by_region()
        _sum = df6.sum(axis=0, skipna = True)[i[0]]
        z.append([i,_sum])

    y=[]
    for i in df2:
       pytrend.build_payload(kw_list=[i[0]])
       df4 = pytrend.interest_by_region()
       _sum = df4.sum(axis=0, skipna = True)[i[0]]
       y.append([i,_sum,sorted(df4.reset_index().values.tolist(),key = lambda x:x[1],reverse=True)[:10]])

    x=[]
    for i in df:
        pytrend.build_payload(kw_list=[i[0]])
        df1 = pytrend.interest_by_region()
        _sum = df1.sum(axis=0, skipna = True)[i[0]]
        x.append([i,df1.reset_index().values.tolist(),_sum])
    context['df'] = x
    context['rel'] = z
    context['featured'] = y
   
    return render(request,'trends/trend.html',context)
def trending(request,keyword):
    context = {}
    keyword = keyword.replace("_"," ")
    pytrend = TrendReq()
    pytrend.build_payload(kw_list = [keyword])
    df1 = pytrend.interest_by_region()
    _sum = df1.sum(axis=0, skipna = True)[keyword]
    context['keyword'] = [keyword,df1.reset_index().values.tolist(),_sum]
    
    googlenews = GoogleNews()
    googlenews.search(keyword)
    disc = []
    for i in googlenews.result():
        if i['title'] != "":
            if not Articles.objects.filter(title = i['title']).exists():
                try:
                    title = i['title']
                    link = i['link']
                    summary = i['desc']
                    image = i['img']
                    disc1 ={
                        title1:i['title'],
                        link1 : i['link'],
                        summary1 : i['desc'],
                        image1 : i['img']
                    }
                    disc.append(disc1)
                    
                    tags = []
                    token = word_tokenize(i['title'].translate(str.maketrans(" "," ",string.punctuation)))
                    tok = nltk.pos_tag(token)
            
                    for i in tok:
                        if i[1] in ['NN','NNP','NNS']:
                            tags.append(i[0])
                    tags = ",".join(tags)
                    cate = 'News' 
                    ins = Articles(user_name2 = User.objects.get(username = 'admin'),title = title,author = 'admin',
                    category = Categories.objects.get(category_name = cate),image2 = image,link = link, description = summary,
                    tags = tags)
                    ins.save()
                except:
                    pass
    context['data'] = disc     


    return render(request,'trends/trending.html',context)