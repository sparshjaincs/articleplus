
from django import forms

from .models import *

class Quotes_form(forms.ModelForm):

    class Meta:
        model = Quotes
        fields = ('title','image','category','tags','facebook','instagram','quora','medium','twitter','other','content')
class CommentForm(forms.ModelForm):
	class Meta:
		model = Quotes_comment
		fields = ('name', 'email', 'body')