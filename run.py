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
    'random.gif',
    'randomgif',
    'random_gif',
    'a_random_gif'

    ]

gifsdone=[]

    

print( "[bot] setting up connection with Reddit")

r = praw.Reddit(user_agent='A_random_gif bot')
r.login(user_name, pw)
print('logged in')

def getgif():
    r_gifs = r.get_subreddit('gifs+gif+Updownvotegifs+captiongifs+Dancinggifs+reactiongifs')
    for x in r_gifs.get_new(limit=200):
        if str(x.url).startswith('http://i.') and x.id not in gifsdone:
            
            gifs.append(x)
    chosen_gif=choice(gifs)
    gifs.remove(chosen_gif)
    gifsdone.append(chosen_gif.id)
    return chosen_gif


sub=r.get_subreddit('all')



while True:
    print('Searching')
    for comment in sub.get_comments(limit=None):
        for phrase in hotphrases:
            if phrase in str(comment.body).lower() and comment.id not in already_done and str(comment.author)!=user_name:
                    print(comment.body+'--'+str(comment.author))
                    randomgif=getgif()
                    try:
                        if randomgif.over_18==True:
                            comment.reply('[Here is a random gif!](NSFW)'+'('+randomgif.url+') \n\n This gif was chosen at random from /r/'+randomgif.subreddit+'\n\n Support the OP of this gif by clicking [here]('+randomgif.permalink+')\n\n _____ \n\n I am still in development!'+
                                      '\n\n Find out about me [here](http://www.reddit.com/r/botwatch/comments/1sewvk/im_a_random_gif_a_bot_dedicated_to_giving_you_a/)'
                                                                     )
                        else:
                            comment.reply('[Here is a random gif!]'+'('+randomgif.url+') \n\n This gif was chosen at random from /r/gifs'+randomgif.subreddit+'\n\n Support the OP of this gif by clicking [here]('+randomgif.permalink+')\n\n _____ \n\n I am still in development!'+
                                      '\n\n Find out about me [here](http://www.reddit.com/r/botwatch/comments/1sewvk/im_a_random_gif_a_bot_dedicated_to_giving_you_a/)'
                                                                     )
                        print(gifsdone)
                        print('commented--'+datetime.now().strftime('%H:%M:%S'))
                        comment.upvote()
                        print('upvoted')
                        already_done.add(comment.id)
                    except sub.RATELIMIT:
                        print('Comment Failed')
                        pass


                
                

    #print('sleeping -- '+datetime.now().strftime('%H:%M:%S'))
    time.sleep(5)

