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


@views.route("/projects", methods=["GET", "POST"])
def projects():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT * FROM crowdfund"

    cursor.execute(query)

    projects = cursor.fetchall()
    connection.close()
    return render_template("projects.html", user=current_user, projects=projects)


@views.route("myprojects", methods=["GET", "POST"])
def myprojects():
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "SELECT * FROM crowdfund WHERE username = %s"
    cursor.execute(query, (current_user.id,))

    projects = cursor.fetchall()
    connection.close()
    return render_template("myprojects.html", user=current_user, projects=projects)


@views.route("/editfundme/<string:id>", methods=["GET", "POST"])
def editfundme(id):
    connection = connect_to_database()
    cursor = connection.cursor()

    if request.method == "POST":
        new_title = request.form.get("title")
        new_description = request.form.get("description")
        new_image = request.form.get("image")
        new_goal = request.form.get("total_funding")

        query = "UPDATE crowdfund SET title = %s, description = %s, image = %s, goal = %s WHERE title = %s"
        cursor.execute(query, (new_title, new_description, new_image, new_goal, id))
        connection.commit()

        connection.close()
        flash("Project updated successfully!", "success")
        return redirect(url_for("views.myprojects"))

    query = "SELECT * FROM crowdfund WHERE title = %s"
    cursor.execute(query, (id,))
    project = cursor.fetchone()
    connection.close()

    return render_template("editfundme.html", user=current_user, project=project)


@views.route("/deletefundme/<string:id>", methods=["GET", "POST"])
def deletefundme(id):
    connection = connect_to_database()
    cursor = connection.cursor()

    query = "DELETE FROM crowdfund WHERE title = %s"
    cursor.execute(query, (id,))
    connection.commit()
    connection.close()
    flash("Project deleted successfully!", "success")
    return redirect(url_for("views.myprojects"))

@views.route("/previewnft")
def previewnft():
    return render_template("previewnft.html", user=current_user)

@login_required
@views.route("/blockfundai")
def blockfundai():
    return render_template("ai.html")
@views.route("/voting")
def voting():
    return render_template("voting.html", user=current_user)
