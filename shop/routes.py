#File to hold routes (we can split this into many separate files if it gets too big)
import os
import random
from flask import render_template, redirect, request, flash, url_for, session
from werkzeug.utils import secure_filename
from .forms import *
from .models import db, Product, Picture
from . import app
import time

@app.route("/")
def render_home():
    return render_template("layout.html")

@app.route("/products")
def render_products():
    def handle_views(variable_list:dict):
        """Handle setting of session variables for product display.\n
        This will return a redirect if a required GET variable is missing from the url.\n
        @param variable_list - A dict, each entry in the dict is a variable name (str), 
        and the corresponding value is a list of options for that variable
        """
        
        def setup_var(var_name:str, options:list) -> str:
            """Generalised function for setting up session variables for GET arguments.\n
            @param var_name - The name of the variable to setup\n
            @param options - A list of options, the first one of these will be used as the default value.\n
            @return - A string containing the redirect URL, or an empty string if GET variable is present.
            """

            #If it is set to grid, set the session variable and return
            if var_name in request.args:

                #If the variable is one of the valid options, update the session variable
                if request.args[var_name] in options:
                    session[var_name] = request.args[var_name]
                
                #If view is in the GET args, we do not need to rebuild the url to contain it.
                #So we can return
                return ""
            else:
                #If the session variable is not setup, set it to the default value (first in the options list)
                if not(var_name in session):
                    session[var_name] = options[0]

                #Build a redirect to set the get variable
                temp = []

                #For each arg in the request, recreate the GET string for that arg
                for arg in request.args:
                    temp.append(f"{arg}={request.args[arg]}")

                #Add our new arg to the list
                temp.append(f"{var_name}={session[var_name]}")

                #Create the base url and add all the args to it
                url = f"{request.base_url}?"
                for arg in temp:
                    url += f"{arg}&"

                #Remove the trailing '&' from the url
                url = url[:-1]

                #Return the url
                return url
        
        #For each of the variables, call the setup_var function
        for variable in variable_list:
            #Call setup_var with the appropriate arguments
            retval = setup_var(variable, variable_list[variable])
            #If the return value is not an empty string, then return a redirect to it
            if retval:
                return redirect(retval)
        #After the loop ends normally (without breaking)
        else:
            return None

    def get_products():
        """This function gets the relevant products from the database and filters them according to user input."""
        products = []

        #If a query is present, and it is not null, filter the results.
        if "query" in request.args and request.args["query"]:

            #Fitler the results with the query, look at the description and name of products.
            products = Product.query.filter(Product.name.like(f"%{request.args['query']}%"))
            products += Product.query.filter(Product.description.like(f"%{request.args['query']}%"))
            #TODO: ADD CATEGORY FILTERING
            #Remove any duplicates
            already_present = []
            for product in products:
                if product.ID in already_present:
                    products.remove(product)
                else:
                    already_present.append(product.ID)
        else:
            products = Product.query.filter()

        #Handle the product limit per page
        if request.args["limit"] == "all":
            #If the request is for all products, put all products in the products list
            products = products.all()
        else:
            #If the limit variable is set to anything else, attempt to limit the results.
            #This will fail if the user puts a non-number into the limit get variable
            try:
                products = products.limit((int(request.args["limit"]))).all()
            except:
                products = products.all()
        return products
    
    def get_pictures(products:list):
        """Get the relevant pictures from the database."""
        #Setup return list with slots for each product
        pictures_return = []

        #If the products list is empty, return an empty list
        if len(products) == 0:
            return pictures_return
        
        #Generate lowest and highest ID variables, these are used to constrain the pictures we get from the database
        lowestID = products[0].ID
        highestID = products[0].ID

        #Initalise pictures_return and get highest and lowest ID.
        for i in range(len(products)):
            if products[i].ID < lowestID:
                lowestID = products[i].ID
            elif products[i].ID > highestID:
                highestID = products[i].ID
            pictures_return.append([])

        #Get pictures from the database
        pictures = Picture.query.filter(Picture.productID <= highestID).filter(Picture.productID >= lowestID).all()

        #Append the corresponding pictures to the correct list
        for i in range(len(products)):
            for picture in pictures:
                if picture.productID == products[i].ID:
                    pictures_return[i].append(picture)
        return pictures_return
    
    #Create the dict of required variables
    var_dict = {
        "view": ["grid", "list"],
        "sort": ["price", "rating"],
        "order": ["asc", "dsc"],
        "limit": ["20", "all"]
    }
    #Call handle_views, if it returns something, return it.
    retval = handle_views(var_dict)
    if retval:
        return retval
    
    #Get products and pictures from the database
    products = get_products()
    pictures = get_pictures(products)

    return render_template("products/products.html", products=products, pictures=pictures, mode="edit")

@app.route("/products/new", methods=["GET", "POST"])
def render_new_product():
    #Give the new product a random name, which we can then use to get its ID from the database
    random_name = str(random.randint(0,500000000))
    new_product = Product(name=random_name)
    #Add product to database
    db.session.add(new_product)
    db.session.commit()
    #Extract the newly created product and redirect to the edit page for it
    new_product = Product.query.filter(Product.name.like(random_name)).first()
    #Change the product name from the random one
    new_product.name = "Product name"
    db.session.commit()
    return redirect(f"/products/{new_product.ID}")

@app.route("/products/<int:product_id>", methods=["GET"])
def render_view_product(product_id):
    product = Product.query.filter(Product.ID.like(product_id)).first()
    pictures = Picture.query.filter(Picture.productID.like(product_id)).all()
    return render_template("products/view_product.html", product=product, pictures=pictures, mode="edit")