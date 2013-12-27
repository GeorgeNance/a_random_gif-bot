import praw
import re
import time
from datetime import datetime
from random import choice


already_done = set()
user_name='A_random_gif'
pw='not4u'
gifs=[]
hotphrases=[
    'random gif ',
    'random gif.',
    'random .gifs',
    'random gifs',
    'random .gif',
    'random.gif',
    'random_gif',
    'a_random_gif'

    ]

gifsdone=[]

banned=[
    "leagueoflegends"
]

print( "[bot] setting up connection with Reddit")

r = praw.Reddit(user_agent='A_random_gif bot')
r.login(user_name, pw)
print('logged in')

def getgif():
    r_gifs = r.get_subreddit('gifs')
    for x in r_gifs.get_new(limit=None):
        if str(x.url).startswith('http://i.') and x.id not in gifsdone:
            
            gifs.append(x)
    chosen_gif=choice(gifs)
    gifs.remove(chosen_gif)
    gifsdone.append(chosen_gif.id)
    return chosen_gif


sub=r.get_subreddit('all')

def message(count):
    gifreply=""
    phrase=''
    for i in range(count):
        if count == 1:
            phrase='[Here is a random gif!'
        else:
            phrase="[randomgif["+str(i+1)+']'

        randomgif=getgif()
        if randomgif.over_18==True:
            gifreply+=phrase+'(NSFW)]'+'('+randomgif.url+')|Support the OP [here]('+randomgif.permalink+')\n\n'
        else:
            gifreply+=phrase+']'+'('+randomgif.url+')|Support the OP [here]('+randomgif.permalink+')\n\n'
    reply=gifreply\
          +'Gifs are chosen at random from /r/gifs'\
          +'\n\n _____ \n\n I am still in development!'\
          +'\n\n Find out about me [here](http://www.reddit.com/r/botwatch/comments/1sewvk/im_a_random_gif_a_bot_dedicated_to_giving_you_a/)'
    return reply


def parse_comment(comment):
    find=re.findall('=[1-9]?[0-9]',comment)
    if find !=[]:
        str=(find[0])
        count=int(str[1:3])
        if count > 10:
            count=10
    else:
        count=1
    return count



def reply_to(comment,count):
    msg=message(count)
    try:
        comment.reply(msg)
        print(gifsdone)
        print('commented---'+datetime.now().strftime('%H:%M:%S'))
        comment.upvote()
        print('upvoted')
        already_done.add(comment.id)
    except sub.RATELIMIT:
        print('Comment Failed')
        pass

print('Searching')
while True:

    for comment in sub.get_comments(limit=None):
        if str(comment.author)!=user_name and comment.subreddit not in banned and comment.id not in already_done:
                 if 'randomgif=' in str(comment.body).lower():
                    print(comment.body+'--'+str(comment.author))
                    number=parse_comment(str(comment.body))
                    reply_to(comment,number)


                 else:
                     for phrase in  hotphrases:
                         if phrase in str(comment.body):
                             print(comment.body+'--'+str(comment.author))
                             reply_to(comment,1)



                
                

    #print('sleeping -- '+datetime.now().strftime('%H:%M:%S'))
    time.sleep(5)

