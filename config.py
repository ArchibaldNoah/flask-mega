import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://archibaldpg:aaa7X*178@192.168.178.38:5432/flaskmega_db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	POSTS_PER_PAGE = 5
