
import scrapper

# DataSet
import pandas as pd

user = "esr-music8"

user_followers = scrapper.get_user_followers(user)

user_tracks = scrapper.get_user_track_list(user)

db_track_likes = db_track_repost = db_track_comments = {}
for track in user_tracks:  # Get all user the likes all your tracks
    db_track_likes[track] = scrapper.get_user_track_likes(track)
    db_track_repost[track] = scrapper.get_track_repost(track)
    db_track_comments[track] = scrapper.get_track_comments(track)

pd.DataFrame(list(user_tracks.items()),
             columns=["Link", "track_name"]).to_csv("user_tracks.csv", index=False)
pd.DataFrame(list(user_followers.items()),
             columns=["Follower_Link", "Follower"]).to_csv("user_followers.csv", index=False)
pd.DataFrame(db_track_likes).to_csv("db_track_likes.csv", index=True)
pd.DataFrame(db_track_repost).to_csv("db_track_repost.csv", index=True)
pd.DataFrame(db_track_comments).to_csv("db_track_comments.csv", index=True)
