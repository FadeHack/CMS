from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
import random 
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)




app = Flask(__name__, template_folder='../frontend/templates',
            static_folder='../frontend/static', static_url_path='/static')

app.secret_key = 'fniemcoampi883nc93mk02'


mongo_username = "Cluster55742"
mongo_password = "fUZbWUl9fntK"
mongo_cluster = "Cluster55742"
mongo_dbname = "Case-Management-Portal"


uri = 'mongodb+srv://Cluster55742:fUZbWUl9fntK@cluster55742.rnk3nbk.mongodb.net/?appName=mongosh+2.0.1&authMechanism=DEFAULT&tls=true'


client = MongoClient(uri, server_api=ServerApi('1'))


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


mongo_dbname = client['Case-Management-Portal']
users_collection = mongo_dbname['Registration']
case_collection = mongo_dbname['Case']



@app.route('/')
def index():
    features = [
        {
            'title': 'Feature 1',
            'description': 'Description of Feature 1.',
            'image': 'hammer.jpg',
            'link': '#',
        },
        {
            'title': 'Feature 2',
            'description': 'Description of Feature 2.',
            'image': 'hammer.jpg',
            'link': '#',
        },
        {
            'title': 'Feature 3',
            'description': 'Description of Feature 3.',
            'image': 'hammer.jpg',
            'link': '#',
        },
        {
            'title': 'Feature 3',
            'description': 'Description of Feature 3.',
            'image': 'hammer.jpg',
            'link': '#',
        },
        {
            'title': 'Feature 3',
            'description': 'Description of Feature 3.',
            'image': 'hammer.jpg',
            'link': '#',
        },
        {
            'title': 'Feature 3',
            'description': 'Description of Feature 3.',
            'image': 'hammer.jpg',
            'link': '#',
        },
        
    ]
    return render_template('index.html', features=features)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        
        if not email or not password or not role:
            error = 'Please fill out all required fields.'
            return render_template('login.html', error=error)

        
        user = users_collection.find_one({'email': email, 'password': password, 'role': role})
        print("user is ", user)

        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username, password, or role. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form['role']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        phone_number = request.form['phoneNumber']
        address = request.form['address']
        gender = request.form['gender']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        state = request.form['state']
        country = request.form['country']
        pin_code = int(request.form['pincode'])

        
        if role == 'Lawyer':
            field_of_expertise = request.form['fieldOfExpertise']
            number_of_cases_won = int(request.form['casesWon'])
            years_of_experience = int(request.form['yearsOfExperience'])
            occupation = None
        else:
            occupation = request.form['occupation']
            field_of_expertise = None
            number_of_cases_won = None
            years_of_experience = None

        registration = {
            'email':email,
            'username':username,
            'password':password,
            'role':role,
            'phone_number':phone_number,
            'address':address,
            'gender':gender,
            'dob':dob,
            'state':state,
            'occupation' : occupation,
            'country':country,
            'pin_code':pin_code,
            'field_of_expertise':field_of_expertise,
            'number_of_cases_won':number_of_cases_won,
            'years_of_experience':years_of_experience
        }
        if password == confirm_password:
            users_collection.insert_one(registration)
            flash('Registration successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Password does not match', 'failure')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/registerCase', methods=['GET', 'POST'])
def registerCase():
    if request.method == 'POST':
        role = request.form['role']
        case_type = request.form['caseType']
        case_name = request.form['caseName']
        case_description = request.form['caseDescription']
        aadhar_number = int(request.form['aadharNumber'])

        case_register = {
            'role':role,
            'case_type':case_type,
            'case_description': case_description,
            'case_name' : case_name,
            'aadhar_number':aadhar_number
        }

        result = case_collection.insert_one(case_register)
        inserted_id = result.inserted_id
        print(inserted_id)

        flash('Registration successful', 'success')
        # return redirect(url_for('dashboard.html'))
        return inserted_id
    # return render_template(case_registration)

@app.route('/cases')
def get_cases():
 
    cases = list(case_collection.find())
    print(cases)
        
    return JSONEncoder().encode(cases)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == "GET":
        contacts = []
        for i in range(1, 6):
            contact = {
                'Id': f'#{random.randint(1000, 9999)}',
                'Name': 'User ' + str(i),
                'Expertise': 'Product ' + str(i),
                'YOE': random.randint(1, 15),
                'CWS': random.randint(1,20),
                'avatar': f'None',
            }
            contacts.append(contact)
        
        return render_template('dashboard.html', username=session['username'], role=session['role'], contacts = contacts)



@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
