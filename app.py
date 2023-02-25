import random

from sanic import Sanic, text, json
from sanic_ext import Extend
import ujson, sanic

app = Sanic("server")

app.config.OAS = False
app.config.LOGGING = True
app.config.CORS_ORIGINS = "*"

Extend(app)

with open("word.json", "r", encoding="utf8") as f:
    word = ujson.load(f)

with open("fy.json", "r", encoding="utf8") as f:
    fy = ujson.load(f)


@app.route("/")
async def index(request: sanic.Request):
    return text("Nothing is here. Visit https://github.com/cxzlw/pen-order-dictionary-python please. ")


@app.route("/search/bsm")
def search_bsm(request: sanic.Request):
    search = request.args.get("search")
    if not search:
        return json([])
    data = []
    find = False
    for w in word:
        if w["bsm"].startswith(search):
            find = True
            data.append({"hz": w["hz"], "bh": w["bh"]})
        elif find:
            break
    return json(data)


@app.route("/hz")
async def hz(request: sanic.Request):
    bh = request.args["bh"][0]
    return json(word[bh])


@app.route("/fybsm")
def fybsm(request: sanic.Request):
    bsm = request.args["bsm"][0]
    ret = ""
    for c in bsm:
        ret += fy[ord(c) - 97]["fy"] + ","
    ret = ret[:-1]
    return json(ret)


@app.route("/learn")
def learn(request: sanic.Request):
    z = random.choice(word)
    ans = random.randint(0, 3)
    ret = []
    for x in range(4):
        if x == ans:
            ret.append(z["hz"])
        else:
            ret.append(random.choice(word)["hz"])
    return json({"bsm": z["bsm"], "sj": ret, "id": ans})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
