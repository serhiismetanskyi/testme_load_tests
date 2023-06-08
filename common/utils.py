import re

""" Utils for Tests """


class Utils:

    @staticmethod
    def get_base_headers():
        base_headers = {
            "Content-type": "application/json",
            "Connection": "keep-alive"
        }
        return base_headers

    @staticmethod
    def get_token_value(headers):
        token_value = r'csrftoken=([a-zA-Z0-9]+);'
        token_search = re.search(token_value, str(headers))
        if token_search:
            token = token_search.group(1)
            return token
        else:
            error = "Token not found"
            return error

    @staticmethod
    def get_headers_with_token(token):
        headers = Utils.get_base_headers()
        headers['X-CSRFToken'] = token
        return headers

