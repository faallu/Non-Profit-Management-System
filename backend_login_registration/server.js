const http = require("http");
const express = require('express');

const app = express();
const fs = require('fs');
const path = require('path');

const hostname = '127.0.0.1';  
const port = 3000;

app.use(express.static(path.join(__dirname, 'backend_login_registration')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname,'login.html'));
  });


app.post('/register', async (req, res) => {
    try {
        const { username, password } = req.body;

        // Check if user already exists
        if (users.some(user => user.username === username)) {
            return res.status(400).json({ message: 'User already exists' });
        }

        const hashedPassword = await bcrypt.hash(password, 10);

        users.push({ username, password: hashedPassword });

        res.status(201).json({ message: 'User registered successfully' });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

app.post('/login', async (req, res) => {
    try {
        const { username, password } = req.body;

        // Find user in the database
        const user = users.find(user => user.username === username);

        if (!user) {
            return res.status(404).json({ message: 'User not found' });
        }

        if (!await bcrypt.compare(password, user.password)) {
            return res.status(401).json({ message: 'Invalid credentials' });
        }

        const token = jwt.sign({ username }, 'randomkey123'); // Replace 'secret_key' with a secure random key
        res.json({ token });
    } catch (error) {
        res.status(500).json({ message: 'Server error' });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
  });