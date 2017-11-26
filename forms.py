
from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])#проверка на пустое поле
    remember_me = BooleanField('remember_me', default = False)




