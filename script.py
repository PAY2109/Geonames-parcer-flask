from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})

@app.route('/geonames/<string:geonameid>', methods=['GET'])
def get_info(geonameid):

    f = open("RU.txt", "r", encoding='utf-8')
    for line in f.readlines():   # read lines
        lineList = line.split()
        #print(lineList[0])
        if lineList[0] == geonameid:
            print(line)
            return jsonify({'info': lineList})
            break
    f.close()

    return jsonify({'info': 'No GeoName with such id'})

@app.route('/geonameslist', methods=['POST'])
def get_info_by_list():
    if not request.json:
        abort(400)
    cities = request.json['cities']
    outputList = [[]]
    f = open("RU.txt", "r", encoding='utf-8')

    for line in f.readlines():   # read lines
        lineList = line.split()
        #print(lineList[0])
        for city in cities:
            if city in line:
                outputList.append(lineList)

    f.close()
    return jsonify({'info': outputList})


@app.route('/geonamestwocities', methods=['POST'])
def get_info_for_two():
    if not request.json:
        abort(400)

    cities = request.json['cities']
    city1 = []
    city2 = []
    outputList = [[]]
    f = open("RU.txt", "r", encoding='utf-8')

    for line in f.readlines():   # read lines
        lineList = line.split()

        for city in cities:
            if city in line:
                if city1 == []:
                    city1 = lineList
                    continue
                elif city in city1 and int(city1[-5]) < int(lineList[-5]):
                    city1 = lineList
                    continue
                elif city2 == []:
                    city2 = lineList
                    continue
                elif city in city2 and int(city2[-5]) < int(lineList[-5]):
                    city2 = lineList
                    continue
    f.close()
    latitude1 = 0
    latitude2 = 0
    for spec in city1:
        if '.' in spec:
            latitude1 = float(spec)
            break
    for spec in city2:
        if '.' in spec:
            latitude2 = float(spec)
            break
    northernCity = ""
    if latitude1 < latitude2:
        northernCity = city1[1]
    else:northernCity = city2[1]
    equalTZ = city1[-2] == city2[-2]
    equalTZString = ""
    if equalTZ:
        equalTZString = "equals"
    else: equalTZString = "different"
    return jsonify({'info': [city1, city2], 'isclosertonorth': northernCity, 'timezone': equalTZString})

from flask import abort


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


from flask import make_response


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


from flask import request


@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


from flask import url_for


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
