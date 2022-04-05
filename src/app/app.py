import random
import re
import bcrypt
from flask import Flask, render_template, request, redirect, flash, abort
from flask_login import LoginManager, login_required, login_user, current_user
from src.authentication.user import User
from src.authentication.auth import authenticate
from src.database.wireguard_db import changeBannedStatus, getUserById, add_users, getUserByName, modifyUsername

def createApp():
    app = Flask(__name__)
    # sets secret key
    app.secret_key = b'f4d3d3349255d55d17dcec79f4b63395'
    #flask login information
    loginManager = LoginManager()
    #add default admin user
    if(getUserByName("admin") == None):
        add_users(1,"admin@admin.com", "admin", bcrypt.hashpw(b"password", bcrypt.gensalt()),1,0)


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

    # error 404 handleing 
    @app.errorhandler(404)
    def fourzerofour(error):
        return render_template("404.html"), 404

    # route is used to server login pages
    @app.route("/")
    def rootRoute():
        return render_template('login.html', title="Login")


    # route used to server user interface 
    @app.route("/user")
    # checks for auth and redirect to root if not
    @login_required
    def userRoute():
        #checks for if admin
        # return tempate page for admin and sets its title to the admins name
        if current_user.is_admin:
            return redirect("/admin/dashboard")
        # returns redirect to correct location of user dashboard
        else:
            return render_template("user.html", title=current_user.get_username())

    # route used to serve webpages to normal users
    @app.route("/user/<path>")
    @login_required
    def serveRoute(path):
        #determine the path and return the correct user page
        if path == "dashboard":
            return render_template("users_page/user_dashboard.html", username=current_user.get_username(), title="Dashboard")
        if path == "guide":
            return render_template("users_page/user_guide.html", username=current_user.get_username(), title="Guide")
        if path == "settings":
            return render_template("users_page/user_settings.html", username=current_user.get_username(), title="Settings")
        abort(404)

    #Route to authenticate a user
    @app.route("/login", methods=["POST"])
    def loginRoute():
        # authenticates the user or returns none if invalid
        user =  authenticate(request.form.get("username"), request.form.get("password"))
        
        # Checks to make sure user was authenticated
        if(user != None):
            if(request.form.get("rememberUser")):
                login_user(user, remember=True)
                return redirect("/user")
            else:
                login_user(user, remember=False)
                return redirect("/user")
        else:
            flash("Invalid password", "error")
            return

    @app.route("/adduser", methods=["POST"])
    def adduserRoute():
        user_name = request.form["username"]
        if (getUserByName(user_name) == None): # checks to see if username already exists
            uid = random.randint(1,100) # using random number generator to get user id
            while (getUserById(str(uid)) != None): # loop to find user id that doesn't already exist
                uid = random.randint(1,100)
            password = request.form["password"]
            add_users(str(uid),"user@user.com", request.form.get("username"), bcrypt.hashpw(bytes(request.form.get("password"), "utf-8"), bcrypt.gensalt()),0,0) #adding user to db
        return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username())

    @app.route("/blockuser", methods=["POST"])
    def blockuserRoute():
        user_name = request.form["blockuser"]
        if (getUserByName(user_name) != None): # makes sure the user exists
            uid = getUserByName(user_name)[0] #gets user's uid 
            changeBannedStatus(uid, 1) #change banned status to true
        return 

    #route used to configure the server
    @app.route("/config")
    def configRoute():
        #get all the information from configuration and check what to do
        if request.form.get("vpnprotocol"):
            print("Change vpn protocol")
        if request.form.get("hostname"):
            print("Change hostname")
        if request.form.get("username"):
            modifyUsername(current_user.get_id(), request.form["username"])
        if request.form.get("password"):
            print("Change password")
    
    # route for enabling 2 factor authentication, will most likely not be done during semester
    @app.route("/2fa")
    def twofactorRoute():
        print("Error two factor authentication is not implemented")
        return redirect("/admin/configuration")

    #route used to serve pages to admin users
    @app.route("/admin/<path>")
    @login_required
    def adminPages(path):
        #check if the user is an admin
        if current_user.is_admin(): 
            #if user is an admin send them to the correct page
            if(path == "configuration"):
                return render_template("admin_configuration.html", title="Configuartion")
            elif path == "settings":
                return render_template("admin_settings.html", title="Settings", information="Server information goes here", username=current_user.get_username())
            elif path == "help":
                return render_template("admin_help.html", username=current_user.get_username())
            elif path == "add_users":
                return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username())
            elif path == "dashboard":
                return render_template("admin_dashboard.html", username=current_user.get_username(), information="Server information goes here", title="Dashboard" )
            else:
                #abort if path is not found and send back error 404
                abort(404)
        #if user is not an admin send them back to normal user space
        return render_template("user.html", title=current_user.get_username())


    return app

