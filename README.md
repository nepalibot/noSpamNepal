# noSpamNepal
A spam detecting bot for Nepal subreddit. The program is written using Python and PRAW.
Link to the bot [here.](https://www.reddit.com/user/noSpamNepal)

# Install PRAW
```
pip install praw
```
# How does it work?
Currently the bot posts a comment to a post if one of the following conditions are met:
* If the user has more than ten comments in a 'specified' sub within the last 30 days.
This was because users from the 'specified' sub posted a lot of spams in our sub.

* If the submitter account is less than 30 days old and is posting their first post here,
a slight warning not to spam and engage in discussions is commented.

* If the user has more posts than comments in our sub, their new post gets a reply suggesting them to participate in conversations.

**Note:** These above mentioned conditions are **mutually exclusive**. If one condition is evaluated true, response is given and the same post is not checked again.

#### I am willing to contribute, what do I do?
Ping the bot and the bot shall reply :).
