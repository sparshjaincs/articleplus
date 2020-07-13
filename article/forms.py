
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Articles,Profile,my_comment



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
class Article_form(forms.ModelForm):
    title = forms.Field(widget=forms.TextInput(attrs={'required':True}))
    class Meta:
        model = Articles
        fields = ('title','image','video','category','tags','facebook','instagram','quora','medium','twitter','other','content')

class ProfileForm(forms.ModelForm):
    
    
    class Meta:
        model = Profile
        fields = ['phone_number', 'bio', 'address', 'city','state', 'country', 'avatar','date_of_birth','first_name','last_name','email','quora','medium','other']

class CommentForm(forms.ModelForm):
	class Meta:
		model = my_comment
		fields = ('name', 'email', 'body')