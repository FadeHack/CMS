from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Case, Lawyer
from flask_login import login_user
from flask import jsonify
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


app = Flask(__name__, template_folder='../frontend/templates',
            static_folder='../frontend/static', static_url_path='/static')

# # MongoDB connection settings
mongo_username = "Cluster55742"
mongo_password = "fUZbWUl9fntK"
mongo_cluster = "Cluster55742"
mongo_dbname = "Case-Management-Portal"

# # Create MongoDB client
# client = MongoClient(f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_cluster}/{mongo_dbname}?retryWrites=true&w=majority")
# print(client)
# db = client[mongo_dbname]
# mongo = PyMongo(app)

# Sample user model for demonstration purposes

##############################################################
uri = 'mongodb+srv://Cluster55742:fUZbWUl9fntK@cluster55742.rnk3nbk.mongodb.net/?appName=mongosh+2.0.1&authMechanism=DEFAULT&tls=true'

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


mongo_dbname = client['Case-Management-Portal']
users_collection = mongo_dbname['Users']
assessments_collection = mongo_dbname['Lawyer']
results_collection = mongo_dbname['Admin']
##############################################################

# Sample user model for demonstration purposes


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
        # Add more feature data as needed
    ]
    return render_template('index.html', features=features)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Perform basic form validation
        if not email or not password or not role:
            error = 'Please fill out all required fields.'
            return render_template('login.html', error=error)

        # Check user credentials from MongoDB
        user = users_collection.find_one({'email': email, 'password': password, 'role': role})

        if user:
            session['email'] = user['email']
            session['role'] = user['role']
            return render_template('dashboard.html', username=session['email'], role=session['role'])
        else:
            error = 'Invalid username, password, or role. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a new user."""

    if request.method == 'POST':
        user_type = request.form['role']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            # Password mismatch error
            return render_template('register.html', error='Passwords do not match.')

        if user_type == 'user':
            user = User(username=username, email=email, password=password)
            mongo_dbname.session.add(user)
            mongo_dbname.session.commit()
            login_user(user)
        elif user_type == 'lawyer':
            lawyer = Lawyer(username=username, email=email, password=password)
            mongo_dbname.session.add(lawyer)
            mongo_dbname.session.commit()
            login_user(lawyer)
        else:
            return render_template('register.html', error='Invalid user type.')

        return redirect(url_for('index'))

    return render_template('register.html')


@app.route("/insert/case", methods=["POST"])
def insert_case():
    """Inserts a new case document into the database."""

    case_data = request.json
    case = Case(
        case_number=case_data["case_number"],
        case_type=case_data["case_type"],
        client_name=case_data["client_name"],
        lawyer_id=case_data["lawyer_id"],
    )
    db.session.add(case)
    db.session.commit()
    return jsonify({"message": "Case inserted successfully."})


# @app.route('/dashboard')
# def dashboard():

#     pass


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
