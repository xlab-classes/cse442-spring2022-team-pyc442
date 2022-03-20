import os
import re
import bcrypt
from flask import Flask, render_template, request, redirect, flash, abort
from flask_login import LoginManager, login_required, login_user, current_user
from src.authentication.user import User
from src.authentication.auth import authenticate
from src.database.wireguard_db import getUserById, add_users, getUserByName, modifyUsername

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


    # route used to server user interface TODO add in check for if post or get and add in below
    @app.route("/user")
    # checks for auth and redirect to root if not
    @login_required
    def userRoute():
        #checks for if admin
        # return tempate page for admin and sets its title to the admins name
        if current_user.is_admin:
            return redirect("/admin/dashboard")
        # returns the user template
        return render_template("user.html", title=current_user.get_username())


    #Route to authenticate a user
    @app.route("/login", methods=["POST"])
    def loginRoute():
        # authenticates the user or returns none if invalid
        user =  authenticate(request.form.get("username"), request.form.get("password"))
        # Checks to make sure user was 
        if(user != None):
            if(request.form.get("rememberUser")):
                login_user(user, remember=True)
                return redirect("/user")
            else:
                login_user(user, remember=False)
                return redirect("/user")
        else:
            flash("Invalid password")
            return
    @app.route("/adduser")
    def adduserRoute():
        user_name = request.form.get("username")
        if (getUserByName(user_name) == None):
            uid = os.random(9)
            while (getUserById(uid) != None):
                uid = os.random(9)
            password = request.form.get("password")
            add_users(str(uid),"user@user.com", user_name, bcrypt.hashpw(password, bcrypt.gensalt()),0,0) 
        return 

    #route used to configure the server
    @app.route("/config")
    def configRoute():
        if request.form.get("vpnprotocol"):
            print("Change vpn protocol")
        if request.form.get("hostname"):
            print("Change hostname")
        if request.form.get("username"):
            modifyUsername(current_user.get_id(), request.form["username"])
        if request.form.get("password"):
            print("Change password")

    #route used to serve pages to admin users
    @app.route("/admin/<path>")
    @login_required
    def adminPages(path):
        if current_user.is_admin(): 
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
                abort(404)

    @app.route("/admin/add_users")
    def add_usersRoute():
        user_name = request.form["adduser"]
        new_user = authenticate(user_name, "password")
        add_users(111,"user@user.com", user_name, bcrypt.hashpw(b"password", bcrypt.gensalt()),0,0) 


    return app
