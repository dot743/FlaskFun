from flask import Flask, render_template, request
import datetime
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    bobby = "Word!^^!"
    return render_template("home.html", bobby=bobby)

@app.route('/mileage')
def mileageForm():
    return render_template("mileage.html")

@app.route('/birthday')
def tansbday():
    tan = datetime.datetime.now()
    # superDay = tan.month == 10 and tan.day == 28
    superDay = 6
    return render_template("home.html", superDay=superDay)

@app.route("/success", methods=["post"])
def submission():
    name2 = request.form.get("name1")
    return render_template("success.html", name3=name2)

@app.route('/<path:dummy>')
def fallback(dummy):
    return render_template("home.html")

# @app.route('/tan')
# def hello_tan():
#     return 'Hello, Tan!!!'
#
# @app.route('/<string:name>')
# def mystt(name):
#     name += "w assa"
#     return "<h1>hello {}</h1>".format(name)


if __name__ == "__main__":
    app.run()
