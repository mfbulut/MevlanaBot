import praw
import time
import random
from mquotes import quotes


def login():
    print("Logging in...")
    # Fill here
    reddit = praw.Reddit(
        client_id="my client id",
        client_secret="my client secret",
        user_agent="my user agent",
        username="my username",
        password="my password",
    )
    print("Logged in!")

    return reddit


def reply(p_type):

    print("Related words found in " + p_type.id)

    random_index = random.randint(0, len(quotes) - 1)

    p_type.reply(
        "Ben bir botum ve paylaşımında 'Mevlana' geçtiği için geldim. Senin için bir tane **Mevlana sözü** paylaştım:"
        + "\n\n"
        + quotes[random_index]
        + " \n\n "
        "*-Mevlânâ Celâleddîn-i Rûmî* \n\n "
        "^(I am a bot and this action was performed automatically.)"
    )

    print("Replied to " + p_type.id)


def main(reddit):

    subreddit = reddit.subreddit(
        "Semazenler+Turkey+TurkeyJerky+KGBTR+ArsivUnutmaz+AteistTurk+BLKGM+Turkmenistan+Otuken+MuslumanTurk+Tiele"
    )

    print("Collecting  last 5 mentions,last 200 comments and last 20 posts from new...")

    time.sleep(1)
    for mention in reddit.inbox.mentions(limit=5):
        if mention.new and mention.author != reddit.user.me():
            mention.mark_read()
            time.sleep(1)
            reply(mention)

    for submission in subreddit.new(limit=20):
        submission_lower = submission.title.lower()
        if submission.score >= 0:
            if (
                "mevlana" in submission_lower
                and submission.saved is False
                and submission.author != reddit.user.me()
            ):
                time.sleep(1)
                reply(submission)
                submission.save()

    for comment in subreddit.comments(limit=200):
        comment_lower = comment.body.lower()
        if comment.score >= 8:

            if (
                "mevlana" in comment_lower
                and comment.saved is False
                and comment.author != reddit.user.me()
            ):
                time.sleep(1)
                reply(comment)
                comment.save()

    print("Collect Completed.")

    print("Sleeping for 300 seconds...")
    time.sleep(300)


reddit = login()


while True:
    try:
        main(reddit)
    except Exception as e:
        print(str(e) + " ,sleeping 120 seconds...")
        time.sleep(120)
