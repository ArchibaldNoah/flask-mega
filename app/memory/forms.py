from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FieldList, TextAreaField  #, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Memory, Tag, MemoryTag



class NewMemoryForm(FlaskForm):

    memorize = SubmitField("Memorize")
    reselect = SubmitField("Reselect Filter")
    slcType = SelectField('Type', choices=[('iAccount','Internet Account'),        # internet konto informationen, e.g. Moodys
                                          ('Citation','Citation'),  # Zitate berühmter Leute oder z.B. meiner Kinder
                                          ('Contract','Contract'),  # contract with another entity/person, receivables, payables
                                          ('Document','Document'),  # contract with another entity/person, receivables, payables
                                          ('Fact','Fact'),        	# facts to be remembered, e.g. world oil production 
                                          ('News','News'),		    # news
                                          ('Payable','Payable'),    # empfangene Rechnungen
                                          ('Payment','Payment'),    # payments made and payments received
                                          ('Publication','Publication'),# documents worth reading
                                          ('Receivable','Receivable'),  # gestellte Rechnungen, forderungen gegen andere
                                          ('Speech','Speech'),		# personal speech fragments, to be used in some future presentations
                                          ('Thought','Thought'),	# what comes to mind and is considered worth remembering, to do
                                          ('Usecase','Usecase')],	# usecases worth remembering, e.g. big data use cases
                                          default='news')

    slcCategory = SelectField('Type', choices=[('Business','Business'),		# e.g. company news, own business
                                            ('Finance','Finance'),		    # e.g. markets, stock prices
                                            ('Home','Home'),                 # e.g. around home including personal finance issues
                                            ('MZ-Patent','MZ-Patent'),            # in relation to family business
                                            ('Sustainability','Sustainability'), # e.g. global warming, evs, batteries, demography
                                            ('Tech','Tech'),               	# technology related, e.g. Big Data, Machine Learning, Engineering
                                            ('Other','Other')])			    # the rest

    tafAbstract = TextAreaField('Abstract', validators=[DataRequired(), Length(min=1,max=256)])
    
    strTags = StringField('Tags', validators=[DataRequired()])

    sbmApplyFilter = SubmitField('Apply Filter')

    sbmBack = SubmitField('Back')

    sbmMemorize = SubmitField('Memorize')

class ViewDeleteMemoryForm(FlaskForm):

    memorize = SubmitField("Memorize", render_kw={'readonly': True})
    reselect = SubmitField("Reselect Filter", render_kw={'readonly': True})
    slcType = StringField('Type', render_kw={'readonly': True})
    slcCategory = StringField('Tags', render_kw={'readonly': True})	
    tafAbstract = TextAreaField('Abstract', render_kw={'readonly': True})
    strTags = StringField('Tags', render_kw={'readonly': True})
    sbmBack = SubmitField('Back', render_kw={'readonly': True})
    sbmDelete = SubmitField('Forget ?', render_kw={'readonly': True})

class EditMemoryForm(FlaskForm):
    id = StringField('id', render_kw={'readonly': True})
    type = SelectField('Type', choices=[('iAccount','Internet Account'),          # internet konto informationen, e.g. Moodys
                                          ('Citation','Citation'),  # Zitate berühmter Leute oder z.B. meiner Kinder
                                          ('Contract','Contract'),  # contract with another entity/person, receivables, payables
                                          ('Document','Document'),  # contract with another entity/person, receivables, payables
                                          ('Fact','Fact'),        	# facts to be remembered, e.g. world oil production 
                                          ('News','News'),		    # news
                                          ('Payable','Payable'),    # empfangene Rechnungen
                                          ('Payment','Payment'),    # payments made and payments received
                                          ('Publication','Publication'),# documents worth reading
                                          ('Receivable','Receivable'),  # gestellte Rechnungen, forderungen gegen andere
                                          ('Speech','Speech'),		# personal speech fragments, to be used in some future presentations
                                          ('Thought','Thought'),	# what comes to mind and is considered worth remembering, to do
                                          ('Usecase','Usecase')],	# usecases worth remembering, e.g. big data use cases
                                          default='news')

    category = SelectField('Type', choices=[('Business','Business'),		# e.g. company news
                                            ('Finance','Finance'),		    # e.g. markets, stock prices
                                            ('Home','Home'),                 # e.g. around home including personal finance issues
                                            ('MZ-Patent','MZ-Patent'),            # in relation to family business
                                            ('Sustainability','Sustainability'), # e.g. global warming, evs, batteries, demography
                                            ('Tech','Tech'),               	# technology related, e.g. Big Data, Machine Learning, Engineering
                                            ('Other','Other')])			    # the rest
    abstract = TextAreaField('Abstract')
    tags = TextAreaField('Tags', validators=[DataRequired(),Length(min=1,max=256)])
    posted = StringField('Posted on', render_kw={'readonly': True})
    memorize = SubmitField('memorize')
    keep = SubmitField('do not')

class ForgetForm(FlaskForm):
    id = StringField('id')
    type = StringField('Type', render_kw={'readonly': True})
    category = StringField('Category', render_kw={'readonly': True})
    abstract = TextAreaField('Abstract', render_kw={'readonly': True})
    tags = TextAreaField('Tags', render_kw={'readonly': True}, validators=[DataRequired(),Length(min=1,max=256)])
    posted = StringField('Posted on', render_kw={'readonly': True})
    keep = SubmitField('keep')
    forget = SubmitField('forget')
# class EditMemoryForm(FlaskForm):

# Subform in memory/index which holds the filter parameters
class MemoryFilterForm(FlaskForm):

    slcType = SelectField('Type', choices=[('Any','Any'),                   # al are fine
                                          ('iAccount','Internet Account'),  # internet konto informationen, e.g. Moodys
                                          ('Citation','Citation'),  # Zitate berühmter Leute oder z.B. meiner Kinder
                                          ('Contract','Contract'),  # contract with another entity/person, receivables, payables
                                          ('Document','Document'),  # contract with another entity/person, receivables, payables
                                          ('Fact','Fact'),        	# facts to be remembered, e.g. world oil production 
                                          ('News','News'),		    # news
                                          ('Payable','Payable'),    # empfangene Rechnungen
                                          ('Payment','Payment'),    # payments made and payments received
                                          ('Publication','Publication'),# documents worth reading
                                          ('Receivable','Receivable'),  # gestellte Rechnungen, forderungen gegen andere
                                          ('Speech','Speech'),		# personal speech fragments, to be used in some future presentations
                                          ('Thought','Thought'),	# what comes to mind and is considered worth remembering, to do
                                          ('Usecase','Usecase')],	# usecases worth remembering, e.g. big data use cases
                                    default='Any')

    slcCategory = SelectField('Category', choices=[('Any','Any'),
                                            ('Business','Business'),		# e.g. company news
                                            ('Finance','Finance'),		    # e.g. markets, stock prices
                                            ('Home','Home'),                 # e.g. around home including personal finance issues
                                            ('MZ-Patent','MZ-Patent'),            # in relation to family business
                                            ('Sustainability','Sustainability'), # e.g. global warming, evs, batteries, demography
                                            ('Tech','Tech'),               	# technology related, e.g. Big Data, Machine Learning, Engineering
                                            ('Other','Other')],			    # the rest		
                                            default='Any')

    stfTags = StringField('Tags')

    sbmFilterOnOff = SubmitField('Filter On/Off')

    sbmApply = SubmitField('do not')

    filter_status_string = 'Filter is off'
