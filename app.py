from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_super_secret_key_here'

db = SQLAlchemy(app)

# Setup Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    pets = db.relationship('Pet', backref='owner', lazy=True)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    feedings = db.relationship('Feeding', backref='pet', lazy=True, cascade="all, delete-orphan")
    health_records = db.relationship('Health', backref='pet', lazy=True, cascade="all, delete-orphan")
    vaccines = db.relationship('Vaccine', backref='pet', lazy=True, cascade="all, delete-orphan")

class Feeding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    food_type = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    portion = db.Column(db.String(50))

class Health(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String(250), nullable=False)

class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    next_due = db.Column(db.Date, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
            
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_pets = Pet.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', pets=user_pets)

@app.route('/add_pet', methods=['GET', 'POST'])
@login_required
def add_pet():
    if request.method == 'POST':
        new_pet = Pet(
            name=request.form['name'],
            species=request.form['species'],
            breed=request.form['breed'],
            age=request.form['age'],
            weight=request.form['weight'],
            user_id=current_user.id
        )
        db.session.add(new_pet)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_pet.html')

# --- Missing Pet Management Routes Restored Here ---

@app.route('/pet/<int:pet_id>')
@login_required
def pet_profile(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    # Security: Make sure the logged-in user actually owns this pet!
    if pet.user_id != current_user.id:
        flash('You do not have permission to view this profile.')
        return redirect(url_for('dashboard'))
    return render_template('pet_profile.html', pet=pet)

@app.route('/pet/<int:pet_id>/add_feeding', methods=['POST'])
@login_required
def add_feeding(pet_id):
    new_feeding = Feeding(
        pet_id=pet_id,
        food_type=request.form['food_type'],
        time=request.form['time'],
        portion=request.form['portion']
    )
    db.session.add(new_feeding)
    db.session.commit()
    return redirect(url_for('pet_profile', pet_id=pet_id))

@app.route('/pet/<int:pet_id>/add_health', methods=['POST'])
@login_required
def add_health(pet_id):
    date_obj = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    new_health = Health(pet_id=pet_id, date=date_obj, notes=request.form['notes'])
    db.session.add(new_health)
    db.session.commit()
    return redirect(url_for('pet_profile', pet_id=pet_id))

@app.route('/pet/<int:pet_id>/add_vaccine', methods=['POST'])
@login_required
def add_vaccine(pet_id):
    due_obj = datetime.strptime(request.form['next_due'], '%Y-%m-%d').date()
    new_vaccine = Vaccine(pet_id=pet_id, name=request.form['name'], next_due=due_obj)
    db.session.add(new_vaccine)
    db.session.commit()
    return redirect(url_for('pet_profile', pet_id=pet_id))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)