#Important Values

#URL and headers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"}

#Links:
BASE_URL = "https://www.newegg.ca/p/pl?d={}"
no_image_link = "https://us-static.z-dn.net/files/d5c/0ff50c772629bc0665622be6fa55e52a.jpg"

#Null data values
null_title = "No Title"
null_price = "No Price"
null_rating = "0"
null_num_rev = 0
null_image_link = "https://us-static.z-dn.net/files/d5c/0ff50c772629bc0665622be6fa55e52a.jpg"

#Indexes of data in item dictionary
priceIndex = 0
reviewsIndex = 1
numReviewsIndex = 2
imageIndex = 3
link_index = 4
priceRIndex = 5
reviewsRIndex = 6
numReviewsRIndex = 7
relRPIndex = 8
relRPRIndex = 9
user_sum_index = 10
user_rank_index = 11
lengthItemInfo = 12
lengthDataGot = 5

#Other
max_name = 30
num_filters = 4

#Filters Indexes.
#To keep it simple, I made the indices or "keys" to each of the filters in the rank_filter dict in views.py
#to be the same index as the rank of that filter stored in the items dictionary.
filter_indices = [priceRIndex, reviewsRIndex, numReviewsRIndex, relRPRIndex]