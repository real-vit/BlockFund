from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .dbconnect import connect_to_database
import time
import json
import ast

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html", user=current_user)

@views.route("/newfundme", methods=["GET", "POST"])
def newfundme():
    connection = connect_to_database()
    cursor = connection.cursor()
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        goal = request.form.get("total_funding")
        image_link = request.form.get("image_link")
        values = (title, description, goal, image_link, current_user.id)
        query = "INSERT INTO crowdfund (title, description, goal, image, username) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, values)
        connection.commit()
        connection.close()
        flash("FundMe Created!", category="success")

        return redirect(url_for("views.projects"))
    return render_template("newfundme.html", user=current_user)