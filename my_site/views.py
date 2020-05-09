from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus

#File imports
from . import functions as f
from . import data as d

from . import models

#TODO edit base template and home view to redo search bar change

#Variables. We do this so that we can store default values in the main view.
search = ""
#The keys are the indices refering to the ranks chosen (refer to data.py) and the values are whether they
#are checked or not.
rank_filters = {}

for filter_index in d.filter_indices:
    rank_filters[filter_index] = None

# Create your views here.
def home(request):
    frontend_vars = {
        'search': search,
        'price_checked': rank_filters[d.priceRIndex],
        'ratings_checked': rank_filters[d.reviewsRIndex],
        'num_ratings_checked': rank_filters[d.numReviewsRIndex],
        'relationship_checked': rank_filters[d.relRPRIndex],
    }

    return render(request, 'my_site/home.html')

#Make search a global variable so that if the user puts in nothing, it will

def new_search(request):

    search = request.POST.get('search') #Gets search value from form
    rank_filters[d.priceRIndex] = request.POST.get('price_checked')  # Gets search value from form
    rank_filters[d.reviewsRIndex] = request.POST.get('ratings_checked')
    rank_filters[d.numReviewsRIndex] = request.POST.get('num_ratings_checked')
    rank_filters[d.relRPRIndex] = request.POST.get('relationship_checked')
    #price_checked = request.POST.get('price_checked')
    models.Search.objects.create(search=search) #Creates a search object in database
    final_url = d.BASE_URL.format(quote_plus(search)) #New Egg url for users search

    # Variables for storing
    items = {}
    itemContainers, test = f.get_item_containers_ng(final_url)
    len_item_containers = len(itemContainers)
    # retrieves the information I want from the website
    itemContainers = f.retrieve_data(itemContainers, items)

    #TODO Also refactor this part so that you can create a for loop instead of ranking three times

    # ranks prices
    f.rank(items, min, d.priceIndex, d.priceRIndex, False)

    # ranks reviews
    f.rank(items, max, d.reviewsIndex, d.reviewsRIndex, False)

    # ranks number reviews:
    f.rank(items, max, d.numReviewsIndex, d.numReviewsRIndex, False)

    # Store relationship between price and reviews
    for item in items:
        difference = abs(int(items[item][d.priceRIndex]) - int(items[item][d.reviewsRIndex]))
        items[item][d.relRPIndex] = difference

    # Ranks relationship
    f.rank(items, min, d.relRPIndex, d.relRPRIndex, False)

    rank_choices = []
    ranked_keys = []

    #Decides what to rank and display to user. For explanation of how dictionary is formatted check data.
    if search != "":
        for filter_index, status in rank_filters.items():
            if status:
                rank_choices.append(int(filter_index))
                rank_filters[int(filter_index)] = "checked"
            else:
                rank_filters[int(filter_index)] = None

        # Store sum of the selected ranks and stores them in the items dictionary
        f.get_sum(items, rank_choices)

        #Rank this combined sum out of all items. Returns a list of keys with the index representing the rank
        #Since it starts at rank 1, this list will be one size bigger than the items list

        ranked_keys = f.rank(items, min, d.user_sum_index, d.user_rank_index, True)

    #Dictionary of Values used in html front end Django Templates
    frontend_vars = {
        'search': search,
        'items': items,
        'ranked_keys': ranked_keys,
        'title_name_limit': d.max_name,
        'image_index': d.imageIndex,
        'base_link_index': d.link_index,
        'price_index': d.priceIndex,
        'rating_index': d.reviewsIndex,
        'num_ratings_index': d.numReviewsIndex,
        'price_rank_index': d.priceRIndex,
        'rating_rank_index': d.reviewsRIndex,
        'num_rating_rank_index': d.numReviewsRIndex,
        'relationship_rank_index': d.relRPRIndex,
        'price_checked': rank_filters[d.priceRIndex],
        'ratings_checked': rank_filters[d.reviewsRIndex],
        'num_ratings_checked': rank_filters[d.numReviewsRIndex],
        'relationship_checked': rank_filters[d.relRPRIndex],
        'test': test,
    }

    # Displays items
    #f.display_dictionary(items)

    return render(request, "my_site/new_search.html", frontend_vars)