from sys import exc_info
from modules.sentiment import Sentiment_analysis
import tweepy
import time
from credentials import TwitterKeys


class TwitterClass:

    def __init__(self):

        self.neg_count = 0
        self.neu_count = 0
        self.pos_count = 0
        self.obj = Sentiment_analysis()
        cred = TwitterKeys()
        try:
            self.auth = tweepy.OAuthHandler(cred.consumer_key, cred.consumer_secret)
            self.auth.set_access_token(cred.access_token, cred.access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("error>>init::", exc_info()[1])

    def _jsonconvetor(self, tweets):

        tempdict = dict()
        # print(tweets)
        # tempdict["description"] = tweets.author.description
        tempdict["source"] = tweets.source
        # tempdict["followers"] = tweets.author.followers_count
        tempdict["author_location"] = tweets.author.location
        if not tempdict["author_location"]:
            tempdict["author_location"] = None

        try:
            tempdict["location"] = tweets.place.full_name
            tempdict["country"] = tweets.place.country
            tempdict["country_code"] = tweets.place.country_code
        except:
            tempdict["location"] = None
            tempdict["country"] = None
            tempdict["country_code"] = None

        if tweets.in_reply_to_status_id is None:
            tempdict["reply"] = False
        else:
            tempdict['reply'] = True
        tempdict["retweet"] = tweets.retweeted
        tempdict["author_name"] = tweets.author.name
        tempdict["author_image"] = tweets.author.profile_image_url
        tempdict["author_userid"] = tweets.author.screen_name
        tempdict['author_url'] = 'https://twitter.com/{}'.format(tempdict["author_userid"])
        # tempdict["dateTime"] = tweets.created_at.strftime("%Y-%m-%d %H:%M:%S")
        tempdict["datetime"] = int(time.mktime(time.strptime(tweets.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                                             '%Y-%m-%d %H:%M:%S'))) - time.timezone
        lst1 = []
        # tempdict["symbols"] = tweets.entities['symbols']
        # tempdict["mentions"] = tweets.entities["user_mentions"]
        for i in tweets.entities["user_mentions"]:
            lst1.append(i['screen_name'])

        tempdict["mentions"] = lst1
        if not tempdict["mentions"]:
            tempdict["mentions"] = None

        # tempdict["tags"] = tweets.entities["hashtags"]
        lst = []
        for i in tweets.entities["hashtags"]:
            # print(i['text'])
            lst.append(i['text'])
        tempdict["tags"] = tweets.entities["hashtags"]
        tempdict['tags'] = lst
        if not tempdict['tags']:
            tempdict['tags'] = None

        lst2 = []
        if tweets.entities["urls"] is not None:
            for i in tweets.entities["urls"]:
                # print(i['expanded_url'])
                lst2.append(i['expanded_url'])
            tempdict["linked_urls"] = lst2
            if not tempdict["linked_urls"]:
                tempdict["linked_urls"] = None

        if "media" in tweets.entities and tweets.entities["media"] is not None:
            tempdict["media"] = tweets.entities["media"]

            # checking the post type
            if '/photo/' in tempdict["media"][0]['expanded_url']:
                tempdict["type"] = 'image'
            elif '/video/' in tempdict["media"][0]['expanded_url']:
                tempdict["type"] = 'video'


        else:
            tempdict["media"] = None
            tempdict["type"] = 'status'

        # tempdict["media"] = tweets.entities["media"]
        tempdict["likes"] = tweets.favorite_count
        tempdict["shares"] = tweets.retweet_count
        tempdict["content"] = tweets.text
        try:
            tempdict['coordinates'] = tweets.geo['coordinates']
        except:
            tempdict['coordinates'] = None

        pol = self.obj.analize_sentiment(tweets.text)
        tempdict['polarity'] = pol

        if pol == 1:
            tempdict['polarity'] = 'positive'
            self.pos_count += 1
        elif pol == -1:
            tempdict['polarity'] = 'negative'
            self.neg_count += 1
        else:
            tempdict['polarity'] = 'neutral'
            self.neu_count += 1
        #
        # if(tweets.coordinates != None):
        #     tempdict["coordinates"] = tweets.coordinates
        # else:
        #     tempdict["coordinates"] = None

        # if(tweets.place != None):
        #     tempdict["country"] = tweets.place.country
            # tempdict["locationName"] = tweets.place.full_name
            # tempdict["placeType"] = tweets.place.place_type
            # tempdict["countryCode"] = tweets.place.country_code

        # else:
        #     tempdict["country"] = None
            # tempdict["locationName"] = None
            # tempdict["placeType"] = None
            # tempdict["countryCode"] = None

        # print(tweets.geo)
        # if(tweets.geo != None):
        #     tempdict["coordinates"] = tweets.geo["coordinates"]
        tempdict["url"] = "https://twitter.com/"+tweets.author.screen_name+"/status/"+tweets.id_str
        return tempdict

    def hashtags(self, inputdata, limit):
        if limit is None:
            limit = 20
        try:
            inputdata = "#"+inputdata
            temp = []
            for tweets in tweepy.Cursor(self.api.search, q=inputdata).items(int(limit)):
                data = self._jsonconvetor(tweets)
                temp.append(data)
                #self._insetvalue(data=tweets)

            ps = self.pos_count
            ng = self.neg_count
            nu = self.neu_count
            total = ps + ng + nu

            sentiments = dict()
            sentiments["positive"] = ps
            sentiments["negative"] = ng
            sentiments["neutral"] = nu

            # return {'results': temp,
            #         'sentiments': Sentiments,
            #         'total': limit}
            return temp

        except:
            print("error>>hashtags ::", exc_info()[1])

    def handlertweets(self, inputdata, limit):
        if limit is None:
            limit = 20
        try:
            inputdata = "@" + inputdata
            temp = []
            for tweets in tweepy.Cursor(self.api.search, q=inputdata).items(int(limit)):
                # print(tweets)
                data = self._jsonconvetor(tweets)
                #self._insetvalue(data=tweets)
                temp.append(data)

            ps = self.pos_count
            ng = self.neg_count
            nu = self.neu_count
            total = ps + ng + nu

            sentiments = dict()
            sentiments["positive"] = ps
            sentiments["negative"] = ng
            sentiments["neutral"] = nu

            # return {'results': temp,
            #         'sentiments': Sentiments,
            #         'total': limit}
            return temp

        except:
            print("error>>handlertweets ::", exc_info()[1])

    def profiletweets(self, handler, limit):
        try:
            temp = []
            timeline = self.api.user_timeline(screen_name=handler, include_rts=True, count=limit)
            for tweets in timeline:
                # print(tweets)
                data = self._jsonconvetor(tweets)
                # print(data)
                #self._insetvalue(data=tweets)
                temp.append(data)
            # print(temp)
            ps = self.pos_count
            ng = self.neg_count
            nu = self.neu_count
            total = ps + ng + nu

            sentiments = dict()
            sentiments["positive"] = ps
            sentiments["negative"] = ng
            sentiments["neutral"] = nu

            # return {'results': temp,
            #         'sentiments': Sentiments,
            #         'total': limit}
            return temp


        except:
            print("error>>profiletweets ::", exc_info()[1])


if __name__ == '__main__':
    obj = TwitterClass()
    print(obj.profiletweets('realdonaldtrump', 110))
    # print(obj.hashtags('politico', 34))
    # print(obj.handlertweets('realdonaldtrump', 100))
