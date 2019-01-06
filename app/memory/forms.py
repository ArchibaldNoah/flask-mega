from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FieldList, TextAreaField  #, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Memory, Tag, MemoryTag



class NewMemoryForm(FlaskForm):

    type = SelectField('Type', choices=[('account','Account'),
                                          ('citation','Citation'),
                                          ('fact','Fact'),        	# facts to be remembered, e.g. world oil production 
                                          ('news','News'),		# news
                                          ('publication','Publication'),# documents worth reading
                                          ('speech','Speech'),		# personal speech fragments
                                          ('thought','Thought'),	# what comes to mind and is considered worth remembering
                                          ('transaction','Transaction'),# contract with another entity/person
                                          ('usecase','Usecase')],	# usecases worth remembering, e.g. big data use cases
                                          default='news')

    category = SelectField('Type', choices=[('business','Business'),		# e.g. company news
                                           ('finance','Finance'),		# e.g. stock prices
                                           ('sustainability','Sustainability'), # e.g. global warming, evs, batteries
                                           ('tech','Tech'),               	# technology related, e.g. Big Data, Machine Learning  
                                           ('other','Other')])			# the rest

    abstract = TextAreaField('Abstract', validators=[DataRequired(), Length(min=1,max=256)])
    
    tags = StringField('Tags', validators=[DataRequired()])


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
    
