import pymongo
from pymongo import MongoClient
from datetime import datetime

__cluster__ = MongoClient(
    "mongodb+srv://OzCohen:Oz322713561@cluster0.e5jas.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = __cluster__["WAH"]
collection = db["Users"]


def add_new_user(f_name, l_name, email, username, password):
    try:
        user_doc = {
            "FirstName": f_name, "LastName": l_name, "Email": email, "UserName": username, "Password": password, "JoinDate": datetime.now()}
        collection.insert_one(user_doc)
        print("User Added")
    except Exception as e:
        print("an Error accord: ", end="")
        print(e)


def check_user_exists(username, password):
    result = collection.find_one({"UserName": username, "Password": password})
    if result:
        print("Log-in successfully")
        return result
    print("Error Password or Username")
    return False


def check_field_exists(field, data):
    result = collection.find_one({field: data})
    if result:
        return True
    return False


def delete_user(username, password):
    if check_user_exists(username, password):
        try:
            collection.delete_one(username, password)
            print("user has been deleted")
        except Exception as e:
            print("error acord: ", end="")
            print(e)


def update_data(search_dict, change_dict):
    results = collection.update_one(search_dict, {"$set": change_dict})


def inc_data(search_dict, change_dict):
    results = collection.update_one(search_dict, {"inc": change_dict})
