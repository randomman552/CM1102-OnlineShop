# File to hold routes (we can split this into many separate files if it gets too big)
import os
import random
from flask_login import current_user, login_required
from flask import render_template, redirect, request, flash, url_for, session
from werkzeug.utils import secure_filename
from .forms import AddReviewForm
from .models import db, func, Product, Picture, Review, User, Wishlist, Category, ProductCategory
from . import app
import time

# TODO: Improve mobile experience


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

            # If it is set to grid, set the session variable and return
            if var_name in request.args:

                # If options have been specified
                if len(options) > 0:

                    # If the variable is one of the valid options, update the session variable
                    if request.args[var_name] in options:
                        session[var_name] = request.args[var_name]

                    # Otherwise revert to what it was set to before
                    else:
                        return build_new_url(var_name, session[var_name])

                # If options have not been specified, allow any variable to be assigned to any value
                else:
                    session[var_name] = request.args[var_name]

            # If the value is not set and not in the session, assign it's default value here
            elif var_name not in session:
                session[var_name] = options[0]
                return build_new_url(var_name, session[var_name])
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

    def get_products() -> (list, int):
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

            # Build subquerys used to filter by more advanced queries
            avg_rating = (db.session
                          .query(Review.productID, func.avg(Review.rating)
                                 .label("avg_rating"))
                          .group_by(Review.productID)
                          .subquery()
                          )

            rating_count = (db.session
                            .query(Review.productID, func.count(Review.productID)
                                   .label("rating_count"))
                            .group_by(Review.productID)
                            .subquery()
                            )

            # Apply joins for the previous subqueries
            products = (products
                        .outerjoin(avg_rating, Product.ID == avg_rating.c.productID)
                        .group_by(Product.ID)
                        )

            products = (products
                        .outerjoin(rating_count, Product.ID == rating_count.c.productID)
                        .group_by(Product.ID)
                        )

            # Set the sort key, this is overridden below to change how the products are sorted
            sort_key = Product.ID

            # This dict is used like a case statement to change the key variable
            key_dict = {
                "price": Product._price,
                "rating": avg_rating.c.avg_rating,
                "no.ratings": rating_count.c.rating_count,
                "mass": Product._mass,
                "surface_gravity": Product._surface_gravity,
                "orbital_period": Product._orbital_period
            }

            # Get the relevant variables
            sort = request.args['sort']
            order = request.args['order']

            # Go through each key in the key dict, and find one that is applied
            for key in key_dict:
                if sort == key:
                    sort_key = key_dict[key]
                    break

            # Apply the sort based on the order
            if order == "asc":
                products = (products
                            .order_by(sort_key.asc())
                            )
            elif order == "desc":
                products = (products
                            .order_by(sort_key.desc())
                            )

            # Return our updated query object
            return products

        def create_list(products) -> list:
            """
            This function takes the products query object and querys the database.\n
            It handles the limit set in the GET variable, and the current page number.\n
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

                # Get the current page number, default to 0 if not present.
                # This must be 0 indexed to allow for easily determining get offset
                page_num = 0
                if "page" in request.args:
                    try:
                        page_num = int(request.args["page"]) - 1
                    except:
                        pass

                # Attempt to get limit variable, if it fails then default to 20
                limit = 20
                try:
                    limit = int(request.args["limit"])
                except:
                    pass
                products = (products
                            .limit(int(request.args["limit"]))
                            .offset(page_num * limit)
                            .all()
                            )

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
                            .filter(Product.name.like(f"%{request.args['query']}%")))

            # Min price filtering
            if "minprice" in request.args:
                # Contained in a try loop to prevent any incorrect values from breaking the page
                try:
                    if request.args["minprice"]:
                        # Multiply by 100 as they are stored as integers after being multiplied by 100
                        min_price = round(
                            float(request.args["minprice"]) * 100)
                    else:
                        # Set to zero if not set in args
                        min_price = 0

                    # Apply the filter to the query
                    products = products.filter(Product._price >= min_price)
                except:
                    pass

            # Max price filtering
            if "maxprice" in request.args:
                try:
                    if request.args["maxprice"]:
                        max_price = round(
                            float(request.args["maxprice"]) * 100)
                    else:
                        max_price = 0
                    # If max_price is equal to 0, we should ignore it and not filter by max price
                    if max_price != 0:
                        products = products.filter(Product._price <= max_price)
                except:
                    pass

            # Product category filtering
            if "category" in request.args:
                # Attempt to get category value
                category = 0
                try:
                    if request.args["category"]:
                        category = int(request.args["category"])
                except:
                    pass

                # If the category is set (not null), then proceed to filter the products
                if category:
                    # Get the product category mappings from the database
                    product_categories = ProductCategory.query.filter(
                        ProductCategory.categoryID.like(category)).subquery()

                    # Join with products to get our allowed products
                    products = (products
                                .outerjoin(product_categories, Product.ID == product_categories.c.productID)
                                .group_by(Product.ID)
                                )

                    # Filter the products
                    products = products.filter(
                        product_categories.c.categoryID == category)

            # Return altered products query
            return products

        # Create the products variable
        products = Product.query.filter()

        # Filter the products query
        products = filter_products(products)

        # Sort the products query
        products = sort_products(products)

        # Get the maximum number of products created by this query (used for page system)
        product_count = len(products.all())

        # Get the products list produced by the query
        products = create_list(products)

        # Return our products list
        return products, product_count

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

        # Create a list of product IDs to get the pictures for
        product_ids = []
        for product in products:
            product_ids.append(product.ID)

        # Get pictures from the database
        pictures = Picture.query.filter(
            Picture.productID.in_(product_ids)).all()

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

        # Each rating in the list is a tuple,
        # the first element in the tuple is the average review score
        # and the second is the number of reviews

        # Return our list of ratings
        return ratings_return

    def get_categories() -> list:
        """Get the categories from the database and return them as a list of category objects.
        @return - A list of categories
        """

        categories = Category.query.all()
        return categories

    # Create the dict of required variables
    # THIS SHOULD ONLY BE DONE FOR VARIABLES WHICH SHOULD BE REMEMBERED BY THE SERVER (in session)
    var_dict = {
        "view": ["grid", "list"],
        "sort": ["rating", "price", "no.ratings", "mass", "surface_gravity", "orbital_period"],
        "order": ["desc", "asc"],
        "limit": ["20", "30", "all"]
    }
    # Call handle_vars, if it returns something (a redirect), return that.
    retval = handle_vars(var_dict)
    if retval:
        return retval

    # Get products and the maximum product count from the database, (this uses tuple unpacking)
    products, product_count = get_products()

    # Get pictures
    pictures = get_pictures(products)

    # Get ratings
    ratings = get_ratings(products)

    # Get the maximum number of pages
    limit = int(request.args["limit"])
    max_page = round((product_count / limit) + 0.5)

    # Get a list of all the categories from the database
    categories = get_categories()

    # Return the template
    return render_template("products/products.html",
                           products=products,
                           pictures=pictures,
                           ratings=ratings,
                           max_page=max_page,
                           categories=categories,
                           mode="edit")


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


@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def render_view_product(product_id):
    # Create a review form object
    review_form = AddReviewForm()

    # If the review form has been submitted, add the review to the database
    if review_form.validate_on_submit():
        userID = None
        if current_user.is_authenticated:
            userID = current_user.ID
        new_review = Review(rating=review_form.stars.data,
                            userID=userID,
                            content=review_form.comment.data,
                            productID=product_id)
        db.session.add(new_review)
        db.session.commit()
        return redirect(request.base_url)

    product = Product.query.filter(Product.ID.like(product_id)).first()
    pictures = Picture.query.filter(Picture.productID.like(product_id)).all()
    reviews = Review.query.filter(Review.productID.like(product_id)).all()
    users_temp = User.query.filter()

    # Create review subquery to join with
    review_subquery = Review.query.subquery()

    users_temp = users_temp.outerjoin(
        review_subquery, review_subquery.c.userID == User.ID).all()

    # Make users list the right format (in order for reviews)
    users = []
    for review in reviews:
        # For each user in the temp list
        for user in users_temp:
            # If a user in the temp list matches the user who wrote the review,
            # append that user to the list
            if user.ID == review.userID:
                users.append(user)
        else:
            # If we finish the loop through users and did not find a match, add a None
            users.append(None)

    review_avg = (db.session
                  .query(func.avg(Review.rating)
                         .label("average"))
                  .filter(Review.productID == product_id)
                  .first()[0]
                  )
    review_count = (db.session
                    .query(func.count(Review.rating)
                           .label("average"))
                    .filter(Review.productID == product_id)
                    .first()[0]
                    )

    # If the avg or count are not set, set them to 0
    if not review_avg:
        review_avg = 0

    # Render the template
    return render_template(
        "products/view_product.html",
        product=product,
        pictures=pictures,
        reviews=reviews,
        review_avg=review_avg,
        review_count=review_count,
        review_form=review_form,
        users=users
    )
