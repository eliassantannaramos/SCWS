"""
Model classes will be a memory representation of soundcloud API schemas
"""

from lib import API_URLS
from lib.api_connector import ApiConnector


class BaseModel:
    """
    Base model class
    """

    def __init__(self, **kwargs):
        """
        Load all raw data into a dictionary
        :param kwargs: raw data from cache or api response
        """
        self.base_dict = kwargs

    def __getattr__(self, item):
        """
        Adds capability to fetch data from base_dict as a properties

        Ex: base_dict = {'key1: 'value1', 'key2: 'value2'}
            self.key1 -> 'value1'
        :param item: key to fetch from base_dict
        :return: Value from base_dict
        """
        return self.base_dict[item]

    @staticmethod
    def get_collection(model, url):
        """
        Gets a collection from API and yields correspondents instances
        :param model: Model class to instantiate
        :param url: api endpoint
        :return: A generator with instances of the given class
        """
        data_list = ApiConnector.get_collection(url)

        for row in data_list:
            if 'self' in row.keys():
                row['safe_self'] = row.pop('self')

            yield model(**row)


class User(BaseModel):
    """
    User model class
    """

    resolve_url = "{resolve}?url=https://soundcloud.com/{username}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_tracks_url = API_URLS["user_tracks"].format(user_id=self.id)
        self.followers_url = API_URLS["user_followers"].format(user_id=self.id)
        self.followings_url = API_URLS["user_followings"].format(user_id=self.id)

    def __str__(self):
        return self.username

    @property
    def tracks(self):
        """
        :return: A generator with user's Track instances
        """
        return User.get_collection(Track, self.user_tracks_url)

    @property
    def followers(self):
        """
        :return: A generator with user's Track instances
        """
        return User.get_collection(User, self.followers_url)

    @property
    def followings(self):
        """
        :return: A generator with user's followings instances
        """
        return User.get_collection(User, self.followings_url)

    @classmethod
    def find_user(cls, username):
        """
        Fetches user data and instantiate a User class
        :param username: Soundcloud user name
        :return: A User instances
        """
        url = User.resolve_url.format(resolve=API_URLS['resolve'], username=username)
        user_dict = ApiConnector.get_json(url)

        return cls(**user_dict)


class Track(BaseModel):
    """
    Track model class
    """

    track_url = API_URLS["track"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.track_comments_url = API_URLS["track_comments"].format(track_id=self.id)
        self.track_reposters_url = API_URLS["track_reposters"].format(track_id=self.id)

    def __str__(self):
        return self.title

    @classmethod
    def get_from_api(cls, track_id):
        """
        Fetches track data and instantiate a Track class
        :param track_id: Soundcloud track id
        :return: A track instance
        """
        track_dict = ApiConnector.get_json(Track.track_url.format(track_id=track_id))
        return cls(**track_dict)

    @property
    def comments(self):
        """
        :return: A generator with track's comment instances
        """
        return Track.get_collection(Comment, self.track_comments_url)

    @property
    def reposters(self):
        """
        :return: A generator with track's reposters instances
        """
        return Track.get_collection(User, self.track_reposters_url)


class Comment(BaseModel):
    """
    Comment model class
    """
    def __str__(self):
        return self.body
