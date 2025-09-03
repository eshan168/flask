import os
from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from data import Googleshop
import threading, time

app = Flask(__name__)
app.secret_key = os.urandom(12)

@app.route("/", methods=["POST","GET"])
def home():
    if request.method == "POST":
        item = request.form["searchbox1"]
        session["new"] = True
        session["item"] = item
        return redirect(url_for("loading"))
    else:
        return render_template("index.html")
    
@app.route("/loading/")
def loading():
    return render_template("loading.html")

@app.route("/search/", methods=["POST","GET"])
def search():
    if request.method == "POST":
        item = request.form["searchbox2"]
        session["item"] = item
        session["new"] = True
        return redirect(url_for("loading"))
    if session["new"]:
        products = Googleshop(session["item"])
        session["data"] = products.getproducts()
    session["new"] = False
    return render_template("products.html", products=session["data"])

if __name__ == "__main__":
    app.run(debug=True)
