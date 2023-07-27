import psycopg2
import os
from flask import Flask,request


CREATE_STUDENT_TABLE=("CREATE TABLE IF NOT EXISTS student(id SERIAL PRIMARY KEY,name TEXT,class TEXT);")

INSERT_STUDENT_RETURN_ID="INSERT INTO student (name,class) VALUES (%s,%s) RETURNING id;"


app=Flask(__name__)
conn = psycopg2.connect(
        host="localhost",
        database="FlaskAPI1",
        user='postgres',
        password='Shiva@09')

@app.route("/api/studentCreate",methods=['POST'])
def create():
    data=request.get_json()
    name=data["name"]
    year=data["class"]

    with conn as cursor:
        cursor = cursor.cursor()
        cursor.execute(CREATE_STUDENT_TABLE)
        cursor.execute(INSERT_STUDENT_RETURN_ID,(name,year))
        stud_id=cursor.fetchone()[0]

    return{"id":stud_id,"message":f"Student {name} inserted"},201

@app.route("/api/studentDelete/<id>",methods=['DELETE'])
def delete(id):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM student WHERE id={id}")
            if cursor.rowcount>0:
                return{"id":id,"message":"Student deleted Succesfully"},201
            else:
                return{"id":id,"message":f"{id} is not present to delete"},201

@app.route("/api/studentUpdate",methods=['PUT'])
def update():
    data=request.get_json()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(f"UPDATE student SET name='{data['name']}',class='{data['class']}' where id={data['id']}")
            if cursor.rowcount>0:
                return "Student Updated Successfully"
            else:
                return "No data found to Update"

app.run(debug=True)




