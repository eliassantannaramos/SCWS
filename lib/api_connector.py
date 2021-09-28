from lib import PARAMETERS
import requests


class ApiConnector:

    @classmethod
    def get_json(cls, endpoint):
        headers = {"Authorization": PARAMETERS['OAuth_token']}
        get = requests.get(endpoint, headers=headers)

        if get.status_code == 200:
            return get.json()

        raise ValueError("Error calling API. [%s]" % get.status_code)