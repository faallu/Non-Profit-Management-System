CREATE DATABASE webapp;

CREATE TABLE users (
    userID SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(10), UNIQUE NOT NULL
    address TEXT,
    location VARCHAR(100),
    skills TEXT[],
    availability TIMESTAMP
    participate_date TIMESTAMP
);

CREATE TABLE events (
    eventID SERIAL PRIMARY KEY,
    event_name VARCHAR(100),
    location VARCHAR(100),
    skills_needed TEXT[],
    availability_needed TIMESTAMP
);

CREATE TABLE volunteers_history (
    historyID SERIAL PRIMARY KEY,
    userID INTEGER,
    eventID INTEGER,
    participation_date TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES UserProfile(userID),
    FOREIGN KEY (eventID) REFERENCES EventDetails(eventId)
);
