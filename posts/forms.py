from wtforms import  Form, StringField, TextAreaField, validators

class PostForm(Form):
    title = StringField('Title', validators=[
        validators.DataRequired()
    ])
    body = TextAreaField('Body', validators=[
        validators.DataRequired()
    ])
    #tags = StringField('Tags')