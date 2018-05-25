from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length
from app.models import User,Answer,Hipe

class LoginForm(FlaskForm):
    openid = StringField('openid',validators=[DataRequired()])
    remember_me = BooleanField('remember_me',default=False)


class EditForm(FlaskForm):
    display_name = StringField('username', validators=[DataRequired()])
    about_me = TextAreaField('about_me',validators=[Length(min=0,max=140)])

    def __init__(self, original_display_name, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_display_name= original_display_name

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        return True

class AnswerForm(FlaskForm):
    answer = StringField('answer',validators=[DataRequired()])
    def __init__(self, hipe, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.hipe = hipe 

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        letters = self.hipe.letters
        if letters not in self.answer.data.lower():
            self.answer.errors.append('The letters %s are not in the word %s, try again.' %(letters,self.answer.data))
            return False

        answer = Answer.query.filter_by(answer=self.answer.data.lower()).filter_by(hipe=self.hipe).first()
        if answer != None:
            return True 
        else: 
            self.answer.errors.append('I do not think that %s is a word. Am I wrong?' %self.answer.data)
            return False



        




class PostForm(FlaskForm):
    post = StringField('post', validators = [DataRequired()])

