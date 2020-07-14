from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Quotes)
admin.site.register(Categories)
admin.site.register(Quotes_comment)
admin.site.register(titleview)