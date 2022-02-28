from lib.model import User


def check_engagement(username):

    s_user = User.find_user(username)
    for row in s_user.tracks:
        print(row)
        for r in row.reposters:
            print(r)
    # user_followers = s_user.followers
    # user_tracks = s_user.tracks


if __name__ == "__main__":
    check_engagement('esr-music8')
    # user = User.find_user('esr-music8')
    # print("Username: %s" % user)
    #
    # print("Printing track list...")
    # for track in user.tracks:
    #     print(track)
    #
    #     for comment in track.comments:
    #         print(comment)


