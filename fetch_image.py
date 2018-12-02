! python3

import sys, pprint, json
from helpers import *


# print('Enter Name:')
# name = input()

# # Fetch images from custom goolge search
# search_url = f'https://www.googleapis.com/customsearch/v1?key=AIzaSyCdKWliVigMt35I7pLM2zqKHftpaFxdCR0&cx=016561402344353211294:au-xlsd-kvu&q={name}&searchType=image&imgSize=large&filetype=jpg'
# search = get_page(search_url)

# # Manually input url if google image url not available
# while not search:
#     print("Can't get search url. Enter manually (Type exit to quit):")
#     search_url = input()

#     if search_url.lower() == 'exit':
#       sys.exit()

#     search = get_page(search_url)

# if (search.status_code != 200):
#   print('Error occured when attempting to fetch images')
# else:
#   content = json.loads(search.content)
#   items = content['items']
#   urls = list(map(lambda item: item['link'], items))
#   print(urls)

with open('content.json') as content_doc:
  content = json.load(content_doc)

  # Get urls of images
  items = content['items']
  urls = list(map(lambda item: item['link'], items))
  print(urls)

  # Download images
  download_img(urls, 'cows')



#   with open('content.json', 'w') as content_doc:
#     content_doc.write(json.dumps(content))
