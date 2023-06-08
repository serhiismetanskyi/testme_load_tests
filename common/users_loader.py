import csv
import os

""" Users Loader from CSV """


class UsersLoader:
    users_list = []
    csv_file_path = os.getcwd() + "/data/users.csv"

    @staticmethod
    def load_users():
        users = csv.DictReader(open(UsersLoader.csv_file_path))
        for user in users:
            UsersLoader.users_list.append(user)

    @staticmethod
    def get_user():
        if len(UsersLoader.users_list) < 1:
            UsersLoader.load_users()
        user = UsersLoader.users_list.pop()
        return user