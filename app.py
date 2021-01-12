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
    images = []

    #Getting images 
    cur1 = get_db().execute("SELECT pid, imageUrl FROM locationImages;")
    columns =  [column[0] for column in cur.description]
    for r in cur1.fetchall():
        images.append(dict(zip(columns, row)))
    print("hereeeeeee");
    #Getting locations
    cur2 = get_db().execute("SELECT pid, pname, jpname, lat, lon, category, label, description, popularity, webUrl FROM location;")
    locations = [column[0] for column in cur.description]

    for row in cur2.fetchall():
        response.append(dict(zip(locations, row)))
        
    for i in range (len(response)):
        response[i]["Images"].append("");
        for j in range (len(images)):
            if (images[j].pid == response[i].pid):
                 response[i]["Images"].append(images[j].imageUrl);
    
    cur.close()

    return jsonify(response)

@app.route('/locations/images/', methods=['GET'])
@cross_origin()
def locationImages():
    response = []

    #Getting pictures
    cur = get_db().execute("SELECT id, pid, imageUrl FROM locationImages;")
    columns = [column[0] for column in cur.description]

    for row in cur.fetchall():
        response.append(dict(zip(columns, row)))
    
    cur.close()

    return jsonify(response)

@app.route('/locations/images/<int:pid>', methods=['GET'])
@cross_origin()
def locationImagesPid(pid):
    response = []

    #Getting pictures by pid
    cur = get_db().execute("SELECT id, pid, imageUrl FROM locationImages WHERE pid = "+str(pid)+";")
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
    cur = get_db().execute("SELECT pid, pname, jpname, lat, lon, category, label, description, popularity FROM location WHERE pid = "+str(pid)+";")
    columns = [column[0] for column in cur.description]

    for row in cur.fetchall():
        response.append(dict(zip(columns, row)))
    
    cur.close()

    return jsonify(response)

@app.route('/locations/delete/<int:pid>', methods=['GET'])
@cross_origin()
def locationDelete(pid):
    
    if pid is None:
        return jsonify({
            "ERROR": "No PID was sent."
        })

    else:
        #deleting location by pid
        cur = get_db().execute("DELETE FROM location WHERE pid = "+str(pid)+";")
        get_db().commit()

        return jsonify({
            "Message": f"Location was successfully deleted.",
        })

@app.route('/locations/create', methods=['POST'])
@cross_origin()
def locationCreate():

    pname = request.form.get('pname');
    jpname = request.form.get('jpname');
    lat = request.form.get('lat');
    lon = request.form.get('lon');
    category = request.form.get('category');
    label = request.form.get('label');
    description = request.form.get('description');
    popularity = request.form.get('popularity');

    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if (jpname and lat and lon):
        if pname is None:
            pname = ""
        get_db().execute("INSERT INTO 'location' ('pname','jpname','lat','lon','category','label','description','popularity') VALUES (\'"+str(pname)+"','"+str(jpname)+"','"+str(lat)+"','"+str(lon)+"','"+str(category)+"','"+str(label)+"','"+str(description)+"','"+str(popularity)+"');")
        get_db().commit()
        return jsonify({
            "Message": "New location successfully inserted in database."
        })
       
    else:
        return jsonify({
            "ERROR": "pname or lat or lon not found."
        })