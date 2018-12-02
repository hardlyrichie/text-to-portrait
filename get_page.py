import requests

def get_page(page_url):
    try:
        res = requests.get(page_url)
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema) as e:
        print('<Invalid Syntax>')
        return None

    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError:
        return None
        
    return res