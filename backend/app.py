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
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        # Replace this with MongoDB user retrieval logic
        if user_type == 'user':
            user = next((u for u in user if u.username == username), None)
        elif user_type == 'lawyer':
            lawyer = next((l for l in lawyer if l.username == username), None)
        else:
            flash('Invalid user type.', 'error')
            return render_template('login.html')

        if user or lawyer and check_password_hash(user.password, password):
            if user_type == 'user':
                session['user'] = username
            elif user_type == 'lawyer':
                session['lawyer'] = username

            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a new user."""

    if request.method == 'POST':
        user_type = request.form['user_type']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            # Password mismatch error
            return render_template('register.html', error='Passwords do not match.')

        if user_type == 'user':
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
        elif user_type == 'lawyer':
            lawyer = Lawyer(username=username, email=email, password=password)
            db.session.add(lawyer)
            db.session.commit()
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


@app.route('/dashboard')
def dashboard():
    
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'], cases=Case)
    elif 'lawyer' in session:
        return render_template('dashboard.html', username=session['lawyer'], cases=Case)
    else:
        flash('You need to log in first', 'error')
        # return redirect(url_for('login'))
        return render_template('dashboard.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
