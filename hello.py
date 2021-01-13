from flask import Flask, render_template

app = Flask(__name__)
port = 500
@app.route("/")
def	index():
	return "Hello"

@app.route("/<string:name>")
def	unknown(name):
	return render_template("index.html")

