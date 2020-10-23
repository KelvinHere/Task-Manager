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
    return render_template("tasks.html", tasks=list(mongo.db.tasks.find())) # Turned task itterator to list so I can loop through it more than once

@app.route('/add_task')
def add_task():
    return render_template("addtask.html", categories=mongo.db.categories.find())

@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories)

@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
        {
            'task_name': request.form.get('task_name'),
            'category_name': request.form.get('category_name'),
            'task_description': request.form.get('task_description'),
            'due_date': request.form.get('due_date'),
            'is_urgent': request.form.get('is_urgent'),
            'task_completed': request.form.get('task_completed')
        })
    return redirect(url_for('get_tasks'))

@app.route('/done_task/<task_id>')
def done_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)}, {"$set": {"task_completed": "on"}})
    return redirect(url_for('get_tasks'))

@app.route('/redo_task/<task_id>')
def redo_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)}, {"$set": {"task_completed": ""}})
    return redirect(url_for('get_tasks'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')), 
            debug=True)
