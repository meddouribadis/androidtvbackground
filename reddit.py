import os
import praw
import time
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
REDDIT_SUBREDDIT = os.getenv('REDDIT_SUBREDDIT')
REDDIT_REDIRECT_URI = os.getenv('REDDIT_REDIRECT_URI')
DIRECTORY = 'plex_backgrounds'

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    password=REDDIT_PASSWORD,
    user_agent="testscript by u/{}".format(REDDIT_USERNAME),
    username=REDDIT_USERNAME,
    redirect_uri=REDDIT_REDIRECT_URI,
)
print(reddit.user.me())
print(f'REDDIT_SUBREDDIT: {REDDIT_SUBREDDIT}')

subreddit = reddit.subreddit(REDDIT_SUBREDDIT)

# iterate over files in
# that directory
for filename in os.listdir(DIRECTORY):
    f = os.path.join(DIRECTORY, filename)
    # checking if it is a file
    if os.path.isfile(f):
        title = Path(f).stem
        image = f
        print (title)
        for submission in subreddit.search(title, sort='relevance', time_filter='all'):
            print(submission.title, submission.id)
            submission.delete()
        print(f'Uploading: {title}')
        subreddit.submit_image(title, image)
        time.sleep(2)