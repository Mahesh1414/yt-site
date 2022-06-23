from flask import Flask, request, render_template, request,jsonify, send_file
from tube import pyt
from stuff import stk2, msg11

bryll = Flask("tube")
savedTokens = {}
processedUsers = {}

@bryll.route("/fetch_url", methods=["POST"])
async def fetch_url():
    print(request.form)
    try:
       link = request.form["link"]
    except Exception as e:
       m = {'id': None,'status':'error','stkr': stk2,'msg': msg11}
       response = jsonify(m)
       response.headers.add("Access-Control-Allow-Origin", "*") # some browsers require this header
       return response                                         # or it fails to send requests

    #TODO before working on it, make regex search
    # to check if it's a yt link
    print('New request!',link)
    # Normally we don't reply untill we fetched details

    if "youtu" in link:
        pyts = pyt(link)
        m, savetoken = await pyt.fetch(pyts)
        if savetoken:
           savedTokens[m['id']] = savetoken
    else:
        print(len(link), "youtu" in link, link)
        m = {'id': None,'status':'error','stkr': stk2,'msg': msg11}

    response = jsonify(m)
    response.headers.add("Access-Control-Allow-Origin", "*") # some browsers require this header
    return response                                         # or it fails to send requests

@bryll.route("/down", methods=["POST"])
async def down():
    print(request.json)

    try:
       id = request.json["id"]
    except Exception as e:
       m = {'id': None,'status':'error','stkr': stk2,'msg': "no id sent"}
       response = jsonify(m)
       response.headers.add("Access-Control-Allow-Origin", "*")
       return response

    if not id in savedTokens:
       m = {'id': None,'status':'error','stkr': stk2,'msg': "Sorry this Process Expired, resend a link"}
       response = jsonify(m)
       response.headers.add("Access-Control-Allow-Origin", "*")
       return response

    pyts     = savedTokens[id]
    is_progr = request.json["progressive"]
    mtype    = request.json["mtype"]
    vtag     = request.json["vtag"]
    atag     = request.json["atag"]

    pyts.setItagV(vtag)
    pyts.setItagA(atag)

    #bug in flask false in json isn't converted to False
    is_progr = is_progr in 'true'
    processedUsers[id] = "processing"
    m, processedUsers[id] = await pyts.download(is_progr)
    response = jsonify(m)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@bryll.route("/final/<id>", methods=["GET"])
async def final(id):
    if not id in savedTokens:
       m = {'id': None,'status':'error','stkr': stk2,'msg': "Sorry this Process Expired, resend a link"}
       response = jsonify(m)
       response.headers.add("Access-Control-Allow-Origin", "*")
       return response
    print(id)
    pyts = savedTokens[id]
    path = pyts.output
    return send_file(path, as_attachment=True)

@bryll.route("/", methods =["GET"])
async def main():
    return render_template("./index.htm")

@bryll.after_request
async def after(response):
    # for debugging requesrs
    print(response.status)
    print(response.headers)
#    print(response.get_data())
    return response

#loop = asyncio.get_event_loop()
#asyncio.ensure_future(bryll.run(), loop=loop)
bryll.run('0.0.0.0', debug=True)

