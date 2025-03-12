
"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# define endpoint for adding a new list
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # check request
    data = request.get_json(force=True)
    if not data or len(data) > 1 or 'name' not in data or not data['name']:
        abort(400)

    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 200

# define endpoint for getting and deleting existing todo lists
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def get_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify(list_item), 200
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return jsonify({'msg': 'success'}), 200
    else:
        abort(405)

# define endpoint for getting all lists
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200

# define endpoint for returning all entries for a list
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_all_entries_from_a_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
     # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)

    entries = []
    for e in todos:
        if e['list'] == list_id:
            entries.append(e)

    return jsonify({entries}), 200
    
# Add an entry to a todo-list
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_entry(list_id):
    # check request
    data = request.get_json(force=True)
    if not data or len(data) > 2 or 'name' not in data or 'description' not in data or not (data['name'] and data['description']):
        abort(400)
    
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
     # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)

    new_entry = request.get_json(force=True)
    print('Got new entry to be added: {}'.format(new_entry))
    new_entry['id'] = str(uuid.uuid4())
    new_entry['list'] = list_id
    todos.append(new_entry)
    return jsonify(new_entry), 200

# update an entry at a list
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT', 'DELETE'])
def updateEntry(list_id, entry_id):
    if request.method == 'PUT':
        # check request
        data = request.get_json(force=True)
        if not data or len(data) > 2 or 'name' not in data or 'description' not in data or not (data['name'] and data['description']):
            abort(400)
     # find todo list depending on given list id
    entry_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            for e in todos:
                if e['id'] == entry_id and e['list'] == list_id:
                    entry_item = e
                    break
    # if the given list id is invalid, return status code 404
    if not entry_item:
        abort(404)

    for e in todos:
        if e['id'] == entry_id and e['list'] == list_id:
            if request.method == 'PUT':
                new_entry_data = request.get_json(force=True)
                entry_item['name'] = new_entry_data['name']
                entry_item['description'] = new_entry_data['description']
                return jsonify(entry_item), 200
            elif request.method == 'DELETE':
                # delete list with given id
                print('Deleting entry...')
                todos.remove(e)
                return jsonify({'msg': 'success'}), 200

@app.errorhandler(500)
def internal_server_error(error):
    abort(500)

if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
