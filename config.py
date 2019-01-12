import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-long-secret-key'
#	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql+psycopg2://archibaldpg:aaa7X*178@192.168.178.38:5432/flaskmega_db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	POSTS_PER_PAGE = 5
#	LANGUAGES = ['en','de']

	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS=['dr.juergen.brust@gmail.com']

#   DOCUMENTS
	DOCUMENTS={"account" :{"01" : "username","02" : "password"},
               "contract" : {"01" : "counterparty","02" : "contract_type","03" : "contract_start_date","04" : "contract_end_date"}
			  }