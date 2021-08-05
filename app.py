from pymongo import MongoClient
from random import choices
import string
import validators
from flask import Flask, render_template, request, flash, redirect, url_for

# connect to DB
client = MongoClient("mongodb+srv://MORIYA:25112001@url-db.xdr7i.mongodb.net/URL-DB?retryWrites=true&w=majority")
db = client.ShortUrls

#requried fonctions:  generate short url, get short url, get long url, check if longqshort url exists 
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
    short_url += ''.join(choices(characters, k=7))
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

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'moriya'

#get url input from user, validate it and give suit response
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        long_url = request.form['url']

        if not long_url or not validators.url(long_url):
            flash('URL is required!')
            return redirect(url_for('index'))

        short_url = get_short_link(long_url)

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

#redirect to original-url by short_url
@app.route('/<short_url>')
def url_redirect(short_url):
    if is_shorturl_exists(short_url):
        long_url = get_long_url(short_url)
        return redirect(long_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))

#view statistics of urls
@app.route('/stats')
def stats():
    corsur = db.urls 
    urls = corsur.find()

    return render_template('stats.html', urls=urls)

#return about html page
@app.route('/about')
def about():
    return render_template('about.html')

# run app
if __name__ == "__main__":
    app.run()
