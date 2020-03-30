#File to hold routes (we can split this into many separate files if it gets too big)
import os
import random
from flask import render_template, redirect, request, flash, url_for, session
from werkzeug.utils import secure_filename
from .forms import *
from .models import db, Product, Picture
from sqlalchemy import and_
from . import app
import time

@app.route("/")
def render_home():
    return render_template("layout.html")

@app.route("/products")
def render_products():
    def handle_views():
        """Handle setting of session variables for product display.\n
        This will return a redirect if the required GET variable is missing from the url."""
        #If it is set to grid, set the session variable and return
        if "view" in request.args:
            if request.args["view"] == "grid":
                session["product display"] = "grid"
            else:
                session["product display"] = "list"
            #If view is in the GET args, we do not need to rebuild the url to contain it.
            #So we can return
            return
                
        #If either of the previous checks fail, set "product display" to if it is not available
        if not("product display" in session):
            session["product display"] = "list"

        #Build a redirect to set the GET variable to list.
        temp = []

        #For each arg in the request, recreate the GET string for that arg
        for arg in request.args:
            temp.append(f"{arg}={request.args[arg]}")

        #Add our new arg to the list
        temp.append(f"view={session['product display']}")

        #Create the base url and add all the args to it
        url = f"{request.base_url}?"
        for arg in temp:
            url += f"{arg}&"

        #Remove the extra & from the string and return the redirect
        return redirect(url[:-1])
    def get_products():
        """This function gets the relevant products from the database and filters them according to user input."""
        products = []
        if "query" in request.args:
            #Fitler the results with the query, look at the description and name of products.
            products = Product.query.filter(Product.name.like(f"%{request.args['query']}%")).all()
            products += Product.query.filter(Product.description.like(f"%{request.args['query']}%")).all()
            #TODO: ADD CATEGORY FILTERING
            #Remove any duplicates
            already_present = []
            for product in products:
                if product.ID in already_present:
                    products.remove(product)
                else:
                    already_present.append(product.ID)
        else:
            products = Product.query.all()
        return products
    def get_pictures(products):
        """Get the relevant pictures from the database."""
        #Setup return list with slots for each product
        pictures_return = []
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
    
    #Call handle_views, if it returns something, return it.
    retval = handle_views()
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