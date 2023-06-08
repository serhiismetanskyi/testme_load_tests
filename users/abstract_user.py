from locust import HttpUser


class AbstractUser(HttpUser):
    abstract = True

    def __init__(self, parent):
        super(AbstractUser, self).__init__(parent)
        self.user_data = {}

    def set_username(self, username):
        self.user_data["username"] = username

    def get_username(self):
        if "username" in self.user_data.keys():
            return self.user_data["username"]
        else:
            return None

    def set_token(self, token):
        self.user_data["token"] = token

    def get_token(self):
        return self.user_data["token"]

    def clear_user_data(self):
        self.user_data.clear()
