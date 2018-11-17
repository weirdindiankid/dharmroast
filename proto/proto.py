# Filename: proto.py
# Author: Dharmesh Tarapore <dharmesh@bu.edu>
# Description: Mucking about.
import praw
import secrets as secrets
from imagedownloader import *
import mysql.connector

mydb = mysql.connector.connect(user=secrets.MYSQL_USERNAME, passwd=secrets.MYSQL_PASSWORD,
    database=secrets.MYSQL_DATABASE, host=secrets.MYSQL_HOST)

mycursor = mydb.cursor()

REDDIT_USERNAME = secrets.REDDIT_USERNAME
REDDIT_PASSWORD = secrets.REDDIT_PASSWORD
IMAGE_DIR = 'images/'

image_downloader = ImageDownloader()

DEBUG = False
NUMBER_OF_COMMENTS = 5

if DEBUG:
    NUMBER_OF_POSTS = 5
else:
    NUMBER_OF_POSTS = 250

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
            comments = submission.comments
            comments_list = []
            for comment in comments[:6]:
                comments_list.append(comment.body)

            print(comments_list[5])
            #mydb.cursor().execute("INSERT INTO roasts (image_link, post_title, c1, c2, c3, c4, c5, c6) VALUES(\"a\", \"b\", \"c\", \"d\", \"e\", \"f\", \"g\", \"h\") ")
            sql = "INSERT INTO roasts (image_link, post_title, c1, c2, c3, c4, c5, c6) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            vals = (image_file_name, title, comments_list[0], comments_list[1], comments_list[2],
                comments_list[3], comments_list[4], comments_list[5])
            # rc = mydb.cursor()
            # rc.execute(sql, values)
            # rc.commit()
            mycursor.execute(sql, vals)
            mydb.commit()
        except Exception as e:
            # TODO: Write this to a log file.
            with open("error.log", "a+") as error_log_file:
                error_log_file.write("Exception occurred: " + str(e) + "\n")
                error_log_file.close()
    else:
        continue