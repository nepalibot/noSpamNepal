import praw
from datetime import datetime, timedelta
import time
import os

# Authenticate using praw.ini file


def authenticate():
    print('Authenticating...')
    reddit = praw.Reddit('noSpamNepal')
    print('Authenticated as:  {}\n'.format(reddit.user.me()))
    return reddit


def main():
    reddit = authenticate()
    commented_posts = get_saved_data()
    while True:
        run_bot(reddit, commented_posts)


def run_bot(reddit, commented_posts):
    # The name of the subreddit in which to run the code
    sub = reddit.subreddit('Nepal')
    print('Scanning sub: ' + str(sub).upper())

    # We store commented posts' id in a text file so that we don't comment
    # in the same post twice
    def write_to_file(submission_id):
        with open('commented_posts.txt', 'a') as id:
            id.write(submission_id + '\n')

    # The bot identification text which goes to every comment it makes
    bot_text = ('\r '
                'Commenters be careful: MAYBE SPAM.\r'
                '***\r'
                'I am a bot made to keep /r/Nepal '
                'free from spams. '
                'Suggestions for improvements [*here.*]'
                '(https://www.reddit.com/message/compose/?to=noSpamNepal)\r'
                '***')
    # Scan 5 new posts, limit can be increased or decreased
    for submission in sub.new(limit=5):
        submitter = submission.author
        post_count = 0
        comment_count = 0
        bakchodi_post_count = 0
        bakchodi_comment_count = 0

        # Get the Reddit age of submitter in days
        submitter_created = submitter.created_utc
        age = time.time() - submitter_created
        d = timedelta(seconds=age)

        # It is because I could not pass submission.id as an argument to
        # .append method
        submission_id = submission.id
        commented_text = ("\t\t Commented on {}'s post"
                        '.\n'.format(submission.author))
        print('\nSubmitted by: ' + str(submitter))

        # Get all the comments of the submitter from all subreddits
        # sorting from new to old
        comments_all = list(submitter.comments.new(limit=None))
        for each_comment in comments_all[:]:
            # Find when the comment was created
            comment_created = each_comment.created_utc
            comment_age = time.time() - comment_created
            comment_age_days = timedelta(seconds=comment_age)

            # count all the comments in the subreddit defined in 'sub'
            if each_comment.subreddit == str(sub):
                comment_count += 1
            if (each_comment.subreddit == 'bakchodi' and
                comment_age_days.days < 30):
                bakchodi_comment_count += 1

        # Getting all the posts here, similar to comments
        posts_all = list(submitter.submissions.new(limit=None))
        for each_post in posts_all[:]:
            if each_post.subreddit == str(sub):
                post_count += 1

        # Print to the screen total posts and comments of the submitter
        # in the subreddit defined in 'sub'
        print('Total posts: ' + str(post_count))
        print('Total comments: ' + str(comment_count))

        # First check if the user is spamming from bakchodi
        # If he has more than 10 comments there in the last 30 days,
        # reply this message
        if (bakchodi_comment_count > 10 and
            submission_id not in commented_posts):
            submission.reply('This submitter has **' + str(bakchodi_comment_count)
                + ' comments** in /r/bakchodi in the last 30 days.' + bot_text)
            commented_posts.append(submission_id)
            write_to_file(submission_id)
            print(commented_text)

        # Check if the user is less than 30 days old and his first post here
        if (d.days < 30 and
            submission.author != reddit.user.me() and
            post_count == 1 and
            comment_count < 10 and
            submission.id not in commented_posts):
                submission.reply('Your account is **' + str(d.days) + ' days** \
                    old and this is your **first** post here. \
                    We encourage you to participate in \
                    discussion and not to post spams. ' + bot_text)
                commented_posts.append(submission_id)
                write_to_file(submission_id)
                print(commented_text)

        # Check if the user has more posts in the sub than comments
        if (comment_count < post_count and
            submission.id not in commented_posts and
            submission.author != reddit.user.me()):
                submission.reply('You have only **' + str(comment_count) + ' \
                    comments** but **' + str(post_count) + ' posts** in this\
                    subreddit. Engage in **conversations!** ' + bot_text)
                commented_posts.append(submission_id)
                write_to_file(submission_id)
                print(commented_text)

        # No need to import datetime if not used here
        # Uncomment to print Reddit accout creation date and age of submitter
        # print('Account created: '+str(datetime.fromtimestamp(submitter_age)))
        # print('Account age: ' + str(d.days) + ' days\n')

    # Bot runs once in a minute and scans 5 new posts.
    # Should be enough for 'Nepal' subreddit
    print('\t\t\t Sleeping for 1 minute.... \n')
    time.sleep(60)

# Save already commented posts' id in a text file and check if the post is
# already scanned. If yes, nothing is commented and no check is performed.


def get_saved_data():
    if not os.path.isfile('commented_posts.txt'):
        commented_posts = []
    else:
        with open('commented_posts.txt', 'r') as id:
            commented_posts = id.read()
            commented_posts = commented_posts.split('\n')
    return commented_posts


if __name__ == '__main__':
    main()
