#File to hold routes (we can split this into many separate files if it gets too big)
from flask import render_template, redirect
from . import app

@app.route("/")
def render():
    return render_template("layout.html")