from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configure the SQLite database
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

# Create the database and tables if they don't exist
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/')
def index():
    # Fetch all pets from the database
    all_pets = Pet.query.all()
    return render_template('index.html', pets=all_pets)

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        # Get data from the HTML form
        name = request.form['name']
        species = request.form['species']
        breed = request.form['breed']
        age = request.form['age']
        weight = request.form['weight']

        # Create a new Pet object and save it to the database
        new_pet = Pet(name=name, species=species, breed=breed, age=age, weight=weight)
        db.session.add(new_pet)
        db.session.commit()

        return redirect(url_for('index'))
    
    # If it's a GET request, just show the form
    return render_template('add_pet.html')

if __name__ == "__main__":
    # Run the app on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)