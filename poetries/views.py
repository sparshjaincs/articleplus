from django.shortcuts import render

# Create your views here.
def poetries_page(request):
    return render(request,'poetries/poetries.html')