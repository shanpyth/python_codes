from flask import Flask,request,jsonify
import mysql.connector

app=Flask(__name__)
db=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Srija-123',
    database='mydatabase'
)


@app.route('/addStudent',methods=['POST'])
def add_student():
    data=request.get_json()
    name=data.get('name')
    mark=data.get('mark')

    cursor=db.cursor()
    sql_query = "INSERT INTO students(name, mark) VALUES (%s, %s)"
    cursor.execute(sql_query, (name, mark))
    db.commit()
    return jsonify({'message': 'posted'}), 200

@app.route('/fetchAll', methods=['GET'])
def fetch_all():
    cursor=db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    cursor.close()
    return jsonify(rows)

@app.route('/fetchbyid/<int:id>', methods=['GET'])
def fetchById(id):
    cursor=db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,)) #Here we keep comma after id to make it a tuple
    data=cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/update', methods=['PUT'])
def update_data():
    id=request.json.get('id')
    name=request.json.get('name')
    mark=request.json.get('mark')
    cursor=db.cursor()
    query = "UPDATE students SET name = %s, mark = %s WHERE id = %s"
    cursor.execute(query, (name, mark, id))
    db.commit()
    cursor.close()
    return jsonify({'message': 'updated'}), 200


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_data(id):
    cursor=db.cursor()
    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (id,))   
    db.commit()
    cursor.close()
    return jsonify({'message': 'deleted'}), 200

@app.route('/postList',methods=['POST'])
def post_list():
    reqData=request.json
    cursor=db.cursor()
    query = "INSERT INTO students(name, mark) VALUES (%s, %s)"
    for student in reqData:
        cursor.execute(query, (student['name'], student['mark']))
    db.commit()
    cursor.close()
    return jsonify({'message': 'list posted'}), 200


if __name__ == '__main__':
    print("Connecting to DB")
    app.run()