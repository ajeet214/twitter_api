from sys import exc_info
from modules.sentiment import Sentiment_analysis
import tweepy
import time
from requests_futures.sessions import FuturesSession
from concurrent.futures import ThreadPoolExecutor
import demjson
from credentials import TwitterKeys, google_keys


class TwitterSearch:

    def __init__(self):

        self.session = FuturesSession(executor=ThreadPoolExecutor(max_workers=5))
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

# data modifier
    def _jsonconvetor(self, tweets):
        # print(tweets)
        tempdict = dict()
        temp = dict()
        # tempdict["postContent"] = tweets.description
        pol = self.obj.analize_sentiment(tweets.description)
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

        # tempdict["followers_count"] = tweets.followers_count
        # tempdict["location"] = tweets.location
        # tempdict["name"] = tweets.name
        # # tempdict["lastName"] = None
        # tempdict["authorId"] = tweets.screen_name

        temp = tweets._json['created_at']
        var = [(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'), (
            9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec')]
        m = temp[4:7]
        for i in var:
            if i[1] == m:
                m = str(i[0])
        tempdict["datetime"] = int(time.mktime(time.strptime(temp[-4:]+'-'+m+'-'+temp[8:10]+' '+temp[11:19],
                                                             '%Y-%m-%d %H:%M:%S'))) - time.timezone

        tempdict["description"] = tweets._json['description']
        if not tempdict["description"]:
            tempdict["description"] = None

        tempdict["likes"] = tweets._json['favourites_count']
        tempdict["followers"] = tweets._json['followers_count']
        tempdict['following'] = tweets._json['friends_count']
        tempdict["userid"] = tweets._json['screen_name']
        tempdict['url'] = 'https://twitter.com/{}'.format(tempdict["userid"])

        # tempdict["geo_enabled"] = tweets._json['geo_enabled']
        # tempdict["id"] = tweets._json['id']
        # tempdict["listed_count"] = tweets._json['listed_count']
        tempdict["location"] = tweets._json['location']
        if not tempdict["location"]:
            tempdict["location"] = None

        tempdict["name"] = tweets._json['name']
        # try:
        #     tempdict["profile_banner_url"] = tweets._json['profile_banner_url']
        # except:
        #     pass
        tempdict["image"] = tweets._json['profile_image_url']

        # enhancement in the image quality
        tempdict["image"] = tempdict["image"].replace('_normal.', '_400x400.').replace('_normal.', '_400x400.').replace(
            '_normal.', '_400x400.')

        # tempdict["profile_link_color"] = tweets._json['profile_link_color']
        # tempdict["profile_sidebar_border_color"] = tweets._json['profile_sidebar_border_color']
        # tempdict["profile_use_background_image"] = tweets._json['profile_use_background_image']

        tempdict["tweets"] = tweets._json['statuses_count']
        tempdict["linked_url"] = tweets._json['url']
        tempdict["verified"] = tweets._json['verified']

        return tempdict
        # print(tempdict)

    def profilesearch(self, inputdata, limit=20):
        # if limit==None:
        #     limit=20

        tmp = []
        for users in tweepy.Cursor(self.api.search_users, q=inputdata).items(limit=int(limit)):
            # print(users)
            # self._insetvalue(users)
            data = self._jsonconvetor(users)
            # print(data)
            tmp.append(data)

        ps = self.pos_count
        ng = self.neg_count
        nu = self.neu_count
        total = ps + ng + nu

        Sentiments = dict()
        Sentiments["positive"] = ps
        Sentiments["negative"] = ng
        Sentiments["neutral"] = nu

        # removing duplicate dict object
        temp = [dict(t) for t in {tuple(d.items()) for d in tmp}]
        # print(temp)
        location_list = []
        for i in temp:
            if i['location'] is not None:
                location_list.append((i['location'], i['userid']))

        rs = []
        for u in location_list:
            rs.append((self.session.get('https://maps.google.com/maps/api/geocode/json?address=' + str(
                u[0])+'&key='+google_keys), u[0], u[1]))

        # print(rs)

        results = []
        for response in rs:

            try:
                r = response[0].result()
                lt = demjson.decode(r.content.decode('utf-8'))
                # print(lt)
                # print(lt['results'][0]['address_components'])
                temp_dict = {}

                for i in lt['results'][0]['address_components']:
                    if i['types'][0] == 'country':
                        # print(i['long_name'])
                        temp_dict['country_code'] = i['short_name']
                        temp_dict['country'] = i['long_name']
                        temp_dict['id'] = response[2]
                        temp_dict['location'] = response[1]
                        results.append(temp_dict)
                # print('**********')
                # print(temp_dict)
                if not temp_dict:
                    _dict = dict()
                    _dict['country'] = None
                    _dict['country_code'] = None
                    _dict['location'] = response[1]
                    _dict['id'] = response[2]
                    results.append(_dict)

            # when google geocode api sends error
            except IndexError:
                pass

        # print(results)

        final_list = []
        for i in range(len(temp)):
            final_dict = dict()

            final_dict['location'] = temp[i]['location']
            final_dict['description'] = temp[i]['description']
            final_dict['verified'] = temp[i]['verified']
            final_dict['datetime'] = temp[i]['datetime']
            final_dict['likes'] = temp[i]['likes']
            final_dict['following'] = temp[i]['following']
            final_dict['followers'] = temp[i]['followers']
            final_dict['name'] = temp[i]['name']
            final_dict['image'] = temp[i]['image']
            final_dict['userid'] = temp[i]['userid']
            final_dict['url'] = temp[i]['url']
            final_dict['posts'] = temp[i]['tweets']
            final_dict['linked_url'] = temp[i]['linked_url']
            final_dict['polarity'] = temp[i]['polarity']
            final_dict['type'] = 'identity'
            final_dict['country'] = None
            final_dict['country_code'] = None

            # final_dict['country'] = results[i]['country']
            # final_dict['country_code'] = results[i]['country_code']
            for j in results:
                if j['id'] == temp[i]['userid']:
                    final_dict['country'] = j['country']
                    final_dict['country_code'] = j['country_code']

            final_list.append(final_dict)
        return final_list

            # return temp

        # except:
        #     print("error>>handlertweets ::", exc_info()[1])


if __name__ == '__main__':
    obj = TwitterSearch()
    print(obj.profilesearch('eric freymond'))

# eric freymond
# niger delta