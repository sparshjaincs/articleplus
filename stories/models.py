from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField

class Categories(models.Model):
    category_name = models.CharField(max_length=40, unique=True,default="")
    def __str__(self):
        return self.category_name

class Stories(models.Model):
    STATUS_CHOICES = (
		('draft', 'Draft'),('published', 'Published'),)
    METHOD_CHOICES = (
		('content', 'content'),('design', 'design'),('editor','editor'))
    user_stories = models.ForeignKey(User, related_name='user1', to_field='username', on_delete=models.CASCADE)
    title = models.CharField(max_length=150,default=" ",blank=False,unique=True)
    project_name = models.CharField(max_length=100, blank=False , null=False)
    author = models.CharField(max_length=50,blank=True)
    date_Publish = models.DateField(default=datetime.now)
    date_updated = models.DateField(default=datetime.now)
    category = models.ForeignKey(Categories,related_name = 'category1', to_field='category_name',on_delete=models.CASCADE,default=" ")
    image = models.ImageField(upload_to='users/images',blank=True,default='',null=True)
    video= models.FileField(upload_to='users/video', null=True,blank=True ,verbose_name="Video")
    image2 = models.CharField(max_length=1000,blank=True,null=True)
    content = RichTextField(blank=False,null=True)
    link = models.TextField(blank=True,default="")
    description = models.TextField(blank=True,default="")
    time= models.TimeField(blank=False,default=datetime.now())
    tags = models.CharField(max_length=300,blank=False,default="",null=True,help_text='Add comma( ,) seperated tags!!')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='published')
    method=models.CharField(max_length=10,choices=METHOD_CHOICES,default='content')
    liked = models.ManyToManyField(User,default=None,blank=True,related_name="likes_stories")
    disliked = models.ManyToManyField(User,default=None,blank=True,related_name="dislikes_stories")
    template = models.CharField(max_length=1000,blank=True,null=True)
    quora = models.CharField(max_length=1000,blank=True,null=True)
    medium= models.CharField(max_length=1000,blank=True,null=True)
    facebook = models.CharField(max_length=1000,blank=True,null=True)
    instagram = models.CharField(max_length=1000,blank=True,null=True)
    twitter = models.CharField(max_length=1000,blank=True,null=True)
    other= models.CharField(max_length=1000,blank=True,null=True)
    
    
	
   
    class Meta:
        ordering = ('date_Publish','time')
    def __str__(self):
        return self.title
    @property
    def num_likes(self):
        return self.liked.all().count()

    @property
    def num_dislikes(self):
        return self.disliked.all().count()

class Story_comment(models.Model):
    post = models.ForeignKey(Stories,related_name='Story_comments',on_delete=models.CASCADE)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created',)
    def children(self):
        return Story_comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

class titleview(models.Model):
    view = models.ForeignKey(Stories,related_name="titleview",to_field='title',on_delete=models.CASCADE)
    ip_addr = models.CharField(max_length=300,blank=True,null=True)
    def __str__(self):
        return str(self.view)+ " " + str(self.ip_addr)