#! python3

import bs4, sys
from get_page import get_page

print('Enter Name:')
name = input()

search_url = f'https://google.com/search?q={name}&source=lnms&tbm=isch'
search = get_page(search_url)

# Manually input url if google image url not available
while not search:
    print("Can't get search url. Enter manually (Type exit to quit):")
    search_url = input()

    if search_url.lower() == 'exit':
      sys.exit()

    search = get_page(search_url)

# page = open('seach.html', 'w')
# page.write(search.text)
# page.close()

# Scraping for image
soup = bs4.BeautifulSoup(search.text, 'html.parser')

# print(soup)
print(soup.find_all("div", {"class": "rg_meta"}))
# print(f'https://google.com/{soup.select(".rg_l")[0].href}')
