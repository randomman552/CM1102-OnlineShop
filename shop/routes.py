#File to hold routes (we can split this into many separate files if it gets too big)
import os
import random
from flask import render_template, redirect, request, flash, url_for
from werkzeug.utils import secure_filename
#from .forms import *
from .models import db, Product, Picture
from . import app

@app.route("/")
def render_home():
    return render_template("layout.html")

@app.route("/products?query=<string:query>")
def render_products(query):
    return render_template("products/products.html")

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
    return redirect(f"/products/edit/{new_product.ID}")

@app.route("/products/edit/<int:product_id>")
def render_edit_product(product_id):
    product = Product.query.filter(Product.ID.like(product_id)).first()
    pictures = Picture.query.filter(Picture.productID.like(product_id)).all()
    return render_template("products/view_product.html", product=product, pictures=pictures, mode="edit")

@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def render_view_product(product_id):
    product = Product.query.filter(Product.ID.like(product_id)).first()
    pictures = Picture.query.filter(Picture.productID.like(product_id)).all()
    return render_template("products/view_product.html", product=product, pictures=pictures, mode="view")