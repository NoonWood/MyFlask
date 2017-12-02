from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#import models
#
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
#
from config import Configuration  # Инпорт конфигураций
from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user

from flask import redirect, request, url_for

from flask_security.forms import RegisterForm
from wtforms import StringField

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)

#
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
#



        #Admin#
from models import *
#Перенаправление на регистрацию
class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()#генерация новогро slug
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

#определяют внешний вид моделей
class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title','body','tags']

class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ['name','posts']

class UserAdminView(AdminMixin, ModelView):
    form_columns = ['nickname','roles']

admin = Admin(app, 'AdminApp', url='/', index_view=HomeAdminView('Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(UserAdminView(User, db.session))

###Flask security

class ExtendedRegisterForm(RegisterForm):
    nickname = StringField('Nickname', [])



user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)
