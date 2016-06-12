######################################################
#
#Author:          whytin
#Email:           whytin@yeah.net
#QQ:              583501947
#
#Filename:        config.py
#Last modified:   2016-06-05 10:26
#Description:     
#
######################################################
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'complex secret'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	MAIL_SERVER = 'smtp.yeah.net'
	MAIL_PORT = 25
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	FLASKY_MAIL_SUBJECT_PREFIX = '[BLOG]'
	FLASKY_MAIL_SENDER = 'whytin <whytin@yeah.net>'
	FLASKY_ADMIN = os.environ.get('FLASY_ADMIN')
	FLASKY_POSTS_PER_PAGE = 10
	FLASKY_COMMENTS_PER_PAGE = 5

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+ os.path.join(basedir, 'data.sqlite')
	@classmethod
	def init_app(cls, app):
		Config.init_app(app)

		# email errors to the administrators
		import logging
		from logging.handlers import SMTPHandler
		credentials = None
		secure = None
		if getattr(cls, 'MAIL_USERNAME', None) is not None:
			credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
			if getattr(cls, 'MAIL_USE_TLS', None):
				secure = ()
		mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)


config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	'default': ProductionConfig 
}
