from pymongo import MongoClient
from random import choices
import string
import validators
from flask import Flask, render_template, request, flash, redirect, url_for
from urlDB import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'moriya'

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
    urls = get_url_data()
    return render_template('stats.html', urls=urls)

#return about html page
@app.route('/about')
def about():
    return render_template('about.html')

# run app
if __name__ == "__main__":
    app.run()

