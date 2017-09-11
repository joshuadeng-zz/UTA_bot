import praw
import time
import os

REPLY_MESSAGE = "Friendly reminder: 'UTA' refers to UT Arlington. UT Austin is simply 'UT'.\n\nIf you actually meant UT Arlington then ignore this post."


def authenticate():
    print("authenticating")
    login_info=retrieve_credentials()
    reddit=praw.Reddit(username=login_info[0],
			password=login_info[1],
			client_id=login_info[2],
			client_secret=login_info[3], 
            user_agent="A bot to remind people that UTA is UT Arlington v0.1")
    print("authenticated as {}".format(reddit.user.me()))
    return reddit


def run_bot(reddit, replied):
    print("getting submissions")
    for submission in reddit.subreddit('UTAustin').new(limit=5):
        if (" uta" in submission.title or " uta" in submission.selftext 
            or " UTA" in submission.title or " UTA" in submission.selftext) and submission.id not in replied:

            print("string with 'UTA' found in " + submission.id)
            submission.reply(REPLY_MESSAGE)
            print("replied to submission " + submission.id)

            replied.add(submission.id)
            with open("replied.txt", "a") as i:
                i.write(submission.id + "\n")

    print("sleeping for 30 seconds")
    # sleep for 30 seconds
    time.sleep(30)


def get_replied():
    if not os.path.isfile("replied.txt"):
        replied = set()
    else:
        replied = set(open("replied.txt").read().split("\n"))
        replied = set(filter(None, replied))
    return replied


def retrieve_credentials():
    login_info = [os.environ['REDDIT_USERNAME'], os.environ['REDDIT_PASSWORD'], 
    os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"]]
    return login_info


def main():
    replied = get_replied()
    reddit = authenticate()
    while True:
        run_bot(reddit, replied)


# main method
if __name__ == "__main__":
    main()
