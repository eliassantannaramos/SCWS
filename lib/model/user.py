from lib import PARAMETERS
from lib.api_connector import ApiConnector


class User:

    resolve_url = "{resolve}?url=https://soundcloud.com/{username}"

    def __init__(self, user_id, **kwargs):

        self.user_id = user_id
        self.user_dict = kwargs

    @property
    def name(self):
        return self.user_dict['username']

    @property
    def followers_count(self):
        return self.user_dict['followers_count']

    @property
    def followings_count(self):
        return self.user_dict['followings_count']

    @classmethod
    def find_user(cls, username):
        url = User.resolve_url.format(resolve=PARAMETERS['URLS']['resolve'], username=username)
        user_dict = ApiConnector.get_json(url)

        return cls(user_dict['id'], **user_dict)
