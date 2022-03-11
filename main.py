from turtle import title
from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_required, login_user
from src.authentication.user import User
from src.authentication.auth import authenticate


app = Flask(__name__)

#flask login information
loginManager = LoginManager()

loginManager.init_app(app)
loginManager.login_view = "/"

@loginManager.user_loader
def userLoader(userId):
    #TODO add database information here
    return NotImplementedError

# route is used to server login pages
@app.route("/")
def rootRoute():
    return render_template('login.html', title="Login")


# route used to server user interface TODO add in check for if post or get and add in below
@app.route("/user")
@login_required
def userRoute():
    #TODO add checks for auth and redirect to root if not
    #TODO add checks for if admin
    if User.is_admin:
        return render_template("user.html", title="Admin")
    #TODO make title the username
    #TODO add redirect for invalid user

    return render_template("user.html", title="User")


#Route to authenticate a user
@app.route("/login", methods=["POST"])
def loginRoute():
    # authenticates the user or returns none if invalid
    user =  authenticate(request.form["username"], request.form["password"])
    # Checks to make sure user was 
    if(user != None):
        login_user(user)
        return redirect("/user")
    else:
        flash("Invalid password")
        return

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
