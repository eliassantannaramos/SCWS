from lib.model import User


if __name__ == "__main__":
    user = User.find_user('esr-music8')
    print("Username: %s" % user)

    print("Printing track list...")
    for track in user.tracks:
        print(track)

        for comment in track.comments:
            print(comment)


