from flask import Flask, render_template, request, redirect, url_for, print, jsonify
import psycopg2
import psycopg2.extras
from bcrypt import hashpw, gensalt, checkpw

app = Flask(__name__)

DB_HOST = "localhost"
DB_NAME = "webapp"
DB_USER = "postgres"
DB_PASS = "admin"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM UserProfile")
    list_users = cur.fetchall()
    cur.close()
    return render_template('index.html', list_users=list_users)

@app.route('/landing', methods=['POST','GET'])
def landing():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM EventDetails ORDER BY eventdate LIMIT 3")
    events = cur.fetchall()
    cur.close()
    
    return render_template('landing.html', events=events)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            print('Username and password are required')
            return redirect(url_for('Index'))
        
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("INSERT INTO UserCredentials (username, password) VALUES (%s, %s)", 
                    (username, hashed_password))
        conn.commit()
        print('User registered successfully')
        return redirect(url_for('Index'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM UserCredentials WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()
        
        if user and checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            print('Login successful')
            return redirect(url_for('Index'))
        print('Invalid username or password')
        return redirect(url_for('Index'))

@app.route('/profile', methods=['POST','GET'])
def create_profile():
    if request.method == 'POST':
        userID = request.form['userID']
        fullName = request.form['fullName']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        skills = request.form.get('skills', 'N/A')
        preferences = request.form.get('preferences', 'N/A')
        availability = request.form.get('availability', 'N/A')
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""INSERT INTO UserProfile (userID, fullName, address, city, state, zipcode, skills, preferences, availability)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (userID, fullName, address, city, state, zipcode, skills, preferences, availability))
        conn.commit()
        print('Profile created successfully')
        return redirect(url_for('Index'))

@app.route('/events', methods=['POST','GET'])
def events():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM EventDetails")
    events = cur.fetchall()
    cur.close()

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    for event in events:
        cur.execute("""
            SELECT u.fullName FROM VolunteerHistory v
            JOIN UserProfile u ON v.userID = u.userID
            WHERE v.eventID = %s
        """, (event['eventid'],))
        volunteers = cur.fetchall()
        event['volunteers'] = [v['fullName'] for v in volunteers]
    cur.close()

    return render_template('events.html', events=events)

@app.route('/check-match', methods=['POST', 'GET']) # Implement this in HTML
def check_match():
    data = request.json
    user_id = data['userId']
    event_id = data['eventId']

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM UserProfile WHERE userID = %s", (user_id,))
    user = cur.fetchone()
    cur.close()

    if user:
        message = f"You are a match for event ID {event_id}!"
    else:
        message = "User not found or does not match."

    return jsonify({'message': message})

@app.route('/volunteer', methods=['POST', 'GET'])
def volunteer():
    if request.method == 'POST':
        userID = request.form['userID']
        eventID = request.form['eventID']
        participationDate = request.form['participationDate']
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""INSERT INTO VolunteerHistory (userID, eventID, participationDate)
                       VALUES (%s, %s, %s)""",
                    (userID, eventID, participationDate))
        conn.commit()
        print('Volunteer history added successfully')
        return redirect(url_for('Index'))

@app.route('/edit_availability/<id>', methods=['POST', 'GET'])
def get_user(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM UserProfile WHERE userID = %s', (id,))
    user = cur.fetchone()
    cur.close()
    return render_template('edit_availability.html', user=user)

@app.route('/update/<id>', methods=['POST', 'GET'])
def update_user(id):
    if request.method == 'POST':
        fullName = request.form['fullName']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        skills = request.form['skills']
        preferences = request.form['preferences']
        availability = request.form['availability']
        
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE UserProfile
            SET fullName = %s, address = %s, city = %s, state = %s, zipcode = %s, 
                skills = %s, preferences = %s, availability = %s
            WHERE userID = %s
        """, (fullName, address, city, state, zipcode, skills, preferences, availability, id))
        conn.commit()
        print('User updated successfully')
        return redirect(url_for('Index'))

# Implement user/event delete functionality

if __name__ == "__main__":
    app.run(debug=True)
