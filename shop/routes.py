# File to hold routes (we can split this into many separate files if it gets too big)
import os
import random
from flask import render_template, redirect, request, flash, url_for, session
from werkzeug.utils import secure_filename
from .forms import *
from .models import db, func, Product, Picture, Review
from . import app
import time


@app.route("/")
def render_home():
    return render_template("layout.html")


@app.route("/products")
def render_products():
    def handle_vars(variable_list: dict):
        """Handle setting of session variables for product display.\n
        @param variable_list - A dict, each entry in the dict is a variable name (str),
        and the corresponding value is a list of options for that variable.\n
        @return - Will return a redirect if a GET variable is to be updated, otherwise will return none.
        """

        def build_new_url(name: str, value: str):
            """
            Builds a new url containing the new get variable.\n
            @param name - The name of the variable to assign\n
            @param value - The value of the variable (as a string)\n
            @return - A url in the form of a string
            """
            # Build a redirect to set the get variable
            temp = []

            # For each arg in the request, recreate the GET string for that arg
            for arg in request.args:
                # Make sure to not append the same GET variable to the url
                if arg != name:
                    temp.append(f"{arg}={request.args[arg]}")

            # Add our new arg to the list
            temp.append(f"{name}={value}")

            # Create the base url and add all the args to it
            url = f"{request.base_url}?"
            for arg in temp:
                url += f"{arg}&"

            # Remove the trailing '&' from the url
            url = url[:-1]
            # Return the url
            return url

        def setup_var(var_name: str, options: list) -> str:
            """Generalised function for setting up session variables for GET arguments.\n
            @param var_name - The name of the variable to setup\n
            @param options - A list of options, the first one of these will be used as the default value.\n
            @return - A string containing the redirect URL, or an empty string if GET variable is present.
            """

            # Check if the variable has a session value, if it doesnt then create one for it and update the url
            if not(var_name in session):
                # If the options list has more than 0 members, take the first as the default
                # Otherwise assign an empty string
                if len(options) > 0:
                    session[var_name] = options[0]
                else:
                    session[var_name] = ""
                return build_new_url(var_name, session[var_name])
            # If it is set to grid, set the session variable and return
            if var_name in request.args:

                # If options have been specified
                if len(options) > 0:
                    # If the variable is one of the valid options, update the session variable
                    if request.args[var_name] in options:
                        # Otherwise revert to what it was set to before
                        session[var_name] = request.args[var_name]
                    else:
                        return build_new_url(var_name, session[var_name])
                # If options have not been specified, allow any variable to be assigned
                else:
                    session[var_name] = request.args[var_name]
            else:
                return build_new_url(var_name, session[var_name])

                # If view is in the GET args, we do not need to rebuild the url to contain it.
            # Return an empty string
            return ""

        # For each of the variables, call the setup_var function
        for variable in variable_list:
            # Call setup_var with the appropriate arguments
            retval = setup_var(variable, variable_list[variable])
            # If the return value is not an empty string, then return a redirect to it
            if retval:
                return redirect(retval)
        # After the loop ends normally (without breaking)
        else:
            return None

    def get_products() -> list:
        """
        This function gets the relevant products from the database and filters them according to user input.
        @return - A list of products
        """

        # Local functions (to split the process up a bit)

        def sort_products(products):
            """
            This function handles the ordering of the products.\n
            It checks the request.args variables to determine how to order the products.\n
            @param products - The query object to be ordered.\n
            @return - The query object with sorting applied.
            """
            sort = request.args['sort']
            order = request.args['order']
            # TODO: Reformat this to have less if statements (use a key variable to handle the final sort?)
            # If a sort is specified
            if sort != "none":
                # If we are sorting by price
                if sort == "price":
                    # If we are ordering by ascending order
                    if order == "asc":
                        products = (products
                                    .order_by(Product._price.asc())
                                    )

                    # If we are ordering by descending order
                    elif order == "desc":
                        products = (products
                                    .order_by(Product._price.desc())
                                    )
                # If we are sorting by rating
                elif sort == "rating":
                    # Calculate average rating for each product
                    avg_rating = (db.session
                                  .query(Review.productID, func.avg(Review.rating)
                                         .label("avg_rating"))
                                  .group_by(Review.productID)
                                  .subquery()
                                  )

                    # Join the average rating onto the products for sorting
                    products = (products
                                .outerjoin(avg_rating, Product.ID == avg_rating.c.productID)
                                .group_by(Product.ID)
                                )

                    # If we are ordering by asc
                    if order == "asc":
                        products = (products
                                    .order_by(avg_rating.c.avg_rating.asc())
                                    )

                    # If we are ordering by desc
                    if order == "desc":
                        products = (products
                                    .order_by(avg_rating.c.avg_rating.desc())
                                    )

                # If we are sorting by number of ratings
                elif sort == "no.ratings":
                    # Get the number of ratings for each product
                    rating_count = (db.session
                                    .query(Review.productID, func.count(Review.productID)
                                           .label("rating_count"))
                                    .group_by(Review.productID)
                                    .subquery()
                                    )

                    # Join the rating count onto the products query for sorting
                    products = (products
                                .outerjoin(rating_count, Product.ID == rating_count.c.productID)
                                .group_by(Product.ID)
                                )

                    # If we are ordering by asc
                    if order == "asc":
                        products = (products
                                    .order_by(rating_count.c.rating_count.asc())
                                    )

                    # If we are ordering by desc
                    if order == "desc":
                        products = (products
                                    .order_by(rating_count.c.rating_count.desc())
                                    )

            # Return our updated query object
            return products

        def create_list(products) -> list:
            """
            This function takes the products query object and querys the database.\n
            It handles the limit set in the GET variable.\n
            It then returns a list of the products.\n
            @param products - The query object to get from.\n
            @return - A list containg the query results.
            """
            # Handle the product limit per page
            if request.args["limit"] == "all":
                # If the request is for all products, put all products in the products list
                products = products.all()
            else:
                # If the limit variable is set to anything else, attempt to limit the results.
                # This will fail if the user puts a non-number into the limit get variable
                try:
                    products = (products
                                .limit((int(request.args["limit"])))
                                .all()
                                )
                except:
                    products = products.all()

            # Return our products list
            return products

        def filter_products(products):
            """
            This function applys any user applied filters, including search query.\n
            @param products - The query to apply filters too\n
            @return - The query object with filters applied
            """
            # If a query is present, and it is not null, filter the results.
            if "query" in request.args and request.args["query"]:

                # Fitler the results with the query, look at the description and name of products.
                products = (products
                            .filter(
                                (Product.name.like(f"%{request.args['query']}%") | Product.description.like(f"%{request.args['query']}%")))
                            )

            # TODO: Add more filtering types (by category etc)
            # Return altered products query
            return products

        # Create the products variable
        products = Product.query.filter()

        # Filter the products query
        products = filter_products(products)

        # Sort the products query
        products = sort_products(products)

        # Get the products list produced by the query
        products = create_list(products)

        # Return our products list
        return products

    # TODO: Could improve the functions for getting pictures and ratings
    # using a join method like the one for the sort in the products function
    def get_pictures(products: list) -> list:
        """
        Get the relevant pictures from the database.\n
        @param products - The list of products to get the pictures for\n
        @return - A list of lists containing the pictures for the corresponding products in the products list
        """

        # Setup return list with lists for each product
        pictures_return = [[] for _ in range(len(products))]

        # If the products list is empty, return an empty list
        if len(products) == 0:
            return pictures_return

        # Generate lowest and highest ID variables, these are used to constrain the pictures we get from the database
        lowestID = products[0].ID
        highestID = products[0].ID

        # Initalise pictures_return and get highest and lowest ID.
        for i in range(len(products)):
            if products[i].ID < lowestID:
                lowestID = products[i].ID
            elif products[i].ID > highestID:
                highestID = products[i].ID

        # Get pictures from the database
        pictures = Picture.query.filter(Picture.productID <= highestID).filter(
            Picture.productID >= lowestID).all()

        # Append the corresponding pictures to the correct list
        for i in range(len(products)):
            for picture in pictures:
                if picture.productID == products[i].ID:
                    pictures_return[i].append(picture)
        return pictures_return

    def get_ratings(products: list) -> list:
        """
        Get the relevant rating averages from the database.\n
        @param products - The list of products to get the average ratings for.\n
        @return - A list of average ratings, position of each rating matches the product list.
        """

        # Setup return list with lists for each product
        ratings_return = [[] for _ in range(len(products))]

        # This is really slow if you have high ping to the sql server, as it requires multiple sql requests
        # Append the corresponding pictures to the correct list
        for i in range(len(products)):
            # Get the average rating and add that to the list
            avg_rating = db.session.query(func.avg(Review.rating).label(
                "average")).filter(Review.productID == products[i].ID).first()[0]
            if avg_rating:
                ratings_return[i].append(float(avg_rating))
            else:
                ratings_return[i].append(0)

            # Get the number of ratings and add that to the list
            count = db.session.query(func.count(Review.rating).label("count")).filter(
                Review.productID == products[i].ID).first()
            ratings_return[i] += count

        # Return our list of ratings
        return ratings_return

    # Create the dict of required variables
    var_dict = {
        "view": ["grid", "list"],
        "sort": ["no.ratings", "price", "rating"],
        "order": ["desc", "asc"],
        "limit": ["20", "all"]
    }
    # Call handle_vars, if it returns something (a redirect), return that.
    retval = handle_vars(var_dict)
    if retval:
        return retval

    # Get products and pictures from the database
    products = get_products()
    pictures = get_pictures(products)
    ratings = get_ratings(products)

    return render_template("products/products.html", products=products, pictures=pictures, ratings=ratings, mode="edit")


@app.route("/products/new", methods=["GET", "POST"])
def render_new_product():
    # Give the new product a random name, which we can then use to get its ID from the database
    random_name = str(random.randint(0, 500000000))
    new_product = Product(name=random_name)
    # Add product to database
    db.session.add(new_product)
    db.session.commit()
    # Extract the newly created product and redirect to the edit page for it
    new_product = Product.query.filter(Product.name.like(random_name)).first()
    # Change the product name from the random one
    new_product.name = "Product name"
    db.session.commit()
    return redirect(f"/products/{new_product.ID}")


@app.route("/products/<int:product_id>", methods=["GET"])
def render_view_product(product_id):
    product = Product.query.filter(Product.ID.like(product_id)).first()
    pictures = Picture.query.filter(Picture.productID.like(product_id)).all()
    return render_template("products/view_product.html", product=product, pictures=pictures, mode="edit")
