import copy
from . import data as d
import numpy as np

from bs4 import BeautifulSoup as bSoup
import requests

#Doggo image: data:image/jpeg;base64,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

def get_sum(items, indices):
    """Stores the sum of the ranks passed into function and stores in items dictionary"""

    for name, features in items.items():
        sum = 0
        for index in indices:
            sum += int(items[name][index])
        items[name][d.user_sum_index] = sum

#TODO maybe refactor this into two functions, one for ranking in dictionary and one for list. But they fit nicely so idk
def rank(items, operation, index, indexR, return_seq_list):
    """Stores the rank of the item in the items dict given what attribute to rank and whether max or min is rank 1.
       Also returns a sequential list of titles if needed."""

    itemsCopy = copy.deepcopy(items)
    values = []

    if return_seq_list:
        ranked_titles = [[]] * (len(itemsCopy))  # Used to return list of names or ranked "keys"
    else:
        ranked_titles = [[]] * (len(itemsCopy) + 1)  # Used to return list of names or ranked "keys"

    temp = 0
    rank = 0

    while (len(itemsCopy) > 0):
        minKey = operation(itemsCopy, key=lambda x: float(itemsCopy[x][index]))
        temp = items[minKey][index]

        #Check if the found value is already in the list of found values.
        if (temp in values) and not return_seq_list:
            items[minKey][indexR] = int(rank)
            ranked_titles[rank].append(minKey)
        else:
            rank += 1
            items[minKey][indexR] = int(rank)
            values.append(temp)

            if return_seq_list: #If you want the index to represent the rank, set to False.
                ranked_titles[rank - 1] = [minKey][0]
            else:
                ranked_titles[rank] = [minKey]

        del itemsCopy[minKey]

    if return_seq_list:
        return ranked_titles

def retrieve_data(itemContainers, items):
    """Retrieves the needed data from website and stores it in a dictionary"""

    for item in itemContainers:
        #Gets title of item stored in "at" tag in class "item_title"
        title = get_title_ng(item)  #get_title_ng(item)

        # Gets rating and number of ratings of the item
        rating_info = get_rating_info_ng(item)
        rating = rating_info["rating"]
        numRev = rating_info["num_reviews"]

        #Get price stored in "li" tag in class "price-current"
        price = get_price_ng(item)

        #Get Image link of item.
        image_link = get_image_link_ng(item)

        #Gets link to item
        base_link = get_link_ng(item)


        #Initializes an array to store the information you get from site initially
        itemInfo = [None] * d.lengthDataGot

        #Only adds an item if there is a price and if the item is in main section of page item list.
        #If it isn't in main section last char in title is a space.
        if (price != "No Price") and (title[-1] != " "):
            itemInfo[d.priceIndex] = price
            itemInfo[d.reviewsIndex] = rating
            itemInfo[d.numReviewsIndex] = numRev
            itemInfo[d.imageIndex] = image_link
            itemInfo[d.link_index] = base_link
            itemInfo = np.hstack((itemInfo, np.zeros(d.lengthItemInfo - len(itemInfo), dtype=float)))

            items[title] = itemInfo

    return itemContainers

def display_dictionary(items):
    """Prints the items and its contents out"""

    for item in items:
        print("")
        print("Name of item: " + str(item))
        print("Rating: " + str(items[item][d.reviewsIndex]))
        print("Price: " + str(items[item][d.priceIndex]))
        print("Image link: " + str(items[item][d.imageIndex]))
        print("Base link: " + str(items[item][d.link_index]))
        print("Number of Reviews: " + str(items[item][d.numReviewsIndex]))
        print("Price Rank: " + str(items[item][d.priceRIndex]))
        print("Reviews Rank: " + str(items[item][d.reviewsRIndex]))
        print("Number of Reviews Rank: " + str(items[item][d.numReviewsRIndex]))
        print("Relationship between reviews and prices: " + str(items[item][d.relRPIndex]))
        print("Users summed value: " + str(items[item][d.user_sum_index]))
        print("Users sum rank: " + str(items[item][d.user_rank_index]))
        print("Relationship Rank: " + str(items[item][d.relRPRIndex]))

#NewEgg Specific Scraping Functions:

def get_item_containers_ng(url):
    """Creates a List of item containers from the specified site"""
    request = requests.get(url).text
    soup = bSoup(request, "html.parser")
    itemContainers = soup.find_all("div", {"class": "item-container"})

    return itemContainers

def get_title_ng(item):
    """Function that retrieves the title of an item in New Egg"""
    #Gets title of item stored in "at" tag in class "item_title"
    titleHTML = item.find("a", {"class": "item-title"})

    if titleHTML is None:
        title = d.null_title
    else:
        # Makes sure that name fits well into card
        title = titleHTML.text
        if len(title) < d.max_name:
            spaces = []
            for i in range(d.max_name - len(title)):
                spaces.append(" ")
            title = title.join(spaces)

    return title
def get_price_ng(item):
    """Retireves the price of an item in New Egg"""
    # Get price stored in "li" tag in class "price-current"
    priceHTML = item.find("li", {"class": "price-current"})

    if priceHTML is None:  # TODO make this a try catch
        price = d.null_price
    else:
        # The price is stored in the "strong" tag
        priceHTMLStrong = priceHTML.find("strong")

        # Some times the price says "COMING SOON"
        if priceHTMLStrong is not None and (priceHTMLStrong.text[0] != "C"):
            price = float(priceHTMLStrong.text.replace(',', '')) + float(priceHTML.sup.text.replace(',', ''))

        else:
            price = d.null_price

    return price

def get_rating_info_ng(item):
    """Retireves the rating of an item in New Egg"""
    iTag = item.find("i")

    if iTag is None:
        rating = d.null_rating
        numRev = d.null_num_rev
    else:
        # Sometimes ratings will be there and sometimes they wont
        classWords = iTag["class"]
        if (classWords[0] != "rating"):
            rating = d.null_rating
            numRev = d.null_num_rev
        else:
            # Stores rating
            rating = int(classWords[1][-1])
            # Gets number of reviews of item
            numRevHTML = item.find("span", {"class": "item-rating-num"})
            num_text = numRevHTML.text[1:-1]
            num_text = num_text.replace(',', '')
            numRev = int(num_text)

    return {"rating": rating, "num_reviews": numRev}

def get_image_link_ng(item):
    """Retireves the image of an item in New Egg"""
    # Get Image link stored in first "a" tag of html.
    a_tags = item.findAll("a")
    a_tag = a_tags[0]
    image_tag = a_tag.find("img")

    # Some images are stored in either "data-src" or "src" of tag
    if image_tag.get("data-src") is None:
        if image_tag.get("src") is not None:
            image_link = image_tag.get("src")

        else:
            image_link = d.null_image_link
    else:
        image_link = image_tag.get("data-src")

    return image_link

def get_link_ng(item):
    """Retireves the link to an item in New Egg"""
    # Still works with first "a" tag. Get the url or link to actual item
    a_tags = item.findAll("a")
    a_tag = a_tags[0]

    # Still works with first "a" tag
    base_link = a_tag.get("href")

    return base_link


def get_item_containers_bb(url):
    """A tragedy of me trying to scrape best buy"""
    request = requests.get(url, headers=d.headers, timeout=5).text
    soup = bSoup(request, "html.parser")
    print(soup.text)
    itemContainers = soup.find_all("div", {"class": "container-fluid_Up8mf"})
    print(len(itemContainers))
    for item in itemContainers:
        print(item.get("div"))
    return itemContainers