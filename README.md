# Non-Profit-Management-System
# The HTML flow of the pages start @ opening_page.html
This project is a Volunteer Management System built using the Flask framework for the backend and SQLite for the database. The application manages user accounts, profiles, event details, and volunteer participation. It provides secure user authentication, profile management, event tracking, and volunteer history features.

Features
User Authentication: Secure user creation and login with encrypted passwords.
User Profiles: Management of user details including full name, address, skills, preferences, and availability.
Event Management: Storage and management of event details such as name, description, location, required skills, urgency, and date.
Volunteer Tracking: Tracking volunteer participation in events.
State Information: Storage of state codes and names.
Database Schema
The database schema consists of the following tables:

UserCredentials: Stores user credentials with encrypted passwords.
ID (Primary Key)
username (Unique)
password

UserProfile: Stores detailed user information.
ID (Primary Key, Foreign Key linking to UserCredentials)
full_name
address
city
state
zipcode
skills
preferences
availability

EventDetails: Stores event information.
event_id (Primary Key)
event_name
description
location
required_skills
urgency
event_date

VolunteerHistory: Tracks volunteer participation in events.
history_id (Primary Key)
user_id (Foreign Key linking to UserProfile)
event_id (Foreign Key linking to EventDetails)
participation_date

States: Stores state codes.
state_code (Primary Key)
