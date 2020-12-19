from flask import Flask, request, jsonify, g
from flask_cors import CORS, cross_origin
import sqlite3
import sys

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

DATABASE = 'kyotomap20.db'

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

@app.route('/')
@cross_origin()
def hello_world():
    return 'Hello, cross origin World!'

#EXAMPLE OF GET
@app.route('/getecho/', methods=['GET'])
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