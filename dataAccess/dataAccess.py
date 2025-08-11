class UserRepository:
    
    def __init__(self):
        self.users = {
            "admin@example.com": {
                "password": "yavuz1234",
                "role": "admin",
                "name": "Admin User"
            },
            "yavuz@example.com": {
                "password": "yavuz1234",
                "role": "student",
                "name": "Yavuz"
            }
        }

    def get_user_by_email(self, email):
        return self.users.get(email)

    def validate_user_credentials(self, email, password):
        user = self.get_user_by_email(email)
        if user and user["password"] == password:
            return user
        return None