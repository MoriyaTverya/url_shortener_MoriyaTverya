from pymongo import MongoClient
from random import choices
import string

# connect to DB
client = MongoClient("mongodb+srv://MORIYA:25112001@url-db.xdr7i.mongodb.net/URL-DB?retryWrites=true&w=majority")
db = client.ShortUrls

# requried fonctions:  generate short url, get short url, get long url, check if longqshort url exists, get url 
def get_long_url(short_url):
    return db.urls.find_one({ 'short_url': short_url}, {"long_url": 1, '_id': 0})["long_url"]

def is_longurl_exists(long_url):
    return db.urls.count_documents({ 'long_url': long_url}, limit = 1)

def is_shorturl_exists(short_url):
    return db.urls.count_documents({'short_url': short_url}, limit = 1)

#generate short link by create random string
def generate_short_link():
    short_url = 'minilink.'
    characters = string.digits + string.ascii_letters
    short_url += ''.join(choices(characters, k=3))
    return short_url

def get_short_link(long_url):
    if is_longurl_exists(long_url):
        return db.urls.find_one({ 'long_url': long_url }, {"short_url": 1, '_id': 0})["short_url"]
    short_url = generate_short_link()
    
    if is_shorturl_exists(short_url):
        generate_short_link(long_url)

    link = {'long_url' : long_url , 'short_url' : short_url}
    db.urls.insert_one(link)

    return short_url

def get_url_data():
    corsur = db.urls
    return corsur.find()
