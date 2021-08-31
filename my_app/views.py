from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from requests.compat import quote_plus
from . import models

BASE_CRAIGSLIST_URL = "https://newyork.craigslist.org/d/services/search/?query={}"
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get("search")
    models.Search.objects.create(search=search)
    url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, features="html.parser")

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []
    for post in post_listings:
        post_title = post.find(class_ = 'result-title').text
        post_url = post.find('a').get('href')
        post_image_url = ""
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_="result-image").get("data-ids"):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(":")[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = "https://lh6.googleusercontent.com/proxy/u0kqVJJi3bazlEgS_n1-mAyc02cZbG2u-xMdT-LPnLWyyvEt2fPSvVZDqzGoidfyMsml296tvOkmLgWA2BXq4PlIrHPlEyudj659uszD_ALLfP3GDZHgPh-ojUYrKPufZhOCDAirhU--i5xsTGqQmvn1qg=w1200-h630-p-k-no-nu"

        final_postings.append([post_title, post_url, post_price, post_image_url])




    dataForFrontEnd = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', dataForFrontEnd)
