from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Models ---
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    
    # Relationships: Links the pet to their records
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

# Create the database tables
with app.app_context():
    db.create_all()

# --- Routes ---

@app.route('/')
def index():
    all_pets = Pet.query.all()
    return render_template('index.html', pets=all_pets)

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        new_pet = Pet(
            name=request.form['name'],
            species=request.form['species'],
            breed=request.form['breed'],
            age=request.form['age'],
            weight=request.form['weight']
        )
        db.session.add(new_pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_pet.html')

# NEW: Pet Profile Route
@app.route('/pet/<int:pet_id>')
def pet_profile(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('pet_profile.html', pet=pet)

# NEW: Add Feeding Route
@app.route('/pet/<int:pet_id>/add_feeding', methods=['POST'])
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

# NEW: Add Health Record Route
@app.route('/pet/<int:pet_id>/add_health', methods=['POST'])
def add_health(pet_id):
    date_obj = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    new_health = Health(pet_id=pet_id, date=date_obj, notes=request.form['notes'])
    db.session.add(new_health)
    db.session.commit()
    return redirect(url_for('pet_profile', pet_id=pet_id))

# NEW: Add Vaccine Reminder Route
@app.route('/pet/<int:pet_id>/add_vaccine', methods=['POST'])
def add_vaccine(pet_id):
    due_obj = datetime.strptime(request.form['next_due'], '%Y-%m-%d').date()
    new_vaccine = Vaccine(pet_id=pet_id, name=request.form['name'], next_due=due_obj)
    db.session.add(new_vaccine)
    db.session.commit()
    return redirect(url_for('pet_profile', pet_id=pet_id))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)