from flask import Flask,jsonify,request,abort
from pymongo import MongoClient
import requests
import datetime
from datetime import date

app = Flask(__name__)
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Origin','127.0.0.1')
  return response

@app.route("/check",methods=['GET'])
def trial_connection():
    trial_dict = dict()
    trial_dict["trial"] = "ok"
    return jsonify(trial_dict),200

@app.route("/donate",methods=["POST"])
def donate_blood():
    user_id = request.json["user_id"]
    date = request.json["date"]
    time = request.json["time"]
    info = request.json["info"]
    bg = request.json["blood_group"]
    client = MongoClient()
    db = client["blood_bank_db"]
    donar = db.donate_table
    donar_data = list(donar.find())
    max_id = -1
    for i in donar_data:
        bi = i["blood_id"]
        b_id = int(bi.split("SAMPLE")[1])
        if(b_id > max_id):
            max_id = b_id
    blood_id = "SAMPLE" + str(max_id+1)
    data = {"blood_id":blood_id,"user_id":user_id,"blood_group":bg,"date":date,"time":time,"info":info,"status":"in"}
    donar.insert_one(data)
    return jsonify({}),200

@app.route("/seek",methods=["POST"])
def seek_blood():
    print(request.json)
    user_id = request.json["user_id"]
    quantity = request.json["quantity"]
    info = request.json["info"]
    blood_group = request.json["blood_group"]
    client = MongoClient()
    db = client["blood_bank_db"]
    seek = db.seek_table
    now = datetime.datetime.now()
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    date = day + "/" + month + "/" + year
    data = {"user_id":user_id,"quantity":quantity,"info":info,"blood_group":blood_group,"status":"pending","date":date}
    seek.insert_one(data)
    return jsonify({}),200

@app.route("/register",methods=["POST"])
def register_user():
    sex = request.json["sex"]
    user_name = request.json["user_name"]
    DOB = request.json["DOB"]
    address = request.json["address"]
    email = request.json["email"]
    blood_group = request.json["blood_group"]
    password = request.json["password"]
    client = MongoClient()
    db = client["blood_bank_db"]
    user_info = db.person_details_table
    res = list(user_info.find())
    for i in res:
        if(i["email"] == email):
            client.close()
            return jsonify({}),401
    max_id = -1
    for i in res:
        user_id = int(i["user_id"].split("BLOOD")[1])
        if(user_id > max_id):
            max_id = user_id
    max_id = max_id + 1
    user_id = "BLOOD" + str(max_id)
    data = {"user_id":user_id,"name":user_name,"sex":sex,"DOB":DOB,"address":address,"email":email,"blood_group":blood_group,"password":password}
    user_info.insert_one(data)
    client.close()
    return jsonify({}),200

@app.route("/login",methods=["POST"])
def user_login():
    email = request.json["email"]
    password = request.json["password"]
    client = MongoClient()
    db = client["blood_bank_db"]
    user_info = db.person_details_table
    res = list(user_info.find({"email":email}))
    if(len(res) == 0):
        client.close()
        return jsonify({}),400
    if(res[0]["password"] != password):
        client.close()
        return jsonify({}),400
    user_id = res[0]["user_id"]
    return jsonify({"user_id":user_id}),200


if __name__ == '__main__':
    app.run("0.0.0.0",port=5000,debug=True)
