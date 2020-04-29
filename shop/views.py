from flask_admin.contrib.sqla import ModelView
import flask_login as login
from shop.models import User
from flask_admin import expose

class AdminView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        if login.current_user.is_authenticated:
            if login.current_user.get_id():
                user = User.query.get(login.current_user.get_id())
                return user.is_admin
        return False

class pCategoryView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    form_columns = ['categoryID', 'productID']
    column_list = ['ID', 'categoryID', 'productID']

    def is_accessible(self):
        if login.current_user.is_authenticated:
            if login.current_user.get_id():
                user = User.query.get(login.current_user.get_id())
                return user.is_admin
        return False

class PictureView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    form_columns = ['productID', 'URL']
    column_list = ['ID', 'productID', 'URL']

    def is_accessible(self):
        if login.current_user.is_authenticated:
            if login.current_user.get_id():
                user = User.query.get(login.current_user.get_id())
                return user.is_admin
        return False
        
class CategoryView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_list = ['ID', 'name']

    def is_accessible(self):
        if login.current_user.is_authenticated:
            if login.current_user.get_id():
                user = User.query.get(login.current_user.get_id())
                return user.is_admin
        return False
