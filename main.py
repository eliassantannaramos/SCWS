
import scrapper


# DataSet

user = "esr-music8"

user_followers = scrapper.get_user_followers(user)

user_tracks = scrapper.get_user_track_list(user)


print(user_tracks)
