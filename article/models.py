from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from ckeditor.fields import RichTextField
from stories.models import Stories
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=40, unique=True,default="")
    def __str__(self):
        return self.category_name


class Articles(models.Model):
    STATUS_CHOICES = (
		('draft', 'Draft'),('published', 'Published'),)
    METHOD_CHOICES = (
		('content', 'content'),('design', 'design'),('editor','editor'))
    user_name2 = models.ForeignKey(User, related_name='project_username_2', to_field='username', on_delete=models.CASCADE)
    title = models.CharField(max_length=150,default=" ",blank=False,unique=True)
    project_name = models.CharField(max_length=100, blank=False , null=False)
    author = models.CharField(max_length=50,blank=True)
    date_Publish = models.DateField(default=datetime.now)
    date_updated = models.DateField(default=datetime.now)
    category = models.ForeignKey(Categories,related_name = 'category', to_field='category_name',on_delete=models.CASCADE,default=" ")
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
    liked = models.ManyToManyField(User,default=None,blank=True,related_name="likes_title")
    disliked = models.ManyToManyField(User,default=None,blank=True,related_name="dislikes_title")
    template = models.CharField(max_length=1000,blank=True,null=True)
    quora = models.CharField(max_length=1000,blank=True,null=True)
    medium= models.CharField(max_length=1000,blank=True,null=True)
    facebook = models.CharField(max_length=1000,blank=True,null=True)
    instagram = models.CharField(max_length=1000,blank=True,null=True)
    twitter = models.CharField(max_length=1000,blank=True,null=True)
    other= models.CharField(max_length=1000,blank=True,null=True)
    views = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    
    
	
   
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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True,default="---")
    last_name = models.CharField(max_length=50, blank=True,default="---")
    email = models.EmailField(max_length=50, blank=True,default="---")
    phone_number = models.CharField(max_length=13, blank=True,default="---")
    avatar = models.ImageField(upload_to='users/avatar',blank=False,default = 'users/avatar/default.jpg')
    bio = models.TextField(blank=True,default="---")
    address = models.CharField(max_length=50, blank=True,default="---")
    city = models.CharField(max_length=50, blank=True,default="---")
    state  = models.CharField(max_length=50, blank=True,default="---")
    country = models.CharField(max_length=50, blank=True,default="---")
    date_of_birth = models.CharField(max_length=13, blank=True,default="---")
    follow = models.ManyToManyField(User,default=None,blank=True,related_name="follow_title")
    following = models.ManyToManyField(User,default=None,blank=True,related_name="following_title")
    signup_confirmation = models.BooleanField(default=False)
    instagram = models.CharField(max_length=1000,blank=True,null=True)
    facebook = models.CharField(max_length=1000,blank=True,null=True)
    twitter = models.CharField(max_length=1000,blank=True,null=True)
 
    medium = models.CharField(max_length=1000,blank=True,null=True)
    quora = models.CharField(max_length=1000,blank=True,null=True)
    other = models.CharField(max_length=1000,blank=True,null=True)
    favourities = models.ManyToManyField(Articles,blank=True,related_name="articles_titles")
    fav_stories = models.ManyToManyField(Stories,blank=True,related_name="stories_titles")
    
  
    

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class my_comment(models.Model):
    post = models.ForeignKey(Articles, related_name='my_comments',on_delete=models.CASCADE)
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True,null=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created',)
    def children(self):
        return my_comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

    

class activity(models.Model):
    user_name3 = models.ForeignKey(User, related_name='project_username_3', to_field='username', on_delete=models.CASCADE)
    user_activity = models.CharField(max_length=200,blank=True)
    activity_icon = models.CharField(max_length=200,blank=True)
    activity_time= models.TimeField(blank=False,default=datetime.now())
    date_activity = models.DateField(default=datetime.now)
    activity_count = models.IntegerField(default =0,null=True)
    def __str__(self):
        return f'{self.user_name3}  -- > Activty {self.user_activity}'
class Notifications(models.Model):
      user_name4 = models.ForeignKey(User,related_name="user_name4_notification",to_field='username',on_delete=models.CASCADE)
      activity_count = models.IntegerField(default =0)
    
      activity_profile_count = models.IntegerField(default =0)
     
      follow_count = models.IntegerField(default =0)
      following_count = models.IntegerField(default =0)
      def __str__(self):
          return " activity_count "+ str(self.activity_count) + " follow_count " + str(self.follow_count)+ " following_count " + str(self.following_count)

class titleview(models.Model):
    view = models.ForeignKey(Articles,related_name="titleview",on_delete=models.CASCADE)
    ip_addr = models.CharField(max_length=300,blank=True,null=True)
    def __str__(self):
        return str(self.view)+ " " + str(self.ip_addr)
