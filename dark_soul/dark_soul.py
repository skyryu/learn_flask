'''
demo
'''
import os

from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from logging import DEBUG
from forms import BookmarkForm
import models

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '010018'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(BASE_DIR, 'dark_soul.db')

#I can see any case in this app that we need to track obj modifcations of sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.setLevel(DEBUG)

#sqlite db
db = SQLAlchemy(app)

bookmarks = []

''' use sqlalchemy instead in memory storage
def store_bookmark(url, description):
    bookmarks.append(dict(
        url=url,
        description=description,
        user='reindert',
        date=datetime.utcnow()
    ))

def new_bookmarks(num):
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]
'''

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
    recent_bookmarks=models.Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = models.Bookmark(url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        #store_bookmark(url, description)
        flash("store '{}'".format(description))
        return redirect(url_for('index'))
    else:
        return render_template('add.html', form=form)
    '''
    if request.method == 'POST':
        url = request.form['url']
        store_bookmark(url)
        flash("Stored bookmark '{}'".format(url))
        #app.logger.debug('store url:' + url)
        return redirect(url_for('index'))
    else:
        return render_template('add.html')
    '''

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
