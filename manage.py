#! /usr/bin/env python

from dark_soul import app, db
from flask.ext.script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    print ('Initalized the database')

@manager.command
def dropdb():
    if prompt_bool('Are you sure you want to lose all your data'):
        db.drop_all()
        print('Dropped the database')

if __name__ == '__main__':
    manager.run()
