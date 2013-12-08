import praw

import time
from datetime import datetime
from random import choice


already_done = set()

print('Loaded Datafile')
user_name=''
pw=''
gifs=[]
hotphrases=[
    'random gif',
    'random .gifs',
    'random gifs',
    'random .gif',
    'random.gif'
    ]

gifsdone=[]

    

print( "[bot] setting up connection with Reddit")

r = praw.Reddit(user_agent='A_random_gif bot')
r.login(user_name, pw)
print('logged in')

def getgif():
    r_gifs = r.get_subreddit('gifs')
    for x in r_gifs.get_new(limit=100):
        if str(x.url).startswith('http://i.') and x.id not in gifsdone:
            
            gifs.append(x)
    chosen_gif=choice(gifs)
    gifsdone.append(x.id)
    return chosen_gif


sub=r.get_subreddit('funny+gifs+pics+gaming+adviceanimals')



while True:
    print('Searching')
    for comment in sub.get_comments(limit=None):
        for phrase in hotphrases:
            if phrase in str(comment.body).lower() and comment.id not in already_done and str(comment.author)!=user_name:
                    print(comment.body+'--'+str(comment.author))
                    randomgif=getgif()
                    try:
                        comment.reply('[Here is a random Gif!]'+'('+randomgif.url+') \n\n This Gif was chosen at random from /r/gifs\n\n Support the OP of this Gif by clicking [here]('+randomgif.permalink+')\n\n _____ \n\n I am still in development!'
                                                                     ' If you dislike me, just let me know in PM.')

                        print('commented--'+datetime.now().strftime('%H:%M:%S'))
                        comment.upvote()
                        print('upvoted')
                        already_done.add(comment.id)
                    except sub.RATELIMIT:
                        print('Comment Failed')
                        pass


                
                

    print('sleeping -- '+datetime.now().strftime('%H:%M:%S'))
    time.sleep(15)

