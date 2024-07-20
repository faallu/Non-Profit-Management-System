document.addEventListener('DOMContentLoaded', function () {
    const signUpForm = document.querySelector('signUpForm');
    const signInForm = document.querySelector('signIForm');
    const loginButton = document.getElementById('login');
    const registerButton = document.getElementById('register');
    const container = document.getElementById('container');

    // Toggle between sign-up and sign-in forms
    loginButton.addEventListener('click', () => {
        container.classList.remove('sign-up-mode');
    });

    registerButton.addEventListener('click', () => {
        container.classList.add('sign-up-mode');
    });

    // Handle sign-up form submission
    signUpForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        
        const formData = new FormData(this);
        const name = formData.get('name');
        const email = formData.get('email');
        const password = formData.get('password');
        
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: email,
                password: password
            })
        });

        const result = await response.json();
        if (response.ok) {
            alert('Registration successful!');
            //redirect to profile page to continue updating personal information
        } else {
            alert(result.message);
        }
    });

    // Handle sign-in form submission
    signInForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        
        const formData = new FormData(this);
        const email = formData.get('email');
        const password = formData.get('password');
        

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: email,
                password: password
            })
        });

        const result = await response.json();
        if (response.ok) {
            localStorage.setItem('token', result.token);
            alert('Login successful!');
            //redirect to landing page
        } else {
            alert(result.message);
        }
    });
});
