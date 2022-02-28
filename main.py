from flask import Flask, render_template


app = Flask(__name__)


@app.route("/test")
def test():
    return render_template('test.html')

@app.route("/")
def root():
    return render_template('login.html', title = "Login")


@app.route("/user")
def user():
    #TODO add checks for auth and redirect to root if not
    #TODO add checks for if admin
    #TODO make page dynamic
    #TODO make title the username
    return render_template("user.html", title = "User")

if __name__ == "__main__":
    app.run()
