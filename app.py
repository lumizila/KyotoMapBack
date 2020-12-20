from flask import Flask, request, jsonify, g
from flask_cors import CORS, cross_origin
import sqlite3
import sys

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

DATABASE = 'KyotoMap.db'

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#-------------------------------------------------------------
#TEST FUNCTIONS

@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello, cross origin World!'

#EXAMPLE OF GET
@app.route('/getecho/', methods=['GET'])
@cross_origin()
def respond():
    # Retrieve the name from url parameter
    echo = request.args.get("echo", None)

    # For debugging
    print(f"got string {echo}")

    response = {}

    # Check if user sent a name at all
    if not echo:
        response["ERROR"] = "no string found, please send a string."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"The server echoes: {echo}"

    # Return the response in json format
    return jsonify(response)

if __name__ == '__main__':
	app.run()

#-------------------------------------------------------------
#REAL API

@app.route('/locations/', methods=['GET'])
@cross_origin()
def locations():
    response = []

    #Getting locations
    cur = get_db().execute("SELECT pid, pname, jpname, lat, lon FROM location;")
    columns = [column[0] for column in cur.description]

    for row in cur.fetchall():
        response.append(dict(zip(columns, row)))
    
    cur.close()

    return jsonify(response)

@app.route('/locations/<int:pid>', methods=['GET'])
@cross_origin()
def locationsById(pid):
    response = []

    #Getting location by pid
    cur = get_db().execute("SELECT pid, pname, jpname, lat, lon FROM location WHERE pid = "+str(pid)+";")
    columns = [column[0] for column in cur.description]

    for row in cur.fetchall():
        response.append(dict(zip(columns, row)))
    
    cur.close()

    return jsonify(response)

@app.route('/locations/create', methods=['POST'])
@cross_origin()
def locationCreate():

    pname = request.form.get('pname');
    jpname = request.form.get('jpname');
    lat = request.form.get('lat');
    lon = request.form.get('lon');

    print(pname)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if (pname and lat and lon):
        return jsonify({
            cur = get_db().execute("INSERT INTO 'location' ('pname','jpname','lat','lon') VALUES ("+str(pname)+","+str(jpname)+","+str(lat)+","+str(lon)+")")
            "Message": f"New location successfully created.",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "pname or lat or lon not found."
        })