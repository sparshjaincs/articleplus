"""articleplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from article import views as user_views 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('article.urls')),
    path("stories/",include('stories.urls')),
    path("trending/",include('trends.urls')),
    path("quotes/",include('quotes.urls')),
    path("poetries/",include('poetries.urls')),
    path("api/",include("api.urls")),
    path('login/', auth_views.LoginView.as_view(template_name='article/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('password_reset/', user_views.MyPasswordResetView.as_view(template_name='article/password_reset.html'), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='article/password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='article/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='article/password_reset_complete.html'), name="password_reset_complete"),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='article/change_password.html', success_url="/"), name="password_change"),
    
    path('social-auth/', include('social_django.urls', namespace="social")),
      path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
  
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 