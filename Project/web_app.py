from flask import Flask,jsonify,request,abort
from pymongo import MongoClient
import requests
import datetime
from datetime import date
import pandas as pd
import numpy as np
import threading
from sklearn.preprocessing import StandardScaler
from sklearn import svm
import warnings
import time 
warnings.filterwarnings('ignore')

check_var = 1
app = Flask(__name__)

def handle_seek(userid):
    time.sleep(60)
    client = MongoClient()
    db = client["blood_bank_db"]
    seek = db.seek_table
    seek.update({"user_id":userid},{"$set":{"status":"available"}})
    client.close()

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
    global check_var
    check_var = check_var + 1
    print(check_var)
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
    t1 = threading.Thread(target=handle_seek, args=(user_id,)) 
    t1.start()
    client = MongoClient()
    db = client["blood_bank_db"]
    seek = db.seek_table
    res = list(seek.find({"user_id":user_id,"status":"pending"}))
    if(len(res) != 0):
        return jsonify({}),400
    now = datetime.datetime.now()
    day = str(now.day)
    month = str(now.month)
    year = str(now.year)
    date = day + "/" + month + "/" + year
    data = {"user_id":user_id,"quantity":quantity,"info":info,"blood_group":blood_group,"status":"pending","date":date}
    seek.insert_one(data)
    client.close()
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

@app.route("/get_status",methods=["POST"])
def get_status():
    client = MongoClient()
    db = client["blood_bank_db"]
    seek = db.seek_table
    print("request json",request.json)
    user_id = request.json["user_id"]
    res = list(seek.find({"user_id":user_id}))
    d = dict()
    if(len(res) != 0):
        d["status"] = res[0]["status"]
        d["blood_group"] = res[0]["blood_group"]
        d["info"] = res[0]["info"]
        d["quantity"] = res[0]["quantity"]
    else:
        d["status"] = "NA"
        d["blood_group"] = "NA"
        d["info"] = "NA"
        d["quantity"] = "NA"
    client.close()
    return jsonify(d),200

@app.route("/predict",methods=["POST"])
def predict_donor():
    #code to input
    msld = int(request.json["msld"])
    td = int(request.json["td"])
    tv = int(request.json["tv"])
    msfd = int(request.json["msfd"])
    df = pd.read_csv('train.csv', index_col=False)
    df.columns = ['id','months_since_last_donation','num_donations','vol_donations','months_since_first_donation', 'class']
    df = df.drop(['id'], axis=1)

    #Enter test values in the below line here
    test = pd.DataFrame(columns=['months_since_last_donation','num_donations','vol_donations','months_since_first_donation'], data=[[msld,td,tv,msfd]])

    df["class"] = df["class"].astype(int)

    Y_train = df["class"]

    X_train = df.drop(labels = ["class"],axis = 1)

    sc = StandardScaler()
    X_train_scaled = sc.fit_transform(X_train)
    test_scaled = sc.transform(test)

    clf = svm.SVC(kernel='linear', C = 1.0, probability=True)
    clf.fit(X_train_scaled,Y_train)

    predictions = clf.predict_proba(test_scaled)
    predictions = predictions[:,1]
    d = dict()
    if(predictions[0]>0.24):
        output = "Yes, Will donate"
    else:
        output = "No, Will not donate"
    d["output"] = output
    return jsonify(d),200



if __name__ == '__main__':
    app.run("0.0.0.0",port=5000,debug=True)
