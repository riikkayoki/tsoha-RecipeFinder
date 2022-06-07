from app import app
from flask import render_template, request, redirect, flash
from services.user_service import user_service
from entities.user import User

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not user_service.login_user(username, password):
            return render_template("login.html")
        return redirect("/homepage")
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        user_role = request.form["role"]
        phone_number = request.form["phone"]
        email = request.form["email"]
        user_service.register_user(username, password1, user_role, phone_number, email)
        return redirect("/homepage")
    return render_template("signup.html")

@app.route("/homepage", methods=["GET","POST"])
def homepage():
    return render_template("homepage.html", user_role = user_service.user_role())

@app.route("/profile/<int:id>", methods=["GET","POST"])
def profile(id):
    username = user_service.get_current_username(id)
    email = user_service.get_current_email(id)
    phone_number = user_service.get_current_phone_number(id)
    role = user_service.get_current_role(id)
    if request.method == "GET":
        return render_template("profile.html", username=username, email=email, role=role, phone_number=phone_number, id=id)

    if request.method == "POST":
        new_username = request.form["new_username"]
        new_email = request.form["new_username"]
        new_phone_number = request.form["new_phone_number"]
        if new_username:
            user_service.modify_username(new_username, id)
            return render_template("profile.html", username=new_username, email=email, role=role, phone_number=phone_number, id=id)
        if new_email:
            user_service.modify_email(new_email, id)
            return render_template("profile.html", username=username, email=new_email, role=role, phone_number=phone_number, id=id)
        if new_phone_number:
            user_service.modify_phone_number(new_phone_number, id)
            return render_template("profile.html", username=username, email=email, role=role, phone_number=new_phone_number, id=id)

@app.route("/favorites", methods=["GET","POST"])
def favorites():
    return render_template("favorites.html")


@app.route("/logout", methods=["GET","POST"])
def logout():
    user_service.logout()
    return redirect("/")

@app.route("/manage-recipes", methods=["GET","POST"])
def manage_recipes():
    return render_template("manage_recipes.html")

@app.route("/manage-ingredients", methods=["GET","POST"])
def manage_ingredients():
    return render_template("manage_ingredients.html")

@app.route("/manage-ingredient-categories", methods=["GET","POST"])
def manage_ingredient_categories():
    return render_template("manage_ingredient_categories.html")

@app.route("/basket", methods=["GET","POST"])
def basket():
    return render_template("basket.html")
