'''
demo
'''

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user

from dark_soul.forms import BookmarkForm, LoginForm, SignupForm
from dark_soul.models import Bookmark, User, Tag
from dark_soul import app
from dark_soul import db
from dark_soul import login_manager

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

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', recent_bookmarks=Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookmarkForm()
    if form.validate_on_submit():
        url = form.url.data
        description = form.description.data
        tags = form.tags.data
        bm = Bookmark(user= current_user, url=url, description=description,
                      tags=tags)
        db.session.add(bm)
        db.session.commit()
        #store_bookmark(url, description)
        flash("store '{}'".format(description))
        return redirect(url_for('index'))
    else:
        return render_template('bookmark_form.html', form=form, title='Add new URL')
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

@app.route('/delete/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def delete_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    if request.method == 'POST':
        db.session.delete(bookmark)
        db.session.commit()
        flash("Delete '{}'".format(bookmark.description))
        return redirect(url_for('user', username=current_user.username))
    else:
        flash('Please confirm delete the bookmark.')
        return render_template('confirm_delete.html', bookmark=bookmark, no_links=True)


@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Store '{}'".format(bookmark.description))
        return redirect(url_for('index'))
    else:
        return render_template('bookmark_form.html', form=form, title='Edit URL')

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #login and validate te user...
        user = User.get_by_username(form.username.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash("Logged in successfully as {}.".format(user.username))
            return redirect(request.args.get('next') or url_for('user', username=user.username))
        flash('Incorrect username or password.')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Welcome, {}! Please login.".format(user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/tag/<name>')
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    return render_template('tag.html', tag=tag)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(403)
def permission_deny(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.context_processor
def inject_tags():
    return dict(all_tags=Tag.all)

if __name__ == '__main__':
    app.run(debug=True)
