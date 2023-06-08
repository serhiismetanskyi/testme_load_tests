from locust import events

from common.logger import Logger
from common.users_loader import UsersLoader
from tasks.lists import Lists
from tasks.stats import Stats
from tasks.tests import Tests
from users.register_user import RegisteredHttpUser

""" Test Runner """


@events.test_start.add_listener
def on_test_start(**kwargs):
    if kwargs['environment'].parsed_options.logfile:
        Logger.init_logger(__name__, kwargs['environment'].parsed_options.logfile)
    UsersLoader.load_users()
    Logger.log_message("......... Initiating Load Test .......")


@events.test_stop.add_listener
def on_test_stop(**kwargs):
    Logger.log_message("........ Load Test Completed ........")


class TestsGroup(RegisteredHttpUser):
    weight = 4
    RegisteredHttpUser.tasks = [Tests]


class ListsGroup(RegisteredHttpUser):
    weight = 2
    RegisteredHttpUser.tasks = [Lists]


class StatsGroup(RegisteredHttpUser):
    weight = 1
    RegisteredHttpUser.tasks = [Stats]

