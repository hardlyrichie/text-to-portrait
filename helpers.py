import requests, pathlib, errno, shutil, os

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

# Taken from https://stackoverflow.com/questions/23793987/write-file-to-a-directory-that-doesnt-exist
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_wb(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    pathlib.Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    return open(path, 'wb')

# Download image to initially nonexistant directory
def download_img(urls, name):
    for count, url in enumerate(urls):
        res = requests.get(url, stream=True)
        with safe_open_wb(f'images/{name}/{name}_{count}.jpg') as img:
            shutil.copyfileobj(res.raw, img)