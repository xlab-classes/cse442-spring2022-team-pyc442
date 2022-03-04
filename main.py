from flask import Flask, render_template

app = Flask(__name__)


# route is used to server login pages
@app.route("/")
def root():
    return render_template('login.html', title="Login")


# route used to server user interface TODO add in check for if post or get and add in below
@app.route("/user")
def user():
    #TODO below for get request
    #TODO add checks for auth and redirect to root if not
    #TODO add checks for if admin
    #TODO make title the username
    #TODO add redirect for invalid user

    return render_template("user.html", title="User")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
