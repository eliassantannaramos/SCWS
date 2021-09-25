
import Scrapper

#DataSet
import pandas as pd

user="esr-music8"
user_followers = Scrapper.get_user_followers(user)
print(user_followers)