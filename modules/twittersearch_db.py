from pymongo import MongoClient
from modules.twittersearch import TwitterSearch
from config import Config


class peopleSearch:

    def __init__(self):

        self.client = MongoClient(Config.DATABASE_CONFIG['host'], Config.DATABASE_CONFIG['port'])
        db = self.client.twitter_db
        self.collection = db.profile_search
        self.dict = {}
        self.obj = TwitterSearch()

    def db_check(self, query):

        r = self.obj.profilesearch(query)
        print(r)
        t = 0
        for i in r:
            if self.collection.find_one({'userid': i['userid']}):
                pass
            else:
                # print(i)
                t += 1
                self.collection.insert_one(i)
        self.client.close()
        print('no. of stored pages', t)
        # self.loop.close()
        #
        results = self.db_fetch(query)
        #
        # # return {'results': m}
        return results

  # ---------------------fetching total number of query pages from database----------------------------------------
    def db_fetch(self, query):
        self.collection.create_index([("description", "text"), ("name", "text")])

        lst = []
        cursor = self.collection.find(
            {"$text": {"$search": query}},
            {'score': {'$meta': "textScore"}}).sort([('score', {'$meta': "textScore"})])
        total = cursor.count()
        n = 0
        for i in cursor:
            # print(i)
            i.pop('_id')
            lst.append(i)
            n += 1

        # print('fetched pages from db', len(lst))
        # return {'results': lst,
        #         'total': n}
        return lst


if __name__ == '__main__':
    obj = peopleSearch()
    print(obj.db_check("trump"))

