from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView
from .forms import SignUpForm,Article_form
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
import json
import threading
from bs4 import BeautifulSoup
import html5lib
import urllib.request
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from nltk.corpus import wordnet
from hitcount.views import HitCountDetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile,Articles,my_comment,Categories,Notifications,activity,titleview
from .forms import ProfileForm,CommentForm
from django.db.models import Count
from PyDictionary import PyDictionary
from py_thesaurus import Thesaurus
from stories.models import Stories
from quotes.models import Quotes

# Create your views here.
def homepage(request):
    context={} 
    if request.user.is_authenticated:
        if not Notifications.objects.filter(user_name4 = request.user).exists():
            notify = Notifications(user_name4 = request.user)
            notify.save()

        context['article'] = Articles.objects.filter(user_name2 = request.user).order_by('-date_Publish',"-time")
        context['article_count'] = [Articles.objects.filter(user_name2 = request.user,status="Draft").all().count(),Articles.objects.filter(user_name2 = request.user,status="published").count()]
        context['story_count'] = [Stories.objects.filter(user_stories = request.user,status="Draft").count(),Stories.objects.filter(user_stories = request.user,status="published").count()]
        context['quotes_count'] = [Quotes.objects.filter(user_quotes = request.user,status="Draft").count(),Quotes.objects.filter(user_quotes = request.user,status="published").count()]
        context['stories'] = Stories.objects.filter(user_stories = request.user).order_by('-date_Publish',"-time")
        context['quotes'] = Quotes.objects.filter(user_quotes = request.user).order_by('-date_Publish',"-time")
        if activity.objects.filter(user_name3 = request.user,user_activity = f'User successfully logged-in !!',activity_icon='fas fa-door-open').exists():
            pass
        else:
            activity.objects.filter(user_name3 = request.user,user_activity = f'User successfully logged-in !!',activity_icon='fas fa-door-open').delete()
            act = activity(user_name3 = request.user,user_activity = f'User successfully logged-in !!',activity_icon='fas fa-door-open')
            act.save()
        return render(request,'article/dashboard.html',context)
    context['top'] = Articles.objects.all().order_by('-date_Publish',"-time")[3:9]
    return render(request,'article/homepage.html',context)

def signup_view(request):
    if request.method  == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            email = form.cleaned_data.get('email')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            current_site = request.get_host()
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('article/activation_request.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject,message,'articleplusceo@gmail.com',[f'{email}'])
            return redirect('activation_sent') 
    else:
        form = SignUpForm()
    return render(request, 'article/signup.html', {'sform': form})


class MyPasswordResetView(UserPassesTestMixin, PasswordResetView):
    template_name = 'users/password_reset.html' 

    # https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User.is_anonymous
    def test_func(self):
        return self.request.user.is_anonymous
def activation_sent_view(request):
    return render(request, 'article/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.profile.first_name = user.first_name
        user.profile.last_name = user.last_name
        user.profile.email = user.email
        user.save()
        
        
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        

        return redirect('homepage')
    else:
        return render(request, 'article/activation_invalid.html')



def article(request):
    context = {}
    method = request.GET.get('method')
    if method == 'text_editor':
        if request.method == 'POST':
            
            form = Article_form(request.POST,request.FILES)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.user_name2 = request.user
                ins.author = request.user
                title = form.cleaned_data['title'].replace(" ","_")
                content = form.cleaned_data['content'].split(".")[0].strip("<p>")
                ins.link = f'/article/{request.user}/{title}'
                ins.description = content
                
                ins.save()
                messages.success(request,f'You Article is published.')
            else:
                context['errors'] = str(form.errors)
        else:
            form = Article_form()



        context['article_form'] = form
        
        return render(request,'article/article_text_editor.html',context)
    else:
        context['category'] = Categories.objects.all()
        return render(request,'article/article_web_editor.html',context)
def webeditor(request):
    if request.method == 'POST':
        html = request.POST.get('html')
        css = "<style> "+ request.POST.get('css') + "</style>"
        path = f'/articleplus/media/{request.user}'
        title = request.POST.get('title')
        header = "_".join(title.split(" "))
        if Articles.objects.filter(title=title).exists():
            return HttpResponse(f'{title} already exists !!')
        else:
            try:
                os.mkdir(path)

            except Exception as exp:
                pass
            path2=f"/articleplus/media/{request.user}/{header}.html"
        
            fp = open(path2,"w+")
            data = css+html
            fp.write(data)
            fp.close()
            link = f'/article/{request.user}/{title.replace(" ","_")}'
            image = request.FILES['image']
            tags = request.POST.get('tags')
            category = request.POST.get('category')
            ref = Articles(user_name2 = request.user ,title=title,
            category = Categories.objects.get(category_name=category),tags=tags,
            image = image,link = link,method = 'editor',template = f'{header}.html')
            ref.save()
    return HttpResponseRedirect('/')
            

def article_draft(request):
    context={}
    if request.method == 'POST':
            
            form = Article_form(request.POST,request.FILES)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.user_name2 = request.user
                ins.author = request.user
                title = form.cleaned_data['title'].replace(" ","_")
                ins.link = f'/article/{request.user}/{title}'
                ins.status = 'Draft'
                ins.save()
                messages.success(request,f'Your Article is saved as Draft!')
            else:
                context['errors'] = str(form.errors)
    else:
            form = Article_form()
    return HttpResponseRedirect('/')

def article_preview(request):
    context = {}
    tit = request.GET.get('title')
    
    if request.method == 'POST':
            
            form = Article_form(request.POST,request.FILES)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.user_name2 = request.user
                ins.author = request.user
                title = form.cleaned_data['title'].replace(" ","_")
                ins.link = f'/article/{request.user}/{title}'
                ins.status = 'Draft'
                ins.save()
                context['title'] = title
                context['message'] =ins.link
                

            else:
                tit= request.POST.get('title')
                data_ins = Articles.objects.get(title = tit.replace("_"," "))
                context['title'] = tit
                context['message'] =data_ins.link
                


    else:
            form = Article_form()


    context['edit'] = True
    return render(request,'article/preview.html',context) 


def preview_publish(request,title):
    ins = Articles.objects.get(title = title.replace("_"," "))
    ins.status = 'published'
    ins.save()
    messages.success(request,'Your article is published!')
    return HttpResponseRedirect('/')
    
def preview_edit(request,title):
    context = {}
    if request.method == 'POST':
            
            form = Article_form(request.POST,request.FILES)
         
               
            tit = request.POST.get('title')
            ins = Articles.objects.get(title=title.replace("_"," "))
            ins.status = 'published'
            ins.title = tit
            if request.FILES.get('image') is not None:
                ins.image = request.FILES.get('image')
            if request.FILES.get('video') is not None:
                ins.video = request.FILES.get('video')
            ins.category = Categories.objects.get(category_name = request.POST.get('category'))
            ins.content = request.POST.get('content')
            ins.description = request.POST.get('content').split(".")[0]
            ins.link = f'/article/{request.user}/{tit.replace(" ","_")}'
            ins.tags = request.POST.get('tags')
            ins.facebook = request.POST.get('facebook')
            ins.twitter = request.POST.get('twitter')
            ins.quora = request.POST.get('quora')
            ins.instagram = request.POST.get('instagram')
            ins.medium = request.POST.get('medium')
            ins.other = request.POST.get('other')
            
            ins.save()
            messages.success(request,f'You Article is published.')
            return HttpResponseRedirect('/')
           
    else:   
           
            ins = Articles.objects.filter(title = title.replace("_"," ")).first()
            initial = {
                "title":ins.title,
                "image":ins.image,
                "category":ins.category,
                "tags":ins.tags,
                "content":ins.content,
                "video":ins.video,
                "facebook":ins.facebook,
                "twitter":ins.twitter,
                "quora":ins.quora,
                "instagram":ins.instagram,
                "medium":ins.medium,
                "other":ins.other
            }

            form = Article_form(initial=initial)

    context['title'] = title
    context['edit'] = True
    context['article_form'] = form
    
    return render(request,'article/article_text_editor.html',context)

def editor_preview(request,title):
    context = {}
    
    if request.method == 'POST':
            
            form = Article_form(request.POST,request.FILES)
            tit = request.POST.get('title')
            ins = Articles.objects.get(title=title.replace("_"," "))
            ins.status = 'Draft'
            ins.title = tit
            if request.FILES.get('image') is not None:
                ins.image = request.FILES.get('image')
            if request.FILES.get('video') is not None:
                ins.video = request.FILES.get('video')
            ins.category = Categories.objects.get(category_name = request.POST.get('category'))
            ins.content = request.POST.get('content')
            ins.description = request.POST.get('content').split(".")[0]
            ins.link = f'/article/{request.user}/{tit.replace(" ","_")}'
            ins.tags = request.POST.get('tags')
            ins.facebook = request.POST.get('facebook')
            ins.twitter = request.POST.get('twitter')
            ins.quora = request.POST.get('quora')
            ins.instagram = request.POST.get('instagram')
            ins.medium = request.POST.get('medium')
            ins.other = request.POST.get('other')
            
            ins.save()
            context['title'] = tit
            context['message'] =ins.link

                


    else:
            form = Article_form()
    return render(request,'article/preview.html',context) 
def draft_version2(request,title):
    context = {}
    
    if request.method == 'POST':
            
            form = Article_form(request.POST,request.FILES)
            tit = request.POST.get('title')
            ins = Articles.objects.get(title=title.replace("_"," "))
            ins.status = 'Draft'
            ins.title = tit
            if request.FILES.get('image') is not None:
                ins.image = request.FILES.get('image')
            if request.FILES.get('video') is not None:
                ins.video = request.FILES.get('video')
            ins.category = Categories.objects.get(category_name = request.POST.get('category'))
            ins.content = request.POST.get('content')
            ins.description = request.POST.get('content').split(".")[0]
            ins.link = f'/article/{request.user}/{tit.replace(" ","_")}'
            ins.tags = request.POST.get('tags')
            ins.facebook = request.POST.get('facebook')
            ins.twitter = request.POST.get('twitter')
            ins.quora = request.POST.get('quora')
            ins.instagram = request.POST.get('instagram')
            ins.medium = request.POST.get('medium')
            ins.other = request.POST.get('other')
            
            ins.save()
            messages.success(request,'Your article is saved as Draft!')
           

                


    else:
            form = Article_form()
    return HttpResponseRedirect('/')
def profile(request):
    context = {}
    profile_ins = Profile.objects.get(user = request.user)
    context['profile'] = profile_ins 
    context['articles'] = Articles.objects.filter(user_name2 = request.user).order_by('-date_Publish','-time')
    initial = {
        "first_name":profile_ins.first_name,
        "last_name":profile_ins.last_name,
        "email":profile_ins.email,
        "phone_number":profile_ins.phone_number,
        "avatar":profile_ins.avatar,
        "bio":profile_ins.bio,
        "address":profile_ins.address,
        "city":profile_ins.city,
        "state":profile_ins.state,
        "country":profile_ins.country,
        "date_of_birth":profile_ins.date_of_birth,
        "quora":profile_ins.quora,
        "medium":profile_ins.medium,
        "other":profile_ins.other
    }
    context['p_form'] = ProfileForm(initial=initial)
    leader = Articles.objects.all().annotate(num_li = Count('liked'),num_dis = Count('disliked')).order_by('-num_li','num_dis')
    
    leader_data=[]
    for i in leader:
        if i.user_name2.profile in leader_data:
            continue
        else:
            leader_data.append(i.user_name2.profile) 
    lead_data=[]
    for i in leader_data:
        tot_post =Articles.objects.filter(user_name2 = i.user,status="published").count()
        lead_data.append((i,tot_post))
    
    context['leaderboard'] = lead_data
    if request.user in leader_data:
        my_rank = leader_data.index(request.user)+1

    else:
        my_rank = len(leader_data)+1
    context['my_rank'] = my_rank
    suggestions = []
    for i in profile_ins.follow.all():
       for j in i.profile.follow.all() :
           if j.profile not in suggestions and j not in profile_ins.follow.all()  and j.username != request.user.username:

               suggestions.append(j.profile)
    for i in User.objects.all():
        
        if i not in profile_ins.follow.all() and i not in profile_ins.following.all() and i.username != request.user.username:
            if i.profile not in suggestions:
                suggestions.append(i.profile)
    act_data = activity.objects.filter(user_name3 = request.user).order_by('-date_activity','-activity_time')
    context['activity'] = act_data
    context['suggestion'] = suggestions
    context['stories'] = Stories.objects.all().order_by('-date_Publish','-time')
    if Notifications.objects.filter(user_name4 = request.user).exists():
            notify = Notifications.objects.get(user_name4 = request.user)
            activity_c,follow_c,following_c = notify.activity_profile_count,notify.follow_count,notify.following_count
            original_act_count = act_data.count()
            original_foll_count = profile_ins.follow.count()
            original_following_count = profile_ins.following.count()
            notify.activity_profile_count = original_act_count
            notify.follow_count = original_foll_count
            notify.following_count = original_following_count
            notify.save()
            d_a_c = original_act_count - activity_c
            f_a_c = original_foll_count - follow_c
            fi_a_c = original_following_count - following_c
            act_status = (False,) if d_a_c <= 0 else (True,d_a_c)
            follow_status = (False,) if f_a_c <= 0 else  (True,f_a_c)
            following_status = (False,) if fi_a_c <= 0 else  (True,fi_a_c)
    else:
            act_status = (False,)
            follow_status = (False,)
            following_status = (False,)
    context['act1_status'] = act_status
    context['follow1_status'] = follow_status
    context['following1_status'] = following_status
    return render(request,'article/profile.html',context)

def profile_save(request):
    if request.method == 'POST':
        p_form = ProfileForm(request.POST,request.FILES)
        if p_form.is_valid():
            dp = Profile.objects.get(user=request.user)
            dp.bio = p_form.cleaned_data['bio']
            dp.first_name = p_form.cleaned_data['first_name']
            dp.last_name = p_form.cleaned_data['last_name']
            dp.email = p_form.cleaned_data['email']
            dp.phone_number = p_form.cleaned_data['phone_number']
            dp.address = p_form.cleaned_data['address']
            dp.city = p_form.cleaned_data['city']
            dp.state = p_form.cleaned_data['state']
            dp.country = p_form.cleaned_data['country']
            dp.date_of_birth = p_form.cleaned_data['date_of_birth']
            dp.avatar = p_form.cleaned_data['avatar']
            dp.quora = p_form.cleaned_data['quora']
            dp.medium = p_form.cleaned_data['medium']
            dp.other = p_form.cleaned_data['other']
            dp.save() 
            ds= User.objects.get(username = request.user)
            ds.first_name = p_form.cleaned_data['first_name']
            ds.last_name = p_form.cleaned_data['last_name']
            ds.email = p_form.cleaned_data['email']
            ds.save()
            
    return HttpResponseRedirect('/profile')
def like(request):
    user = request.user
    
    title = request.GET.get('title').replace("_"," ")
   
    post_obj = Articles.objects.get(title = title)
    dislikes_count = post_obj.disliked.count()
  
    if user in post_obj.liked.all():
        post_obj.liked.remove(user)
        likes = True
        count = post_obj.liked.count()
        

    else:
        post_obj.liked.add(user)
        activity_title=f"You liked Article with title {title} !!"
        activity_icon = 'fa fa-thumbs-up'
        likes = False
        count = post_obj.liked.count()
        

        
        if user in post_obj.disliked.all():
            post_obj.disliked.remove(user)
            dislikes_count = post_obj.disliked.count()
            
      

    
    return HttpResponse(json.dumps([likes,count,dislikes_count]))

def dislike(request):
    user = request.user
    
    title = request.GET.get('title').replace("_"," ")
  
    post_obj = Articles.objects.get(title = title)
    likes_count = post_obj.liked.count()
    if user in post_obj.disliked.all():
        post_obj.disliked.remove(user)
        dislikes = True
        count = post_obj.disliked.count()
    else:
        post_obj.disliked.add(user)
        activity_title=f"You disliked Article with title {title} !!"
        activity_icon = 'fa fa-thumbs-down'
        act = activity(user_name3 = request.user,user_activity = activity_title,activity_icon=activity_icon)
        act.save()
        dislikes = False
        count = post_obj.disliked.count()
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
            likes_count = post_obj.liked.count()
    
    return HttpResponse(json.dumps([dislikes,count,likes_count]))
def follow(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title')
        user_name = request.POST.get('user_name')
        user_name_ins = User.objects.get(username = user_name)
        user_name = user_name_ins.username
        
        foll = Profile.objects.get(user = user)
        folli = Profile.objects.get(user = user_name_ins)
        if user_name_ins in foll.follow.all():
            foll.follow.remove(user_name_ins)
            followed = False
        else:
            foll.follow.add(user_name_ins)
            followed=True

        if user in folli.following.all():
            folli.following.remove(user)
        else:
            folli.following.add(user)
    return HttpResponseRedirect(title)


def article_section(request):
    context = {}
    art = Articles.objects.filter(status = "published").order_by('-date_Publish','-time')
 
    context['articles'] =art
   
    context['category'] = Categories.objects.all().order_by('category_name')
    context['users'] = User.objects.all().order_by('first_name')
    return render(request,'article/article.html',context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

 
def article_read(request,username,title):
    context={}
    post = get_object_or_404(Articles, title = title.replace("_"," "))
    comments = post.my_comments.filter(active=True,parent=None)
    ip_addr = get_client_ip(request)
   
    if not post.titleview.filter(ip_addr=ip_addr).exists():
        print(ip_addr)
        ins = titleview(view=post,ip_addr = ip_addr)
        ins.save()
    if request.method == 'POST':
       
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = my_comment.objects.get(id = parent_id)
                if parent_obj:
                    reply_comment = comment_form.save(commit=False)
                    reply_comment.parent = parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            name = comment_form.cleaned_data['name']
            
           
            new_comment.post.user_name2
    else:
        comment_form = CommentForm()
    context['form'] = comment_form
    tag = post.tags.split(",")
    related_stories = []
    data = Articles.objects.filter(status='published').order_by('-date_Publish','-time')
    for i in data:
        if i.title != post.title: 
            if len(related_stories) <=5:
                df = i.tags.split(",")
                for j in tag:
                    if j in df:
                        
                        related_stories.append(i)
                        break
                        
            else:
                break
    trending = []
    for i in data:
        if i not in related_stories and len(trending) <=5:
            trending.append(i)


    context['related_stories'] = related_stories
    context['comments'] = comments
    context['read']=[post]
    context['article_trend'] = trending
    context['tags'] = tag
    context['template'] = post.template
    return render(request,'article/article_read.html',context)


def save_fav(request):
    user = request.user
    title = request.GET.get('title').replace("_"," ")
    ids = request.GET.get('id')
    tit_ins = Articles.objects.get(title = title)
    prof_ins = Profile.objects.get(user = user)
      
    if tit_ins in prof_ins.favourities.all():
            prof_ins.favourities.remove(tit_ins)
            key = True
    else:
            prof_ins.favourities.add(tit_ins)
            key = False
        

        
        
    return HttpResponse(json.dumps([key,ids]))

def profile_watch(request,username):
    context={}
    profile_ins = Profile.objects.get(user = User.objects.get(username = username))
    context['profile'] = profile_ins 
    context['articles'] = Articles.objects.filter(user_name2 = User.objects.get(username = username)).order_by('-date_Publish','-time')
    initial = {
        "first_name":profile_ins.first_name,
        "last_name":profile_ins.last_name,
        "email":profile_ins.email,
        "phone_number":profile_ins.phone_number,
        "avatar":profile_ins.avatar,
        "bio":profile_ins.bio,
        "address":profile_ins.address,
        "city":profile_ins.city,
        "state":profile_ins.state,
        "country":profile_ins.country,
        "date_of_birth":profile_ins.date_of_birth,
        "quora":profile_ins.quora,
        "medium":profile_ins.medium,
        "other":profile_ins.other
    }
    context['p_form'] = ProfileForm(initial=initial)
    leader = Articles.objects.all().annotate(num_li = Count('liked'),num_dis = Count('disliked')).order_by('-num_li','num_dis')
    
    leader_data=[]
    for i in leader:
        if i.user_name2.profile in leader_data:
            continue
        else:
            leader_data.append(i.user_name2.profile) 
    lead_data=[]
    for i in leader_data:
        tot_post =Articles.objects.filter(user_name2 = i.user,status="published").count()
        lead_data.append((i,tot_post))
    
    context['leaderboard'] = lead_data
    context['watch'] = True
    
    return render(request,'article/profile.html',context)

def article_category(request,category):
    context={}
    context['name'] = category
    try:
        context['article']=Articles.objects.filter(category = Categories.objects.get(category_name = category)).order_by('-date_Publish','-time')
    except:
        context['message'] = "Something is wrong try again in some time !!"
    context['category'] = Categories.objects.all().order_by('category_name')
    context['users'] = User.objects.all().order_by('first_name')
    return render(request,'article/category.html',context)

def delete(request,title):
    context={}
    if Articles.objects.filter(title=title.replace("_"," ")).exists():
        Articles.objects.get(title=title.replace("_"," ")).delete()
    messages.success(request,f'You Successfully deleted Article with title {title.replace("_"," ")}')
    return HttpResponseRedirect('/')

def read_author(request,username):
    context=dict()
    user_ins =  User.objects.get(username = username)
    context['users'] = User.objects.all()
    context['profile'] = Profile.objects.get(user= user_ins)
    context['stories'] = Stories.objects.filter(user_stories = user_ins,status = "published").order_by('-date_Publish','-time')
    context['title']  = Articles.objects.filter(user_name2 = user_ins,status="published").order_by('-date_Publish','-time')
    
    return render(request,'article/read_author.html',context)

def dictionary(request,keyword):
    le = wordnet.synsets(keyword)
    synonyms = []
    antonyms = []
    defination = examples = ""
    for syn in le:
        for l in syn.lemmas(): 
            synonyms.append(l.name()) 
            if l.antonyms(): 
                antonyms.append(l.antonyms()[0].name()) 
    try:
        defination =le[0].definition()
        examples = le[0].examples()
    except:
        meaning = "No Meaning Found"
    dictionary=PyDictionary()
    l=[]
    new_instance = Thesaurus(keyword)
    try:
        meaning = dictionary.meaning(keyword)
    except:
        meaning = "No Meaning Found"
  

    return HttpResponse(json.dumps([meaning,defination,examples,list(set(synonyms)),list(set(antonyms))]))

def my_bookmarks(request):
    return render(request,'article/bookmarks.html')


#------------------------------ AJAX------------------------------
def subscribe(request):
    user_name = request.user
    print(user_name)
    user_title = request.GET.get('title')
    print(user_title)
    post_obj = Profile.objects.get(user = User.objects.get(username = user_title))
    if user_name in post_obj.subscribe.all():
        post_obj.subscribe.remove(user_name)
        key = True
        

    else:
        post_obj.subscribe.add(user_name)
        key = False

    return HttpResponse(json.dumps([key]))

def mute(request):
    user_name = request.user
    user_title = request.GET.get('title').replace("_"," ")
    user_ins = User.objects.get(username = user_title)
    ids = str(request.GET.get('id'))
    post_obj = Profile.objects.get(user = user_name)
    if user_ins in post_obj.mute.all():
        post_obj.mute.remove(user_ins)
        key = True
        

    else:
        post_obj.mute.add(user_ins)
        key = False

    return HttpResponse(json.dumps([key,ids]))



















def web_scraping(request):
        
        url="https://www.instyle.com/fashion"
        html_doc=requests.get(url).content
        soup = BeautifulSoup(html_doc,'html5lib')
        for i in soup.find_all('article')[:2]:
            
            title = i.find('div',['class','media-body']).find('h3').text.strip()
            if Articles.objects.filter(title = title).exists():
                pass
            else:
                dd = i.find('a')
                image_link = dd.find('img')['src']
                url_child = 'https://instyle.com'+i.find('a')['href']
                so = BeautifulSoup(requests.get(url_child).content,'html5lib')
                content=[]
                for i in so.find_all('div',['class','paragraph']):
                    
                    content.append(i.text.strip())
                desc=content[0]
                ref_ti = Articles(user_name2 = User.objects.get(username = 'sparsh'),title=title,content=content,\
                    category = Categories.objects.get(category_name = 'Fashion'),author='admin',link=url_child,\
                        description =desc,tags='Fashion,News,Culture,Fashion Tips,Outfits,Culture',image2=image_link)
                
                
                ref_ti.save()
                try:
                    act = activity(user_name3 = User.objects.get(username = 'sparsh'),user_activity = f'Article named {title} saved from instyle.com !!',activity_icon='fa fa-newspaper')
                    act.save()
                except:
                    pass
        return HttpResponse(json.dumps(" "))
      