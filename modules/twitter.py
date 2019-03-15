import sys
import json

from modules import twittertweets, twitterprofile, twittersearch


# file which is support modify that
def profilesender(handler):
    tempobj = twitterprofile.Profileclass(db=db, collection=collection1,
                                          host=host, port=port)
    profiledict = {}
    profiledict["name"] = handler
    data = tempobj.profilefetcher(name=handler)
    if data == None:
        profiledict["status"] = False
    else:
        profiledict["status"] = True
    profiledict["profile"] = [data]
    return (json.dumps(profiledict, ensure_ascii=False))


def profilefriends(handler, limit):
    tempobj = twitterprofile.Profileclass(db=db, collection=collection1,
                                          host=host, port=port)
    profiledict = {}
    profiledict["name"] = handler
    profiledict["profiles"] = tempobj.friendsprofile(name=handler, limit=int(limit))
    return (json.dumps(profiledict))

def profiletweets(handler, limit):
    tempobj = twittertweets.TweitterClass(db=db, collection=collection2,
                                          host=host, port=port)
    profiledict = {}
    profiledict["name"] = handler
    profiledict["posts"] = tempobj.profiletweets(handler=handler, limit=int(limit))

    return (json.dumps(profiledict))

def tweetsofHandler(handler, limit):
    tempobj = twittertweets.TweitterClass(db=db, collection=collection2,
                                          host=host, port=port)
    tweetsdata = {}
    tweetsdata["handler"] = handler
    tweetsdata["posts"] = tempobj.handlertweets(inputdata=handler, limit=int(limit))
    return (json.dumps(tweetsdata))

def tweetsofHashtags(hashtags, limit):
    tempobj = twittertweets.TweitterClass(db=db, collection=collection2,
                                          host=host, port=port)
    tweetsdata = {}
    tweetsdata["hashtags"] = "#"+hashtags
    tweetsdata["posts"] = tempobj.hashtags(inputdata=hashtags, limit=int(limit))

    return (json.dumps(tweetsdata))

def person_search_twitter(name, limit):

    tempobj = twittersearch.TweitterClass(db=db, collection=collection2,
                                          host=host, port=port)
    profile = {}
    profile["search-type"] = name
    profile["profiles"] = tempobj.profilesearch(inputdata=name, limit=int(limit))
    return (json.dumps(profile))

def main(*kwargs):
    data = 0
    try:
        print(kwargs)
        if(len(kwargs)<4):
            raise Exception
        elif ("special" in kwargs):
            if "tweets" in kwargs:
                data = profiletweets(handler=kwargs[0], limit=(kwargs[1]))
            elif "friends" in kwargs:
                data = profilefriends(kwargs[0], limit=(kwargs[1]))
            elif "profile" in kwargs:
                data = profilesender(kwargs[0])

        elif("general" in kwargs):
            print("///")
            if "hashtags" in kwargs:
                data = tweetsofHashtags(kwargs[0], kwargs[1])
            elif "handler" in kwargs:
                data = tweetsofHandler(kwargs[0], kwargs[1])
            elif "search" in kwargs:
                data = person_search_twitter(kwargs[0], kwargs[1])
        else:
            raise Exception

    except Exception:
        print("error>>main::",sys.exc_info()[1])

    finally:
        return (data)



if __name__ == '__main__':
    #main(None)
    #pass
    # print(main("freefood", 5, "hashtags", "general"))
    # main("stevewoz", 5, "handler", "general")
    # main("stevewoz", 10, "tweets")
    # main("elonmusk", "friends")
    print(main("elonmusk", "special", "profile" , 1))
