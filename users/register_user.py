from locust import between

from common.logger import Logger, LogType
from common.users_loader import UsersLoader
from common.utils import Utils
from users.abstract_user import AbstractUser


class RegisteredHttpUser(AbstractUser):
    wait_time = between(1, 2)
    abstract = True

    username = ""

    @classmethod
    def verify_login(cls, response, username):
        if response.status_code != 200:
            failure_info = f"Login failed for user: {username}. Response: {response.text}. Status code: {response.status_code}."
            response.failure(failure_info)
            Logger.log_message(failure_info, LogType.ERROR)
            print(failure_info)
        return True

    @classmethod
    def verify_logout(cls, response, username):
        if response.status_code != 200:
            failure_info = f"Logout failed for user: {username}. Response: {response.text}. Status code: {response.status_code}."
            response.failure(failure_info)
            Logger.log_message(failure_info, LogType.ERROR)
            print(failure_info)
        return True

    def on_start(self):
        user = UsersLoader.get_user()
        headers = Utils.get_base_headers()
        username = user["username"]
        self.username = username

        with self.client.post(url="/api/auth/login", json=user, headers=headers, catch_response=True, name="Login") as response:
            if self.verify_login(response, self.username):
                success_info = f"Login successfully for user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                print(success_info)
                super().set_username(self.username)
                headers = response.headers
                token = Utils.get_token_value(headers)
                super().set_token(token)


    def on_stop(self):
        with self.client.get(url="/api/auth/logout", catch_response=True, name="Logout") as response:
            if self.verify_logout(response, self.username):
                success_info = f"Logout successfully for user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                print(success_info)
                super().clear_user_data()