from flask import Flask, request, render_template

bryll = Flask(__name__)

@bryll.route("/fetch_url", methods =["GET", "POST"])
def fetch_url():
    if request.method == "POST":
        return render_template("index.html")