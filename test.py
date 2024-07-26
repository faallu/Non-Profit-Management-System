import unittest
import json
from app import app

class UserManagementTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data.decode(), "User Management Backend")

    def test_get_users(self):
        result = self.app.get('/getusers')
        self.assertEqual(result.status_code, 200)
        self.assertTrue(len(json.loads(result.data)) > 0)

    def valid_user_test(self):
        test_user = {
            "name": "Fallou Sarr",
            "username": "faallu",
            "age": 28,
            "email": "fgsarr@gmail.com",
            "phone": "555-123-4567",
            "password": "test123"
        }
        result = self.app.post('/register', json=new_user)
        self.assertEqual(result.status_code, 200)
        self.assertIn("User 'Fallou' Created Successfully", result.data.decode())

    def invalid_user_test(self): # Inputting wrong username, age, email, phone and password.
        invalid_user = {
            "name": "Jack",
            "username": "#jacque",
            "age": "twenty", 
            "email": "jacques.com", 
            "phone": "123456",  
            "password": "pwd"  
        }
        result = self.app.post('/register', json=invalid_user)
        self.assertEqual(result.status_code, 400)

    def test_authenticate(self):
        user_credentials = {
            "username": "johndoe",
            "password": "password123"
        }
        result = self.app.post('/authenticate', json=user_credentials)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Authorized", result.data.decode())

    def test_authenticate_invalid(self):
        invalid_credentials = {
            "username": "johndoe",
            "password": "wrongpassword"
        }
        result = self.app.post('/authenticate', json=invalid_credentials)
        self.assertEqual(result.status_code, 401)

    def test_update_user(self):
        update_data = {
            "name": "John Updated",
            "username": "johndoe",
            "age": 31,
            "email": "john_updated@example.com",
            "phone": "321-654-0987",
            "password": "newpassword123"
        }
        result = self.app.put('/updateuser', json=update_data)
        self.assertEqual(result.status_code, 200)
        self.assertIn("User Updated Successfully", result.data.decode())

    def test_delete_user(self):
        delete_data = {"username": "janesmith"}
        result = self.app.delete('/deleteuser', json=delete_data)
        self.assertEqual(result.status_code, 200)
        self.assertIn("User Deleted Successfully", result.data.decode())

if __name__ == '__main__':
    unittest.main()
