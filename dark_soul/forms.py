from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
#from flask.ext.wtf.html5 import URLField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Email, Regexp,\
EqualTo, ValidationError


from dark_soul.models import User


class BookmarkForm(FlaskForm):
    '''
    from derived from wtform
    '''

    #url = URLField('url', validators=[DataRequired(), url()])
    '''notice if using URLField then it will validate the content once you
    input a string, even though you haven't post submit yet'''

    url = StringField('The URL for your book mark:', validators=[DataRequired(), url()])
    description = StringField('Add an optional description:')

    def validate(self):
        '''
        override the validate function of FlaskForm, it is used when checking
        validate_on_submit()
        '''
        urldata = self.url.data

        if not urldata.startswith('https://') and not urldata.startswith('http://'):
            self.url.data = 'https://' + self.url.data

        if not FlaskForm.validate(self):
            return False

        if not self.description.data:
            self.description.data = self.url.data

        return True


class LoginForm(FlaskForm):
    '''
    this is the form for login page
    '''
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    '''
    this is the form for sign up page
    '''
    username = StringField('Username:',
                            validators=[DataRequired(), Length(3, 80),
                                        Regexp('^[A-Za-z0-9_]{3,}$',
                                                message='User name consists\
                                                of numbers, letters and\
                                                underscores.'
                                                )])

    password = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField('Confirm password:',
                                validators=[DataRequired(),
                                            EqualTo('password',
                                                    message='password unmatch.'
                                                    )])

    email = StringField('Email', validators=[DataRequired(), Length(3, 80), Email()])

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('Email is already registered.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('User name is already registered.')

    #submit = SubmitField('Login')
