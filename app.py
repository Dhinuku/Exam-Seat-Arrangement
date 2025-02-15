from math import ceil
from flask import Flask, render_template, request
import json
import pandas as pd
app = Flask(__name__)

stufiles = open("studetails.txt", "r")
stulist = json.load(stufiles)
listy = []
newlist=[]

@app.route("/")
def hi():
    return render_template("home.html")


@app.route('/submit', methods=["POST"])
def home1():
    dict = request.form
    stulist.append(dict)
    stufile = open("studetails.txt", "w")
    json.dump(stulist, stufile)
    stufile.close()
    return stulist


@app.route('/data', methods=["GET"])
def data():
    studata = open("Test.csv", "r")
    exams = []
    while True:
        line = studata.readline()
        if not line:
            break
        ligma = line.replace('\n', '').split(',')
        if not ligma[2] in exams:
            exams.append(ligma[2])
            dict = {'name': ligma[2], 'ro': []}
            listy.append(dict)
    studata.seek(0)
    while True:
        line = studata.readline()
        if not line:
            break
        ligma = line.replace('\n', '').split(',')
        for d in listy:
            if d['name'] == ligma[2]:
                d['ro'].append(ligma[0])
    return listy


@app.route('/seating', methods=["GET"])
def seating():
    k = 0
    for i in stulist:
        if len(listy) == 0:
            break
        a = ceil(int(i["column"])/2)*int(i["rows"])
        b = (int(i["column"])*int(i["rows"]))-a
        firstitem = listy[0]
        listy.pop(0)
        if len(firstitem["ro"]) == 0:
            continue
        for j in range(0, a):
            if len(firstitem["ro"]) == 0:
                if len(listy) == 0:
                    break
                firstitem = listy[0]
                listy.pop(0)
            i["a"].append(firstitem["ro"][0])
            firstitem["ro"].pop(0)
        if len(firstitem["ro"]) != 0:
            print("before pop\n")
            listy.append(firstitem)
            firstitem = listy[0]
            listy.pop(0)
        for k in range(0, b):
            if len(firstitem["ro"]) == 0:
                if len(listy) == 0:
                    break
                firstitem = listy[0]
                listy.pop(0)
            i["b"].append(firstitem["ro"][0])
            firstitem["ro"].pop(0)
        if len(firstitem["ro"]) != 0:
            listy.append(firstitem)
    global newlist
    newlist=list(stulist)
    return newlist
    

@app.route('/student', methods=["POST"])
def details():
    roll=request.form["rollnum"]
    print(newlist)
    return roll
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
