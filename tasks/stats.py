from locust import task, SequentialTaskSet

from common.logger import Logger, LogType
from common.utils import Utils

""" Tasks for Stats """


class Stats(SequentialTaskSet):

    def on_start(self):
        self.username = self.user.get_username()
        self.token = self.user.get_token()
        self.headers = Utils.get_headers_with_token(self.token)

    @task
    def get_stats(self):
        with self.client.get(url="/api/getstat", headers=self.headers, catch_response=True, name="Get Stats") as response:
            if response.status_code != 200:
                failure_info = f"Test stats receiving failed by user: {self.username}. Response: {response.text}. Status code: {response.status_code}."
                response.failure(failure_info)
                Logger.log_message(failure_info, LogType.ERROR)
                print(failure_info)
            else:
                success_info = f"Test stats successfully received by user: {self.username}"
                response.success()
                Logger.log_message(success_info, LogType.INFO)
                print(success_info)

    @task
    def exit_task_execution(self):
        self.interrupt()