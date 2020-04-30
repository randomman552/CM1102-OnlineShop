from flask_admin.contrib.sqla import ModelView
import flask_login as login
from shop.models import User
from flask_admin import expose

# The views in this file are used on the admin panel page


class ProductView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    form_columns = ['name', 'public', '_price', 'description',
                    '_mass', '_surface_gravity', '_orbital_period']
    column_list = ['ID' , 'name', 'public', '_price', 'description',
                    '_mass', '_surface_gravity', '_orbital_period']
    column_searchable_list = ['name']

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
    column_searchable_list = ['categoryID', 'productID']
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
    column_searchable_list = ['productID']
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
    column_searchable_list = ['name']
    column_list = ['ID', 'name']

    def is_accessible(self):
        if login.current_user.is_authenticated:
            if login.current_user.get_id():
                user = User.query.get(login.current_user.get_id())
                return user.is_admin
        return False


class ReviewView(ModelView):
    column_display_pk = True
    column_hide_backrefs = False
    column_searchable_list = ['productID']
    column_list = ['ID', 'productID', 'rating', 'content']

    def is_accessible(self):
        if login.current_user.is_authenticated:
            if login.current_user.get_id():
                user = User.query.get(login.current_user.get_id())
                return user.is_admin
        return False
