from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Case, Lawyer
from flask_login import login_user


app = Flask(__name__, template_folder='../frontend/templates',
            static_folder='../frontend/static', static_url_path='/static')
# Replace with a strong secret key
app.config['SECRET_KEY'] = 'fUZbWUl9fntK'
# Replace with your MongoDB URI
app.config['MONGO_URI'] = 'mongodb+srv://Cluster55742:fUZbWUl9fntK@cluster55742.rnk3nbk.mongodb.net/?appName=mongosh+2.0.1&authMechanism=DEFAULT&tls=true'

mongo = PyMongo(app)

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

        # Replace this with MongoDB user retrieval logic
        user = next((u for u in user if u.username == username), None)

        if user and check_password_hash(user.password, password):
            session['user'] = username
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
        return render_template('dashboard.html', username=session['user'], cases=cases)
    elif 'lawyer' in session:
        return render_template('dashboard.html', username=session['lawyer'], cases=cases)
    else:
        flash('You need to log in first', 'error')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
