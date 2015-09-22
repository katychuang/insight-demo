from flask import Flask
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route('/index')
def hello():
    return "Hello World!"

@app.route("/case/<id>/")
def case(id):
    return id


@app.route("/test/<id>/")
def test(id):
    return id

@app.route("/test")
def create_test():
	return render_template("layout.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


