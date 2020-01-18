from flask import Flask, jsonify

app = Flask(__name__)


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
    outputList = []
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


from flask import make_response

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

from flask import request



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
