from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length
from app.models import User

class LoginForm(FlaskForm):
    openid = StringField('openid',validators=[DataRequired()])
    remember_me = BooleanField('remember_me',default=False)


class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me',validators=[Length(min=0,max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            suggestion = User.make_unique_nickname(self.nickname.data)
            self.nickname.errors.append('Sorry, the nickname %s is already in use, please choose another. You could try %s.' %(self.nickname.data,suggestion))
            suggestion = User.make_unique_nickname(self.nickname.data)
            return False
        return True


