import requests
import re
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://kolkata.craigslist.org/search/?query={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    # Extracting the source code of the page
    data = response.text
    # Passing source code to Beautiful Soup to create a BeautifulSoup object for it
    soup = BeautifulSoup(data, features='html.parser')
    # post_titles = soup.find_all('a', {'class': 'result-title'})
    # Extracting all the <a> tags whose class name is 'result-title' into a list
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        '''
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            new_response = requests.get(post_url)
            new_data = new_response.text
            new_soup = BeautifulSoup(new_data, features='html.parser')
            post_text = new_soup.find(id='postingbody').text

            r1 = re.findall(r'\$\w+', post_text)
            if r1:
                post_price = r1[0]
            else:
                post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')
            post_image_url = "https://images.craigslist.org/{}_300x300.jpg".format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'
        '''
        final_postings.append((post_title, post_url, post_price))
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
