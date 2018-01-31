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
