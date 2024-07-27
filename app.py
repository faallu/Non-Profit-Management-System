from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)
current_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////webapp.db'
current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#app.app_context().push()
#db.create_all()

class UserCredentials(db.Model):
    #__tablename__ = 'UserCredentials'
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)

    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt())

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password)

class UserProfile(db.Model):
    #__tablename__ = 'UserProfile'
    userID = db.Column(db.Integer, ForeignKey('UserCredentials.ID'), primary_key=True)
    fullName = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    #For skills, preferences and availability, if the user don't have any of these, it automatically sets it to N/A.
    skills = db.Column(db.Text, default = 'N/A')
    preferences = db.Column(db.Text, default = 'N/A')
    availability = db.Column(db.Text, default = 'N/A')
    user = relationship('UserCredentials', back_populates='profile')

UserCredentials.profile = relationship('UserProfile', uselist=False, back_populates='user')

class EventDetails(db.Model):
    #__tablename__ = 'EventDetails'
    eventID = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.Text)
    requiredSkills = db.Column(db.Text)
    urgency = db.Column(Boolean)
    eventDate = db.Column(Date, nullable=False)

class VolunteerHistory(db.Model):
    #__tablename__ = 'VolunteerHistory'
    historyID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, ForeignKey('UserCredentials.ID'))
    eventID = db.Column(db.Integer, ForeignKey('EventDetails.eventID'))
    participationDate = db.Column(db.Date)
    user = relationship('UserCredentials')
    event = relationship('EventDetails')

class States(db.Model):
    #__tablename__ = 'States'
    stateCode = db.Column(db.String(2), primary_key=True)

#db.create_all()

@app.route('/register', methods=['GET', 'POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    user = UserCredentials(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = UserCredentials.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/profile', methods=['POST'])
def create_profile():
    data = request.json
    userID = data.get('userID')
    fullName = data.get('fullName')
    address = data.get('address')
    city = data.get('city')
    state = data.get('state')
    zipcode = data.get('zipcode')
    skills = data.get('skills')
    preferences = data.get('preferences')
    availability = data.get('availability')
    if not userID or not fullName:
        return jsonify({'error': 'UserID and FullName are required'}), 400
    profile = UserProfile(
        userID=userID,
        fullName=fullName,
        address=address,
        city=city,
        state=state,
        zipcode=zipcode,
        skills=skills,
        preferences=preferences,
        availability=availability
    )
    db.session.add(profile)
    db.session.commit()
    return jsonify({'message': 'Profile created successfully'}), 201

@app.route('/events', methods=['GET', 'POST'])
def create_event():
    data = request.json
    eventName = data.get('eventName')
    description = data.get('description')
    location = data.get('location')
    requiredSkills = data.get('requiredSkills')
    urgency = data.get('urgency')
    eventDate = data.get('eventDate')
    if not eventName or not eventDate:
        return jsonify({'error': 'EventName and EventDate are required'}), 400
    event = EventDetails(
        eventName=eventName,
        description=description,
        location=location,
        requiredSkills=requiredSkills,
        urgency=urgency,
        eventDate=eventDate
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully'}), 201

@app.route('/volunteer', methods=['GET', 'POST'])
def volunteer():
    data = request.json
    userID = data.get('userID')
    eventID = data.get('eventID')
    participationDate = data.get('participationDate')
    if not userID or not eventID:
        return jsonify({'error': 'UserID and EventID are required'}), 400
    history = VolunteerHistory(
        userID=userID,
        eventID=eventID,
        participationDate=participationDate
    )
    db.session.add(history)
    db.session.commit()
    return jsonify({'message': 'Volunteer history recorded successfully'}), 201

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
