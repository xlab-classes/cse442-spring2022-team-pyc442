from os import remove
import random
import bcrypt
from flask import Flask, render_template, request, redirect, flash, abort
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from src.authentication.user import User
from src.authentication.auth import authenticate
from src.database import wireguard_db
from src.database.wireguard_db import changeBannedStatus, getUserById, add_users, getUserByName, listBlockedUsers, modifyUsername, changePassword, get_user_server
from src.wireguard import wireguard_server as wg
import ipaddress

def createApp(dev: bool):
    app = Flask(__name__)
    if not dev:
        wireguard_db.setup_con_db()
    # sets secret key must set to new random key later on
    app.secret_key = b'f4d3d3349255d55d17dcec79f4b63395'


    #flask login information
    loginManager = LoginManager()

    # create wireguard server management class
    wireguard_server = wg.Wireguard_Server()

    #add default admin user
    if(getUserByName("admin") == None):
        add_users("1","admin@admin.com", "admin", bcrypt.hashpw(b"password", bcrypt.gensalt()),1,0)
        wireguard_server.add_user_new("1")



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
        if current_user.is_authenticated:
            return redirect("/user")
        return render_template('login.html', title="Login")


    # route used to server user interface
    @app.route("/user")
    # checks for auth and redirect to root if not
    @login_required
    def userRoute():
        #checks for if admin
        # return tempate page for admin and sets its title to the admins name
        if current_user.is_admin():
            return redirect("/admin/dashboard")
        if getUserByName(current_user.get_username())[5] == 1:
            return render_template('login.html', title="Login", error="You have been blocked! Please contact admin for more info")
        # returns redirect to correct location of user dashboard
        else:
            return redirect("/user/dashboard")

    @app.route("/changepwd", methods=["POST"])
    @login_required
    def changepwdRoute():
        user = authenticate(current_user.get_username(),request.form.get("pwd"))
        if(user != None):
            changePassword(current_user.get_username(), bcrypt.hashpw(bytes(request.form.get("newpwd"), "utf-8"), bcrypt.gensalt()))
            return render_template("users_page/user_settings.html", username = current_user.get_username(), passwordStatus = "Successfully changed password")
        return render_template("users_page/user_settings.html", username = current_user.get_username(), passwordStatus = "Incorrect password")

    # route used to serve webpages to normal users
    @app.route("/user/<path>")
    @login_required
    def serveRoute(path):
        #determine the path and return the correct user page
        if getUserByName(current_user.get_username())[5] == 1:
            return render_template('login.html', title="Login", error="You have been blocked! Please contact admin for more info")
        if path == "dashboard":
            return render_template("users_page/user_dashboard.html", username=current_user.get_username(), title="Dashboard")
        if path == "help":
            keys = get_user_server(current_user.get_id())
            return render_template("users_page/user_guide.html",
                                   username=current_user.get_username(),
                                   title="Guide",
                                   private_key = keys[1],
                                   ipaddrs = str(ipaddress.ip_address(keys[3])),
                                   server_public = wireguard_server.get_pubkey(),
                                   dns = wireguard_server.dns,
                                    listen_port = wireguard_server.listen_port)
        if path == "settings":
            return render_template("users_page/user_settings.html", username=current_user.get_username(), title="Settings")
        abort(404)

    @app.route("/user")

    #Route to authenticate a user
    @app.route("/login", methods=["POST"])
    def loginRoute():
        # authenticates the user or returns none if invalid
        user =  authenticate(request.form.get("username"), request.form.get("password"))

        # Checks to make sure user was authenticated
        if(user != None):
            if(request.form.get("rememberUser")):
                print("here")
                login_user(user, remember=True)
                return redirect("/user")
            else:
                login_user(user, remember=False)
                return redirect("/user")
        else:
            Error = "Invalid username and/or password"
            return render_template('login.html', title="Login", error=Error)

    @app.route("/adduser", methods=["POST"])
    def adduserRoute():
        if (request.form["username"] == "" or request.form["password"] == ""):
            Error = "Please enter a valid username/password."
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, error=Error)
        user_name = request.form["username"]
        if (getUserByName(user_name) == None): # checks to see if username already exists
            uid = random.randint(1,100) # using random number generator to get user id
            while (getUserById(str(uid)) != None): # loop to find user id that doesn't already exist
                uid = random.randint(1,100)
            password = request.form["password"]
            add_users(str(uid),"user@user.com", request.form.get("username"), bcrypt.hashpw(bytes(request.form.get("password"), "utf-8"), bcrypt.gensalt()),0,0) #adding user to db
            wireguard_server.add_user_new(str(uid))
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", blist=bu_list, username=current_user.get_username())
        else:
            Error = "The username you entered is already in use. Please enter a different username."
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, error=Error)

    @app.route("/blockuser", methods=["POST"])
    def blockuserRoute():
        if (request.form["blockuser"] == ""):
            Error = "Please enter a valid username."
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, error=Error)
        user_name = request.form["blockuser"]
        if (getUserByName(user_name) != None): # makes sure the user exists
            uid = getUserByName(user_name)[0] #gets user's uid
            changeBannedStatus(uid, 1) #change banned status to true
            wireguard_server.remove_user(uid)
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, addedlist=[])
        else:
            Error = "User not found. Please enter a valid username."
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, error=Error)

    @app.route("/unblockuser", methods=["POST"])
    def unblockuserRoute():
        if (request.form["unblockuser"] == ""):
            Error = "Please enter a valid username."
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, error=Error)
        user_name = request.form["unblockuser"]
        if (getUserByName(user_name) != None): # makes sure the user exists
            uid = getUserByName(user_name)[0] #gets user's uid
            changeBannedStatus(uid, 0) #change banned status to false
            wireguard_server.add_user(uid)
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, addedlist=[])
        else:
            Error = "User not found. Please enter a valid username."
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, error=Error)
    
    @app.route("/kickuser", methods=["POST"])
    def kickuserRoute():
        if (request.form["kickuser"] == ""):
            Error = "Please enter a valid username."
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, error=Error)
        user_name = request.form["kickuser"]    
        if (getUserByName(user_name) != None): # makes sure the user exists
            uid = getUserByName(user_name)[0] #gets user's uid
            wireguard_server.remove_user(uid)
            wireguard_server.add_user(uid)
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list)
        else:
            Error = "User not found. Please enter a valid username."
            bu_list = listBlockedUsers()
            return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, error=Error)

    @app.route("/advancedsettings", methods=["POST"])
    def advancedsettingsRoute():
        lport = request.form["lport"]
        wireguard_server.change_listen_port(lport)

        dns = request.form["dns"]
        wireguard_server.change_DNS(dns)
        return render_template("admin_settings.html", title="Settings", username=current_user.get_username())

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
                keys = get_user_server(current_user.get_id())
                return render_template("admin_help.html", username=current_user.get_username(),
                                       private_key=keys[1],
                                       server_public=wireguard_server.get_pubkey(),
                                       ipaddrs=str(ipaddress.ip_address(keys[3])),
                                       dns=wireguard_server.dns,
                                       listen_port=wireguard_server.listen_port)
            elif path == "add_users":
                bu_list = listBlockedUsers()
                return render_template("admin_add_users.html", title="Add Users", username=current_user.get_username(), blist=bu_list, addedlist=[])
            elif path == "dashboard":
                return render_template("admin_dashboard.html", username=current_user.get_username(), information="Server information goes here", title="Dashboard", start_button=("Stop" if wireguard_server.is_running() else "Start"))
            else:
                #abort if path is not found and send back error 404
                abort(404)
        #if user is not an admin send them back to normal user space
        return redirect("/user") # render_template("user.html", username=current_user.get_username(), information="Server information goes here", title="Dashboard" )

    @app.route("/logout", methods=["POST"])
    def logoutRoute():
        if current_user.is_authenticated:
           logout_user() 
        return redirect("/")

    @app.route("/togglewg", methods=["POST"])
    @login_required
    def toggle_wg_route():
        if current_user.is_admin():
            if wireguard_server.is_running():
                wireguard_server.stop()
            else:
                wireguard_server.start()
            return redirect("/admin/dashboard")

    return app

