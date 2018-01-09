'''
demo
'''

from flask import render_template, request, redirect, url_for, flash

from dark_soul.forms import BookmarkForm
from dark_soul.models import Bookmark, User
from dark_soul import app
from dark_soul import db

''' use sqlalchemy instead in memory storage
bookmarks = []
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
    recent_bookmarks=Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        bm = Bookmark(url=url, description=description)
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
