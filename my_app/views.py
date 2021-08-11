from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get("search")
    dataForFrontEnd = {
        'search': search,
    }
    return render(request, 'new_search.html', dataForFrontEnd)