
from django import forms

from .models import *

class Stories_form(forms.ModelForm):
    title = forms.Field(widget=forms.TextInput(attrs={'required':True}))
    class Meta:
        model = Stories
        fields = ('title','image','video','category','tags','facebook','instagram','quora','medium','twitter','other','content')
class CommentForm(forms.ModelForm):
	class Meta:
		model = Story_comment
		fields = ('name', 'email', 'body')