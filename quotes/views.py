from django.shortcuts import render

# Create your views here.
def quotes_page(request):
    return render(request,'quotes/quotes.html')