#File to hold routes (we can split this into many separate files if it gets too big)
from flask import render_template, redirect
from . import app

@app.route("/")
def render():
    return render_template("layout.html")

@app.route("/products")
def render_products():
    return render_template("products/products.html")

@app.route("/products/new", methods=["GET", "POST"])
def render_new_product():
    return render_template("products/new_product.html")

@app.route("/products/<int:product_id>", methods=["GET", "POST"])
def render_view_product(product_id):
    return render_template("products/view_product.html")