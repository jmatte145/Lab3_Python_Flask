import flask
from markupsafe import escape
from flask import request, jsonify
from werkzeug.exceptions import abort

app = flask.Flask(__name__)
app.config["Debug"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Justin M Lab 3 Part 1 Submission</h1><p>Welcome!</p>"


@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"


tasks = [
    {
        'id': 1,
        'title': 'Schedule Scrum Meeting',
        'description': 'Call group members to schedule the meeting',
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn Python',
        'description': 'Need to find a good Python tutorial on the web',
        'done': False
    },
    {
        'id': 3,
        'title': 'Start Project',
        'description': 'Group meeting to discuss how to handle the new project.',
        'done': False
    },
]


@app.route('/api/v1/resources/tasks', methods=['GET'])
def get_task():
    return jsonify(tasks)


@app.route('/api/v1/resources/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    results = []

    if task_id is not None:
        for t in tasks:
            if t['id'] == task_id:
                results.append(t)
        return jsonify(results)
    else:
        return "Error: No id field provided. Please specify an id."
    
    
@app.route('/api/v1/resources/tasks', methods=['POST'])
def add_task():
    task = {}
    length = len(tasks)
    if not request.json:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    if request.json:
        task['id'] = int(length + 1)
        task['title'] = request.json[0]['title']
        task['description'] = request.json[0]['description']
        task['done'] = request.json[0]['done']
        tasks.append(task)
    return jsonify(tasks)


@app.route('/api/v1/resources/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json[0]['title']
    task[0]['description'] = request.json[0]['description']
    task[0]['done'] = request.json[0]['done']
    return jsonify({'task': task[0]})


@app.route('/api/v1/resources/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


app.run()
