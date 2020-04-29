# Any code we want to run before creating any routes or models should be put in here
from flask import Flask, redirect, flash
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_admin import Admin
import os

# Setup the flask app
app = Flask(__name__)
app.secret_key = b'T\xb8\xb8\x84\xa4\x17J\x07\xb7A\xd4\xca8\xcb1\xfb\xda\t\x81\x0b\xfa\x1e\xde['

#Initalise bootstrap
bootstrap = Bootstrap(app)

#Initalise the login manager
login_manager = LoginManager()
login_manager.init_app(app)


#Imports from lower level packages
from . import routes
from shop.views import AdminView
from shop.models import db, User, Product, Category, ProductCategory, Wishlist, Picture, Review, User, read_json
from shop.views import ModelView, PictureView, AdminView, pCategoryView, AdminView

admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))
admin.add_view(PictureView(Picture, db.session))
admin.add_view(AdminView(Category, db.session))
admin.add_view(pCategoryView(ProductCategory, db.session))
admin.add_view(AdminView(Review, db.session))

#User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#TODO: Make it redirect you to the previous page you were on instead of login?
#Redirect for when user is unauthorised
@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view that page.")
    return redirect("/login")


#The code section below is only used when some environment variables are set
sample_data_location = "shop/config/sample_data.json"

# If the environment variable "SHOP_CLEAR_DATA" is set to "1", this will drop all tables from the database
if bool(os.getenv("SHOP_CLEAR_DATA", "")):
    # THIS DOES NOT DELETE THE TABLES, IT ONLY CLEARS THE DATA
    Review.query.delete()
    Wishlist.query.delete()
    Picture.query.delete()
    ProductCategory.query.delete()
    Category.query.delete()
    User.query.delete()
    Product.query.delete()

# If the environment variable "SHOP_SAMPLE_DATA" is set to "1",
# this will load the data in the sample data file and put it in the database
# This code could be stripped out in a production setting
if bool(os.getenv("SHOP_SAMPLE_DATA", "")):

    # Print status
    print(f"Loading data from: '{sample_data_location}'")

    def load_categories(categories: list) -> dict:
        """
        Load the category data into the database.\n
        @param categories - A list of strings, each string is a category name.\n
        @return - A dict mapping category name to ID.
        """

        # Get the already existing categories
        existing = Category.query.all()
        # Get just the name of each element
        for i in range(len(existing)):
            existing[i] = existing[i].name

        # Create category objects for each string in the categories list (if it isn't already present)
        for category in categories:
            if category not in existing:
                new_category = Category(name=category)
                db.session.add(new_category)

        # Commit our changes
        db.session.commit()

        # Create the category mapping dict
        categories = Category.query.all()
        mapping = dict()
        for category in categories:
            mapping[category.name] = category.ID

        # Return our category mapping
        return mapping

    def load_products(products: list, category_map: dict, user_map: dict) -> dict:
        """
        Load the product data into the database. Also sets the product categories, pictures and reviews.\n
        @param products - A list of dicts for the products.\n
        @param category_map - The dict mapping category name to ID.\n
        @param user_map - The dict mapping user email to ID.\n
        @return - A dict mapping product name to ID.
        """

        # Get a list of all existing products
        existing = Product.query.all()

        # Convert into list of taken names
        for i in range(len(existing)):
            existing[i] = existing[i].name

        # Add each product in the list to the database
        for product in products:
            if product["name"] not in existing:
                # Price is divided by 100 before entry so it can be entered normally in json file
                new_product = Product(name=product.get("name", "Product Name"),
                                      _price=product.get("price", 0),
                                      public=True,
                                      description=product.get("description", ""),
                                      _mass=product.get("mass", -1),
                                      _surface_gravity=product.get("surface gravity", -1),
                                      _orbital_period=product.get("orbital period", -1)
                                      )
                db.session.add(new_product)

        # Commit changes
        db.session.commit()

        # Make the product map
        product_map = dict()
        all_products = Product.query.all()
        for product in all_products:
            product_map[product.name] = product.ID

        # Add other elements to the product
        for product in products:

            # Add categories
            for category in product.get("categories", []):
                new_category = ProductCategory(productID=product_map.get(product.get("name")),
                                               categoryID=category_map.get(
                                                   category)
                                               )
                db.session.add(new_category)

            # Add pictures
            for picture in product.get("pictures", []):
                new_picture = Picture(productID=product_map.get(product.get("name", "Product Name")),
                                      URL=picture
                                      )
                db.session.add(new_picture)

            # Add reviews
            for review in product.get("reviews", []):
                new_review = Review(productID=product_map[product.get("name")],
                                    userID=user_map.get(review.get("author")),
                                    rating=review.get("rating", 5),
                                    content=review.get("comment", "")
                                    )
                db.session.add(new_review)

        # Commit categories, pictures, and reviews
        db.session.commit()

        # Return the product map
        return product_map

    def load_users(users: list) -> dict:
        """
        Load the user data into the database.\n
        @param users - A list of user dicts to make.\n
        @return - A dict mapping user email to ID.
        """
        
        # Get the already existing users
        existing = User.query.all()
        # Get just the email for each element
        for i in range(len(existing)):
            existing[i] = existing[i].email

        # Create user objects for each string in the categories list (if it isn't already present)
        for user in users:
            if user["email"] not in existing:
                new_user = User(
                    email=user.get("email"), password=user.get("password"), is_admin=user.get("admin", False))
                db.session.add(new_user)

        # Commit our changes
        db.session.commit()

        # Create the user mapping dict
        users = User.query.all()
        mapping = dict()
        for user in users:
            mapping[user.email] = user.ID

        # Return our user mapping
        return mapping

    sample_data = read_json(sample_data_location)

    category_map = load_categories(sample_data.get("categories", []))

    user_map = load_users(sample_data.get("users", []))

    product_map = load_products(sample_data.get("products", []), category_map, user_map)

    print("Finished data loading")
