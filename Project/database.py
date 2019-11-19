from pymongo import MongoClient
import json
client = MongoClient()
db = client["blood_bank_db"]

donate_info = db.donate_table
data1 = {"blood_id":"SAMPLE1","user_id":"BLOOD3","date":"23/11/2019","time":"11:30","info":"save life","status":"in"}
data2 = {"blood_id":"SAMPLE2","user_id":"BLOOD4","date":"25/11/2019","time":"10:30","info":"save life","status":"out"}
donate_info.insert_many([data1,data2])

seek_info = db.seek_table
data1 = {"user_id":"BLOOD1","bloodgroup":"A+","quantity":"300","info":"needed urgent","status":"pending"}
data2 = {"user_id":"BLOOD2","bloodgroup":"B+","quantity":"500","info":"needed urgent","status":"pending"}
seek_info.insert_many([data1,data2])

person_info = db.person_details_table
data1 = {"user_id" : "BLOOD1", "name" : "Sanjay", "sex" : "M", "DOB" : "10/10/1998", "address" : "#210/1A Banashankari Bangalore", "bloodgroup" : "B+", "email" : "sanjay@gmail.com", "password" : "a9993e364706816aba3e25717850c26c9cd0d89d" }
data2 = {"user_id" : "BLOOD2", "name" : "Sharath", "sex" : "M", "DOB" : "12/3/1995", "address" : "#210/1A Banashankari Bangalore", "bloodgroup" : "A+", "email" : "sharath@gmail.com", "password" : "a9993e364706816aba3e25717850c26c9cd0d89d"}
data3 = {"user_id" : "BLOOD3", "name" : "Kishore", "sex" : "M", "DOB" : "13/4/1985", "address" : "#210/1A Banashankari Bangalore", "bloodgroup" : "O+", "email" : "kishore@gmail.com", "password" : "a9993e364706816aba3e25717850c26c9cd0d89d"}
data4 = {"user_id" : "BLOOD4", "name" : "Saloni", "sex" : "F", "DOB" : "14/6/1997", "address" : "#210/1A Banashankari Bangalore", "bloodgroup" : "B+", "email" : "saloni@gmail.com", "password" : "a9993e364706816aba3e25717850c26c9cd0d89d" }
data5 = {"user_id" : "BLOOD5", "name" : "Shalini", "sex" : "F", "DOB" : "17/7/1990", "address" : "#210/1A Banashankari Bangalore", "bloodgroup" : "AB+", "email" : "shalini@gmail.com", "password" : "a9993e364706816aba3e25717850c26c9cd0d89d" }
data6 = {"user_id" : "BLOOD6", "name" : "Samarth", "sex" : "M", "DOB" : "18/9/1986", "address" : "#210/1A Banashankari Bangalore", "bloodgroup" : "O+", "email" : "samarth@gmail.com", "password" : "a9993e364706816aba3e25717850c26c9cd0d89d" }
person_info.insert_many([data1,data2,data3,data4,data5,data6])








