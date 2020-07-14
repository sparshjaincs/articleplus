
from django import forms

from .models import *

class Poetries_form(forms.ModelForm):
    title = forms.Field(widget=forms.TextInput(attrs={'required':True}))
    class Meta:
        model = Poetries
        fields = ('title','image','video','category','tags','facebook','instagram','quora','medium','twitter','other','content')
class CommentForm(forms.ModelForm):
	class Meta:
		model = Poetries_comment
		fields = ('name', 'email', 'body')