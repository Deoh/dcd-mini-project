import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'task_manager'
app.config["MONGO_URI"] = 'mongodb+srv://new_root_dh:r00tUserDh@myfirstcluster-lhfu5.mongodb.net/task_manager?retryWrites=true&w=majority'

mongo = PyMongo(app)


# -------------------------task.html
@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    """Render the tasks.html (homepage) and finds tasks collection info from the task_manager db"""
    return render_template("tasks.html", tasks=mongo.db.tasks.find())


# -------------------------addtask.html
@app.route('/add_task')
def add_task():
    """Render addtask.html and finds the catergories collection info from the task_manager db """
    return render_template("addtask.html", categories=mongo.db.categories.find())

# create function
@app.route('/insert_task', methods=['POST'])
def insert_task():
    """takes the form info from the addtask.html template and adds it to the tasks collection in task_manger db(mongo),
        then rediects back to tasks.html(the get_tasks route)"""
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))


# -------------------------edittask.html
@app.route('/edit_task/<task_id>') #advance routing for the edit button
def edit_task(task_id):
    """Render edittask.html and finds both the tasks(one of) and catergories collection info from the task_manager db,
        to be the preselects on the edit task form"""
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template("edittask.html", task=the_task, categories=all_categories)

# update function
@app.route('/update_task/<task_id>', methods=["POST"]) #advance routing for the edit task button
def update_task(task_id):  
    """takes the form info from the edittask.html template and updates the selected tasks_id in task_manger db(mongo),
        then rediects back to tasks.html(the get_tasks route)"""
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
                 {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))


@app.route('/delete_task/<task_id>') #advance routing for the done button
def delete_task(task_id):
    """Removes the tasks data corresponding to the id selected"""
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template("editcategory.html",
                           category=mongo.db.categories.find_one(
                               {'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for("get_categories"))


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
