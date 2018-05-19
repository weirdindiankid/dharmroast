# Filename: proto.py
# Author: Dharmesh Tarapore <dharmesh@bu.edu>
# Description: Mucking about.
import praw
import secrets as secrets
from imagedownloader import *

REDDIT_USERNAME = secrets.REDDIT_USERNAME
REDDIT_PASSWORD = secrets.REDDIT_PASSWORD
IMAGE_DIR = 'images/'

image_downloader = ImageDownloader()

DEBUG = True
NUMBER_OF_COMMENTS = 5

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
    if not title.startswith("[META]") and (submission.link_flair_text != 'Meta'):
        try:
            # Download the image
            image_file_name = image_downloader.visit_url(submission.url, 0)
            # Retrieve top comments for this post (presumably, these are roasts)
            # TODO: Down the line, use NLP to figure out if these are actually insults
            # TODO: Also figure out if the retrieved images contain faces of humans/potatoes.
            print(submission.title)
        except Exception as e:
            # TODO: Write this to a log file.
            with open("error.log", "a+") as error_log_file:
                error_log_file.write("Exception occurred: " + e + "\n")
                error_log_file.close()
    else:
        continue