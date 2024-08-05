const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 5501;

app.use(cors());
app.use(bodyParser.json());

// Sample data
const events = [
    {
        id: 1,
        name: 'Beach Cleanup',
        skillsNeeded: ['Teamwork', 'Organization'],
        location: 'Sunset Beach, California',
        dateTime: '2024-07-15T09:00:00',
        description: 'Join us for a beach cleanup...',
        eventType: 'Environmental'
    },
    {
        id: 2,
        name: 'Food Drive',
        skillsNeeded: ['Communication', 'Organizational Skills'],
        location: 'Community Center, Downtown',
        dateTime: '2024-06-10T10:00:00',
        description: 'Assist in collecting and distributing...',
        eventType: 'Social'
    }
];

const users = [
    {
        id: 1,
        name: 'John Doe',
        skills: ['Teamwork', 'Organization'],
        availability: ['2024-07-15'],
        preferences: ['Environmental'],
        preferredLocation: 'California'
    },
    {
        id: 2,
        name: 'Jane Smith',
        skills: ['Communication', 'Organizational Skills'],
        availability: ['2024-06-10'],
        preferences: ['Social'],
        preferredLocation: 'Downtown'
    }
];

// Endpoint to check if a user matches an event
app.post('/check-match', (req, res) => {
    const { userId, eventId } = req.body;

    // Find the event and user
    const event = events.find(e => e.id === eventId);
    const user = users.find(u => u.id === userId);

    if (!event) {
        return res.status(404).json({ message: 'Event not found' });
    }
    if (!user) {
        return res.status(404).json({ message: 'User not found' });
    }

    // Matching logic
    const skillsMatch = event.skillsNeeded.every(skill => user.skills.includes(skill));
    const availabilityMatch = user.availability.includes(event.dateTime.split('T')[0]);
    const preferencesMatch = user.preferences.includes(event.eventType);
    const locationMatch = user.preferredLocation === event.location.split(',')[0];

    if (skillsMatch && availabilityMatch && preferencesMatch && locationMatch) {
        res.json({ match: true, message: 'You match this event!' });
    } else {
        res.json({ match: false, message: 'You do not match this event.' });
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
