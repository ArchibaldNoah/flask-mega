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
	DOCUMENTS={"i_account" : 	{	# internet accounts, logins
									"k01" : {"key" : "site","label" : "Site"},
									"k03" : {"key" : "username","label" : "Username"},
									"k04" : {"key" : "password","label" : "Password"}
						   		},
               "contract" : 	{	# any contract like credit, purchase, rent, insurance, etc.
									"k01" : {"key" : "counterparty","label" : "Counterparty"}, # ideally use data from exchange
									"k02" : {"key" : "contract_id","label" : "Contract ID"},
									"k03" : {"key" : "contract_type","label" : "Contract Type"},
									"k04" : {"key" : "contract_start_date","label" : "Contract Start Date"},
									"k05" : {"key" : "contract_end_date","label" : "Contract End Date"}
								},
               "news" : 		{	# any contract like credit, purchase, rent, insurance, etc.
									"k01" : {"key" : "source","label" : "Source"},
									"k02" : {"key" : "url","label" : "Source URL"},
									"k03" : {"key" : "publication_date","label" : "Publication Date"}
								}
			  }

	CONTRACT_TYPES = 	{
							"credit" : "Credit Contract",
							"insurance" : "Insurance Contract",
							"purchase" : "Purchase Contract",
							"rent" : "Rent Contract",
							"sale" : "Sales Contract",
							"service_provided" : "Contract for Services Provided",
							"service_taken" : "Contract for Services Purchased"
						}