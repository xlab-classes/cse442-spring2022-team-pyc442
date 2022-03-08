from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required
from src import User


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
    #TODO make title the username
    #TODO add redirect for invalid user

    return render_template("user.html", title="User")


@app.route("/login", methods=["POST"])
def loginRoute():
    print(request.form["username"])
    print(request.form["password"])
    if(request.form["password"]=="wrong"):
        return redirect("/login")
    return redirect("/user")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
