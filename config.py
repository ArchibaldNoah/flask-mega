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
	DOCUMENTS={"iaccount" : 	{	# internet accounts, logins
									"k01" : {"key" : "site","label" : "Site"},
									"k02" : {"key" : "username","label" : "Username"},
									"k03" : {"key" : "password","label" : "Password"}
						   		},
               "citation" : 		{	# any contract like credit, purchase, rent, insurance, etc.
									"k01" : {"key" : "source","label" : "Source"}
			   					},
               "document" : 	{	# any contract like credit, purchase, rent, insurance, etc.
									"k01" : {"key" : "file","label" : "File ID"},
									"k02" : {"key" : "source","label" : "Source"},
									"k03" : {"key" : "file_url","label" : "File Location"},
									"k04" : {"key" : "publication_date","label" : "Publication Date"}
								},
               "contract" : 	{	# any contract like credit, purchase, rent, insurance, etc.
									"k01" : {"key" : "counterparty","label" : "Counterparty"}, # ideally use data from exchange
									"k02" : {"key" : "contract_id","label" : "Contract ID"},
									"k03" : {"key" : "contract_type","label" : "Contract Type"},
									"k04" : {"key" : "contract_start_date","label" : "Contract Start Date"},
									"k05" : {"key" : "contract_end_date","label" : "Contract End Date"}
								},
               "fact" : 		{	# any contract like credit, purchase, rent, insurance, etc.
									"k01" : {"key" : "source","label" : "Source"},
									"k02" : {"key" : "source_url","label" : "Source URL"},
									"k03" : {"key" : "reference_date","label" : "Reference Date"},		# date the fact refers to eg Population Desity as of 1.1.1900
									"k04" : {"key" : "publication_date","label" : "Publication Date"}
								},
               "news" : 		{	# any contract like credit, purchase, rent, insurance, etc.
									"k01" : {"key" : "source","label" : "Source"},
									"k02" : {"key" : "source_url","label" : "Source URL"},
									"k03" : {"key" : "publication_date","label" : "Publication Date"}
								},
				"payable" : 	{	# any payable also arising out of contracts
									"k01" : {"key" : "recipient","label" : "Recepient"},
									"k02" : {"key" : "recipient_id","label" : "Recepient ID"},  # Personennummer
									"k03" : {"key" : "contract_id","label" : "Contract ID"},	# e.g. Aktenkennzeichen bei MZ
									"k04" : {"key" : "invoice_id","label" : "Invoice No."},		# Rechnungsnummer der Eingangsrechnung, sofern erforderlich
									"k05" : {"key" : "amount","label" : "Payment Amount"},
									"k06" : {"key" : "due_date","label" : "Payment Due Date"}
								},
				"payment" : 	{	# any any payment recorded e.g. at bank account, credit incoming, debit outgoing
									"k01" : {"key" : "counterparty","label" : "Counterparty"},
									"k02" : {"key" : "payment type","label" : "Debit or Credit"},
									"k03" : {"key" : "amount","label" : "Payment Amount"},
									"k04" : {"key" : "payment_date_date","label" : "Payment Due Date"},
									"k05" : {"key" : "payment_id","label" : "Payment ID"},		# unique payment identifier
									"k06" : {"key" : "contract_id","label" : "Contract ID"},	# e.g. Aktenkennzeichen bei MZ
									"k07" : {"key" : "invoice_id","label" : "Invoice No."}		# Rechnungsnummer der Eingangsrechnung, sofern erforderlich
								},
				"publication" : {	# any any payment recorded e.g. at bank account, credit incoming, debit outgoing
									"k01" : {"key" : "source","label" : "Source"},
									"k02" : {"key" : "source_url","label" : "Source URL"},
									"k03" : {"key" : "publication_date","label" : "Publication Date"}
								},
				"receivable" : 	{	# any payable also arising out of contracts
									"k01" : {"key" : "debtor","label" : "Debtor"},
									"k02" : {"key" : "debtor_id","label" : "Debtor ID"},
									"k03" : {"key" : "contract_id","label" : "Contract ID"},
									"k04" : {"key" : "invoice_id","label" : "Invoice No."},		# Ausgangsrechnung, wenn vorhanden
									"k05" : {"key" : "amount","label" : "Receivable Amount"},	# Forderungssbetrag
									"k06" : {"key" : "due_date","label" : "Payment Due Date"}
								},
               "speech" : 		{	# personal speech fragments, to be used in some future presentations
									"k01" : {"key" : "source","label" : "Source"}
			   					},
               "thought" : 		{	# what comes to mind and is considered worth remembering, to do
									"k01" : {"key" : "source","label" : "Source"}
			   					},
               "usecase" : 		{	# any contract like credit, purchase, rent, insurance, etc.
									"k01" : {"key" : "source","label" : "Source"},
									"k02" : {"key" : "source_url","label" : "Source URL"},
									"k03" : {"key" : "reference_date","label" : "Reference Date"},		# date the fact refers to eg Population Desity as of 1.1.1900
									"k04" : {"key" : "publication_date","label" : "Publication Date"}
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

	CASHFLOW_TYPES = 	{
							"pay_out" : "Privatentnahme Gesellschafter",
							"pay_in" : "Privateinlage Gesellschafter"			
						}