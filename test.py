from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import urllib.parse
import certifi  # FIX 1: Import certifi to handle SSL certificate verification

app = Flask(__name__)

# FIX 2: Load the certificate bundle provided by certifi
ca = certifi.where()

password = urllib.parse.quote_plus("MONNOH29")
uri = f"mongodb+srv://jackline:{password}@cluster0.pz7xrkr.mongodb.net/?appName=Cluster0"

# FIX 3: Add 'tlsCAFile=ca' to the MongoClient to solve the handshake error
client = MongoClient(uri, tlsCAFile=ca)

db = client["lms_db"]
students = db.students
courses = db.courses

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/create_student', methods=['POST'])
def create_student():
    name = request.form['name']
    email = request.form['email']

    students.insert_one({
        "name": name,
        "email": email,
        "role": "student",
        "enrolled_courses": []
    })

    return redirect('/')

# View data
@app.route('/view')
def view():
    all_students = list(students.find())
    all_courses = list(courses.find())
    return render_template("view.html", students=all_students, courses=all_courses)

if __name__ == "__main__":
    app.run(debug=True)
