# Filename: proto.py
# Author: Dharmesh Tarapore <dharmesh@bu.edu>
# Description: Mucking about.
import praw
import secrets

REDDIT_USERNAME = secrets.REDDIT_USERNAME
REDDIT_PASSWORD = secrets.REDDIT_PASSWORD

DEBUG = False

if DEBUG:
    NUMBER_OF_POSTS = 5
else:
    NUMBER_OF_POSTS = 25

reddit = praw.Reddit(client_id='9KimOyjWFOM8ag',
                     client_secret='q11CnnYVwTJ7P927XKYJHJi_Rvg',
                     password=REDDIT_PASSWORD,
                     user_agent='testscript by /u/' + REDDIT_USERNAME,
                     username=REDDIT_USERNAME)

# Get a reference to the roastme subreddit
roastme = reddit.subreddit('roastme')

# Get a list of the top posts of all time
# Work our way down
# For each post, store the image followed by the top 10 roasts and comments
# in a tuple 
for submission in roastme.top(limit=NUMBER_OF_POSTS):
    title = submission.title
    if not title.startswith("[META]"):
        print(submission.title)
    else:
        continue