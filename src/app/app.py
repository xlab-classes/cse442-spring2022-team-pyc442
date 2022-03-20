from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_required, login_user
from src.authentication.user import User
from src.authentication.auth import authenticate
from src.database.wireguard_db import getUserById

def createApp():
    app = Flask(__name__)
    # sets secret key
    app.secret_key = b'f4d3d3349255d55d17dcec79f4b63395'
    #flask login information
    loginManager = LoginManager()

    loginManager.init_app(app)
    loginManager.login_view = "/"

    #User loader used by flask login library
    @loginManager.user_loader
    def userLoader(userId):
        #gets the user by there ID
        #output formate of [user_id, email, username, password, admin, banned]
        userInfo = getUserById(userId)
        #creates user object and returns it
        #formate of init for User is username: str, userid: str, isAdmin: bool, isBanned: bool
        return User(userInfo[2], userInfo[0], userInfo[4], userInfo[5])

    # route is used to server login pages
    @app.route("/")
    def rootRoute():
        return render_template('login.html', title="Login")


    # route used to server user interface TODO add in check for if post or get and add in below
    @app.route("/user")
    # checks for auth and redirect to root if not
    @login_required
    def userRoute():
        #checks for if admin
        # return tempate page for admin and sets its title to the admins name
        if User.is_admin:
            return render_template("user.html", title=User.get_username)
        # returns the user template
        return render_template("user.html", title=User.get_username)


    #Route to authenticate a user
    @app.route("/login", methods=["POST"])
    def loginRoute():
        # authenticates the user or returns none if invalid
        user =  authenticate(request.form["username"], request.form["password"])
        # Checks to make sure user was 
        if(user != None):
            if(request.form["rememberUser"]=="True"):
                login_user(user, remember="True")
                return redirect("/user")
            else:
                login_user(user)
                return redirect("/user")
        else:
            flash("Invalid password")
            return
    return app
