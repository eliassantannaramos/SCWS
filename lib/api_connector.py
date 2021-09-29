from lib import PARAMETERS
import requests


class ApiConnector:

    base_url = PARAMETERS["URLS"]["base"]

    @staticmethod
    def get_json(endpoint):
        headers = {"Authorization": PARAMETERS['OAuth_token']}
        params = {"client_id": PARAMETERS["client_id"]}
        get = requests.get(ApiConnector.base_url + endpoint, headers=headers, params=params)

        if get.status_code == 200:
            return get.json()

        raise ValueError("Error calling API. [%s]" % get.status_code)

    @staticmethod
    def get_collection(endpoint):
        data = ApiConnector.get_json(endpoint)
        return data["collection"]
