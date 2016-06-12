######################################################
#
#Author:          whytin
#Email:           whytin@yeah.net
#QQ:              583501947
#
#Filename:        manage.py
#Last modified:   2016-06-05 11:55
#Description:     
#
######################################################

#!/usr/bin/env python

import os
from app import create_app, db
from app.models import User, Role, Permission
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app,db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role, Permission=Permission)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
	"""Run deployment tasks"""
	from flask.ext.migrate import upgrade
	from app.models import Role

	upgrade()
	Role.insert_roles()

if __name__ == '__main__':
	manager.run()
