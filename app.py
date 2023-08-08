from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
db = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')

# Connect DB (phpMyAdmin)
mydb = mysql.connector.connect(
    host=host, user=user, password=password, db=db, port=port)
mycursor = mydb.cursor(dictionary=True)


# Get : Get All attractions
# POST : Create new attraction to DB
@app.route('/api/attractions', methods=['GET', 'POST'])
def attractions():
    if request.method == 'GET':
        mycursor.execute('SELECT * FROM attractions')
        myresult = mycursor.fetchall()
        return make_response(jsonify({'attractions': myresult}), 200)

    elif request.method == 'POST':
        data = request.get_json()  # get body
        sql = 'INSERT INTO attractions (name, detail) VALUES (%s, %s)'
        value = (data['name'], data['detail'])
        mycursor.execute(sql, value)
        mydb.commit()
        return make_response(jsonify({'rowcount': mycursor.rowcount, 'body': data}), 201)


# GET : Get attractions by ID
@app.route('/api/attractions/<id>', methods=['GET'])
def get_attractions_by_id(id):
    id = (id, )
    sql = 'SELECT * FROM attractions WHERE id = %s'
    mycursor.execute(sql, id)
    myresult = mycursor.fetchall()
    return make_response(jsonify({'attractions': myresult}), 200)


# PUT : update attriaction
# DELETE : attraction by ID
@app.route('/api/attractions/<id>', methods=['PUT', 'DELETE'])
def update_attractions_by_id(id):
    if request.method == 'PUT':
        data = request.get_json()  # get body
        sql = 'UPDATE attractions SET name = %s, detail = %s WHERE id = %s'
        val = (data['name'], data['detail'], id)
        mycursor.execute(sql, val)
        mydb.commit()
        return make_response(jsonify({'rowcount': mycursor.rowcount, 'body': data}), 200)

    elif request.method == 'DELETE':
        sql = 'DELETE FROM attractions WHERE id = %s'
        val = (id,)
        mycursor.execute(sql, val)
        mydb.commit()
        return make_response(jsonify({'rowcount': mycursor.rowcount, 'message': 'Delete attraction ID ' + id}), 200)


# Start Server
if __name__ == '__main__':
    app.run(debug=True)
