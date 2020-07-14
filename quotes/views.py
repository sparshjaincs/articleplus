from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from .models import * 
from article.models import Profile,activity
from django.contrib import messages

def quotes_page(request):
    context={}
    context['stories'] = Quotes.objects.filter(status = 'published').order_by('-date_Publish','-time')
    context['category'] = Categories.objects.all()
    context['users'] = User.objects.all().order_by('first_name')
    return render(request,'quotes/quotes.html',context)
def category(request,category):
    context = {}
    context['name'] = category
    context['category'] = Categories.objects.all()
    context['stories'] = Stories.objects.filter(status = 'published',category = Categories.objects.get(category_name = category)).order_by('-date_Publish','-time')
    context['users'] = User.objects.all()

    return render(request,'stories/category.html',context)

def editor(request):
    context = {}
    if request.method == 'POST':
            
            form = Quotes_form(request.POST,request.FILES)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.user_quotes = request.user
                ins.author = request.user
                ins.save() 
                messages.success(request,'Your Quote is published.')
                return redirect('/')
            else:
                context['errors'] = str(form.errors)
    else:
        form = Quotes_form()
    context['quotes_form'] = form
    return render(request,'quotes/quotes_editor.html',context)

def stories_draft(request):
    context={}
    if request.method == 'POST':
            
            form = Stories_form(request.POST,request.FILES)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.user_stories = request.user
                ins.author = request.user
                title = form.cleaned_data['title'].replace(" ","_")
                ins.link = f'/stories/{request.user}/{title}'
                ins.status = 'Draft'
                ins.save()
            else:
                context['errors'] = str(form.errors)
    else:
            form = Stories_form()
    return HttpResponseRedirect('/')
    pass
def story_draft(request,title):
    context = {}
    
    if request.method == 'POST':
            
            form = Stories_form(request.POST,request.FILES)
            tit = request.POST.get('title')
            ins = Stories.objects.get(title=title.replace("_"," "))
            ins.status = 'Draft'
            ins.title = tit
            if request.FILES.get('image') is not None:
                ins.image = request.FILES.get('image')
            if request.FILES.get('video') is not None:
                ins.video = request.FILES.get('video')
            ins.category = Categories.objects.get(category_name = request.POST.get('category'))
            ins.content = request.POST.get('content')
            ins.description = request.POST.get('content').split(".")[0]
            ins.link = f'/stories/{request.user}/{tit.replace(" ","_")}'
            ins.tags = request.POST.get('tags')
            ins.facebook = request.POST.get('facebook')
            ins.twitter = request.POST.get('twitter')
            ins.quora = request.POST.get('quora')
            ins.instagram = request.POST.get('instagram')
            ins.medium = request.POST.get('medium')
            ins.other = request.POST.get('other')
            
            ins.save()
           

                


    else:
            form = Stories_form()
    return HttpResponseRedirect('/')
def story_preview(request,title):
    context = {}
    
    if request.method == 'POST':
            
            form = Stories_form(request.POST,request.FILES)
            tit = request.POST.get('title')
            ins = Stories.objects.get(title=title.replace("_"," "))
            ins.status = 'Draft'
            ins.title = tit
            if request.FILES.get('image') is not None:
                ins.image = request.FILES.get('image')
            if request.FILES.get('video') is not None:
                ins.video = request.FILES.get('video')
            ins.category = Categories.objects.get(category_name = request.POST.get('category'))
            ins.content = request.POST.get('content')
            ins.description = request.POST.get('content').split(".")[0]
            ins.link = f'/stories/{request.user}/{tit.replace(" ","_")}'
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
    return render(request,'stories/preview.html',context)
def preview(request):
    context = {}
    tit = request.GET.get('title')
    
    if request.method == 'POST':
            
            form = Stories_form(request.POST,request.FILES)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.user_stories = request.user
                ins.author = request.user
                title = form.cleaned_data['title'].replace(" ","_")
                ins.link = f'/stories/{request.user}/{title}'
                ins.status = 'Draft'
                ins.content = form.cleaned_data['content'].split(".")[0].strip("<p>")
                ins.save()
                context['title'] = title
                context['message'] =ins.link
                

            else:
                tit= request.POST.get('title')
                data_ins = Stories.objects.get(title = tit.replace("_"," "))
                context['title'] = tit
                context['message'] =data_ins.link
                


    else:
            form = Stories_form()


    context['edit'] = True
    return render(request,'stories/preview.html',context) 
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
def stories_read(request,username,title):
    context={}
    post = get_object_or_404(Stories, title = title.replace("_"," "))
    comments = post.Story_comments.filter(post = post,active=True,parent=None)
    ip_addr = get_client_ip(request)
    if not titleview.objects.filter(view=post,ip_addr=ip_addr).exists():
        ins = titleview(view = post,ip_addr = ip_addr)
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
            
           
            new_comment.post.user_stories
    else:
        comment_form = CommentForm()
    context['form'] = comment_form
    context['comments'] = comments
    
    context['read']=[post]
    context['article_trend'] = Stories.objects.filter(status="published").order_by('-date_Publish','-time')[:4]
    context['tags'] = post.tags.split(",")
    context['template'] = post.template
    return render(request,'stories/read.html',context)

def like(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('like')
        url = request.POST.get('url')
        post_obj = Stories.objects.get(title = title)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
            

        else:
            post_obj.liked.add(user)
            activity_title=f"You liked Article with title {title} !!"
            activity_icon = 'fa fa-thumbs-up'
            act = activity(user_name3 = request.user,user_activity = activity_title,activity_icon=activity_icon)
            act.save()
            

            
            if user in post_obj.disliked.all():
                post_obj.disliked.remove(user)
      

    
    return HttpResponseRedirect(url)

def dislike(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('like')
        url = request.POST.get('url')
        post_obj = Stories.objects.get(title = title)
        if user in post_obj.disliked.all():
            post_obj.disliked.remove(user)
        else:
            post_obj.disliked.add(user)
            activity_title=f"You disliked Article with title {title} !!"
            activity_icon = 'fa fa-thumbs-down'
            act = activity(user_name3 = request.user,user_activity = activity_title,activity_icon=activity_icon)
            act.save()
            if user in post_obj.liked.all():
                post_obj.liked.remove(user)
    
    return HttpResponseRedirect(url)

def save_fav(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title')
        tit = request.POST.get('user_name')
        tit_ins = Stories.objects.get(title = tit)
        prof_ins = Profile.objects.get(user = user)
      
        if tit_ins in prof_ins.fav_stories.all():
            prof_ins.fav_stories.remove(tit_ins)
        else:
            prof_ins.fav_stories.add(tit_ins)
        

        
        
    return HttpResponseRedirect(title)

def preview_publish(request,title):
    ins = Stories.objects.get(title = title.replace("_"," "))
    ins.status = 'published'

    ins.save()
    return HttpResponseRedirect('/')
    
def preview_edit(request,title):
    context = {}
    if request.method == 'POST':
            
            form = Stories_form(request.POST,request.FILES)
         
               
            tit = request.POST.get('title')
            ins = Stories.objects.get(title=title.replace("_"," "))
            ins.status = 'published'
            ins.title = tit
            if request.FILES.get('image') is not None:
                ins.image = request.FILES.get('image')
            if request.FILES.get('video') is not None:
                ins.video = request.FILES.get('video')
            ins.category = Categories.objects.get(category_name = request.POST.get('category'))
            ins.content = request.POST.get('content')
            ins.description = request.POST.get('content').split(".")[0]
            ins.link = f'/stories/{request.user}/{tit.replace(" ","_")}'
            ins.tags = request.POST.get('tags')
            ins.facebook = request.POST.get('facebook')
            ins.twitter = request.POST.get('twitter')
            ins.quora = request.POST.get('quora')
            ins.instagram = request.POST.get('instagram')
            ins.medium = request.POST.get('medium')
            ins.other = request.POST.get('other')
            
            ins.save()
            return HttpResponseRedirect('/')
           
    else:   
           
            ins = Stories.objects.filter(title = title.replace("_"," ")).first()
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

            form = Stories_form(initial=initial)

    context['title'] = title
    context['edit'] = True
    context['story_form'] = form
    
    return render(request,'stories/stories_text_editor.html',context)

def delete(request,title):
    context={}
    if Stories.objects.filter(title = title.replace("_"," ")).exists():   
        Stories.objects.filter(title = title.replace("_"," ")).delete()
    messages.success(request,f'You Successfully deleted Story with title {title.replace("_"," ")}')
    return HttpResponseRedirect('/')    