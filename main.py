from flask import Flask, request, render_template, request,jsonify

bryll = Flask(__name__)

@bryll.route("/fetch_url", methods=["POST"])
def fetch_url():
    print(11)
    print(request.form)

    try:
       link = request.form["link"]
    except Exception as e:
       response = jsonify(status="no link sent????")
       response.headers.add("Access-Control-Allow-Origin", "*") # some browsers require this header
       return response                                         # or it fails to send requests

    # before working on it, make regex search
    # to check if it's a yt link
    print('New request!',link)
    # Normally we don't reply untill we fetched details
    response = jsonify(status="Working on it!")
    response.headers.add("Access-Control-Allow-Origin", "*") # some browsers require this header
    return response                                         # or it fails to send requests

@bryll.route("/", methods =["GET"])
def main():
    return render_template("./index.htm")

@bryll.after_request
def after(response):
    # for debugging requesrs
    print(response.status)
    print(response.headers)
    print(response.get_data())
    return response

bryll.run()

