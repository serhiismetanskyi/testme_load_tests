import time

from locust import task, SequentialTaskSet

from common.logger import Logger, LogType
from common.utils import Utils
from data.test_data import NewTest

""" Tasks for Tests """


class Tests(SequentialTaskSet):
    test_id = ""

    def on_start(self):
        self.username = self.user.get_username()
        self.token = self.user.get_token()
        self.headers = Utils.get_headers_with_token(self.token)

    @task
    def create_new_test(self):
        test = NewTest()
        test.set_test_name(f"API Test {int(time.time() * 1000)}")
        test.set_test_desc(f"Checking the creation of a new test by {self.username}. Endpoint: /api/tests/new")

        test_name = test.get_test_name()
        test_desc = test.get_test_desc()

        form_data = {"name": test_name, "description": test_desc}

        with self.client.post(url="/api/tests/new", json=form_data, headers=self.headers, catch_response=True, name="Create new Test") as response:
            if response.status_code != 201:
                failure_info = f"Test creation failed by user: {self.username}. Response: {response.text}. Status code: {response.status_code}."
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                print(failure_info)
            else:
                success_info = f"Test successfully created by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                print(success_info)
            response_json = response.json()
            self.test_id = response_json["test_id"]
            test.set_test_id(self.test_id)

    @task
    def get_test(self):
        with self.client.get(url=f"/api/tests/{self.test_id}", headers=self.headers, catch_response=True, name="Get Test Case by ID") as response:
            if response.status_code != 200:
                failure_info = f"Test receiving failed by user: {self.username}. Response: {response.text}. Status code: {response.status_code}."
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                print(failure_info)
            else:
                success_info = f"Test successfully received by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                print(success_info)

    @task
    def update_test(self):
        test_new_name = f"Updated API Test {int(time.time() * 1000)}"
        test_new_desc = f"Checking the update a test by {self.username}."

        form_data = {"name": test_new_name, "description": test_new_desc}

        with self.client.put(url=f"/api/tests/{self.test_id}", json=form_data, headers=self.headers, catch_response=True, name="Update Test Case by ID") as response:
            if response.status_code != 200:
                failure_info = f"Test changing failed by user: {self.username}. Response: {response.text}. Status code: {response.status_code}."
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                print(failure_info)
            else:
                success_info = f"Test successfully changed by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                print(success_info)

    @task
    def partial_update_test(self):
        test_new_desc = f"Checking the update a test description by {self.username}."

        form_data = {"description": test_new_desc}

        with self.client.patch(url=f"/api/tests/{self.test_id}", json=form_data, headers=self.headers, catch_response=True, name="Partial Update Test Case by ID") as response:
            if response.status_code != 200:
                failure_info = f"Test description changing failed by user: {self.username}. Response: {response.text}. Status code: {response.status_code}."
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                print(failure_info)
            else:
                success_info = f"Test description successfully changed by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                print(success_info)

    @task
    def run_test(self):
        form_data = {"status": "PASS"}

        with self.client.post(url=f"/api/tests/{self.test_id}/status", json=form_data, headers=self.headers, catch_response=True, name="Run Test") as response:
            if response.status_code != 200:
                failure_info = f"Test running failed by user: {self.username}. Response: {response.text}. Status code: {response.status_code}."
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                print(failure_info)
            else:
                success_info = f"Test successfully run by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                print(success_info)

    @task
    def delete_test(self):
        with self.client.delete(url=f"/api/tests/{self.test_id}", headers=self.headers, catch_response=True, name="Delete Test Case by ID") as response:
            if response.status_code != 200:
                failure_info = f"Test deleting failed by user: {self.username}. Response: {response.text}. Status code: {response.status_code}."
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                print(failure_info)
            else:
                success_info = f"Test successfully deleted by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                print(success_info)

    @task
    def exit_task_execution(self):
        self.interrupt()
