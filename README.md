# Smart Pet Care Monitoring & Management System 🐾

A web-based application developed to help pet owners manage and monitor their pets' daily care activities efficiently. This system provides a centralized dashboard where users can maintain pet profiles and track essential details.

## 🌟 Features

* **Centralized Dashboard:** View all your pets in one clean, responsive interface.
* **Pet Profiles:** Add and store detailed information for each pet, including name, species, breed, age, and weight.
* **Database Integration:** Persistent storage using SQLite ensures your data is saved automatically.
* **Containerized:** Fully Dockerized for consistent deployment across any environment.
* **Responsive UI:** Styled with Bootstrap 5 to work seamlessly on desktop and mobile devices.

## 🛠️ Technologies Used

* **Backend:** Python 3, Flask
* **Database:** SQLite, Flask-SQLAlchemy
* **Frontend:** HTML5, Jinja2 Templating, Bootstrap 5 (CSS)
* **DevOps:** Docker, Git/GitHub


## 🚀 Getting Started

You can run this application directly on your local machine using Python, or inside a Docker container.

### Prerequisites
* Python 3.8+ installed (if running locally)
* Docker Desktop installed and running (if running via Docker)
* Git

### Option 1: Run Locally (Without Docker)

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd smart-pet-care
Create and activate a virtual environment:

Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install the required dependencies:

Bash
pip install -r requirements.txt
Run the Flask application:

Bash
python app.py
Access the app:
Open your web browser and navigate to http://localhost:5000.

Option 2: Run with Docker (Recommended)
Running with Docker ensures you don't run into any version mismatch or dependency issues.

Ensure Docker Desktop is running.

Build the Docker image:

Bash
docker build -t pet-care-app .
Run the Docker container:

Bash
docker run -p 5000:5000 pet-care-app
Access the app:
Open your web browser and navigate to http://localhost:5000.

📂 Project Structure
Plaintext
smart-pet-care/
│
├── app.py                 # Main backend application file (Flask logic & DB models)
├── requirements.txt       # Python dependencies list
├── Dockerfile             # Instructions to build the Docker image
├── .dockerignore          # Files to exclude from the Docker build
├── instance/              # Auto-generated folder containing the SQLite database
│
└── templates/             # HTML template files
    ├── base.html          # Base layout and navigation bar
    ├── index.html         # Main dashboard displaying all pets
    └── add_pet.html       # Form to add a new pet profile

    
🔮 Future Enhancements
Feeding Schedules: Add functionality to log feeding times and food types.

Vaccination Tracker: Implement a system to track past vaccinations and alert users of upcoming due dates.

User Authentication: Allow multiple users to register, log in, and manage their own specific pets privately.