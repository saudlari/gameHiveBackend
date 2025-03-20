from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_cors import CORS
import os

# instance APP
app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(144), unique=False, nullable=False)
    is_done = db.Column(db.Boolean, default=False, nullable=False) 

    def __init__(self, title, description, done):
        self.title = title
        self.description = description
        self.done = done

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'is_done')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# Endpoint to create a new Task
@app.route('/api/tasks', methods=["POST"])
def add_task():
    task = request.get_json()
    title = task.get('title')
    description = task.get('description')
    is_done = task.get('is_done')
    
    new_task = Task(title, description, is_done)
    db.session.add(new_task)
    db.session.commit()

    result = task_schema.dump(new_task)
    return jsonify(result)
    


# Endpoint to query all tasks
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    all_tasks =  db.session.query(Task).all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)


# Endpoint for querying a single task
@app.route("/api/tasks/<id>", methods=["GET"])
def get_task(id):
    
    get_task = db.session.query(Task).filter(Task.id == id).first()
    return jsonify(task_schema.dump(get_task))


# Endpoint for updating a task
@app.route("/api/tasks/<id>", methods=["PUT"])
def task_update(id):
    task = request.get_json()
    title = task.get('title')
    description = task.get('description')
    is_done = task.get('is_done')

    task_update = db.session.query(Task).filter(Task.id == id).first()

    if title != None:
        task_update.title = title
    if description != None:
        task_update.description = description
    if is_done != None:
        task_update.is_done = is_done


    db.session.commit()
    return jsonify(task_schema.dump(task_update))


# Endpoint for deleting a task 
@app.route("/api/tasks/<id>", methods=["DELETE"])
def task_delete(id):
    task = db.session.query(Task).filter(Task.id == id).first()
    db.session.delete(task)
    db.session.commit()

    return jsonify("The following task has been deleted!", task_schema.dump(task))


# Health Checker
@app.route("/api/healthchecker", methods=["GET"])
def healthchecker():
    return {"status": "success", "message": "Integrate Flask Framework with Next.js"}

if __name__ == "__main__":
    app.run(debug=True, port=8000)
