--------------------------------
This project is the implementation of Plurasight course: Introduction to the Flask Microframework (2014 Dec by Reindert Ekker)

Environment set up:
To view sqllite db file, I use SQL Lite Studio 3.1.1

20180114
pip install Flask-Script
flask.ext.script is deprecated, use flask_script package instead.

20180116
add user page.

20180121
conda install flask-login
add login validation and login page

20180131
add current_user and logout function
in flask_login 0.4.1 the is_authenticated is a property instead of a method, so
we should use current_user.is_authenticated instead of current_user.is_authenticated().

add password authentication.

---------------------------------
20180214
check WTForm validation method to see how the implementation of in-line
validator at: wtforms/wtforms/form.py

def validate(self):
    """
    Validates the form by calling `validate` on each field, passing any
    extra `Form.validate_<fieldname>` validators to the field validator.
    """
    extra = {}
    for name in self._fields:
        inline = getattr(self.__class__, 'validate_%s' % name, None)
        if inline is not None:
            extra[name] = [inline]

    return super(Form, self).validate(extra)

----------------------------
20180214
Valentine's day.

pip install flask-moment

----------------------------
20180215
re-arrange the layout of the bookmark list into bookmark_list.html.
modify the css for bookmark_list.html in main.css

---------------------------
20180216

Importing flask.ext.moment is deprecated, use flask_moment instead.

---------------------------
20180509

many thing happened during these 3 month since the last time I come. sad
things. new start.

pip install flask-migrate
flask.ext.migrate is deprecated, use flask_migrate instead.

---------------------------
20180510

add Tag table in models.py
add Tag in view and templates.

--------------------------
20180514
create environment.yaml by using(suggested):
    conda env export > environment.yaml
this can be share in other env by using:
    conda env update -f=/path/to/environment.yml

create requirement.txt by using(if don't have conda):
    pip freeze > requirement.txt
this can be shared in other env by using:
    pip install -r /path/requirements.txt

-------------------------
20180626
fix a bug for bookmark_list.html about the tags.

