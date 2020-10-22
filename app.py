import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Create constants for URI login data / database / collection in database
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE = "task_manager"
COLLECTION = "tasks"

app.config["MONGO_DBNAME"] = DATABASE
app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app) #Connect to mongoDB through flask_pymongo > PyMongo(this_flask_app)

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')), 
            debug=True)
