from lib.model.user import User
import json


if __name__ == "__main__":
    user = User.find_user('esr-music8')

    print(json.dumps(user.__dict__, indent=4))
