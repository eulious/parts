#!/usr/bin/env python3

from json import dumps, loads
from bottle import Bottle, HTTPError, request, response, static_file
from os.path import basename, dirname

app = Bottle()


def jsonify(d):
    return dumps(d, ensure_ascii=False)


def file_response(filename):
    response = static_file(basename(filename), root=dirname(filename))
    response.set_header("Access-Control-allow-Origin", "*")
    return response


@app.hook("after_request")
def enable_cors():
    if not "Origin" in request.headers.keys():
        return
    response.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]
    response.headers["Access-Control-Allow-Methods"] = "PUT, GET, POST, DELETE, OPTIONS"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Authorization"


@app.get("/sample")
def sample():
    raise HTTPError(401, body={"error": "hoge"})
    return jsonify({"hoge": "sampleにアクセスしました。"})


@app.get("/static")
def server_static():
    return file_response("230603.jpg")


# fetch("http://localhost:8000/test/bbb?query=ccc", {method: "POST", mode: "cors", body: JSON.stringify({post: "aaaa"})}).then(res => res.json()).then(res => console.log(res))
@app.post("/test/<param>")
def sample(param):
    post = loads(request.body.read().decode("utf-8"))
    query = request.query.query
    return jsonify({"query": query, "param": param, "post": post["post"]})


app.run(host="0.0.0.0", port=8000, debug=True, reloader=True)
