from flask import Flask, jsonify, request
from modules.twittersearch_db import peopleSearch
from modules.twitterprofile import Profileclass
from modules.twittertweets import TwitterClass
from modules.trend import geoTrend
from modules.twitter_db import Profile_existance
from modules.twitter_profile_db import Profile_fetch
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app)


# @app.route('/api/v1/profile/search/<string:q>')
# @app.route('/api/v1/profile/search/<string:q>/<int:limit>')
@app.route('/api/v1/search/profile')
def profile_search():
    f = peopleSearch()
    query = request.args.get('q')
    # limit = request.args.get('limit')
    result1 = f.db_check(query)
    return jsonify({'data': result1})


@app.route('/api/v1/profile')
def profile():
    username = request.args.get('id')
    g = Profile_fetch()
    result2 = g.db_check(username)
    return jsonify(result2)


@app.route('/api/v1/profile/friends')
def friends_profile():
    username = request.args.get('id')
    limit = request.args.get('limit')
    g = Profileclass()
    result2 = g.friendsprofile(username, limit)
    return jsonify({"data": result2})


@app.route('/api/v1/search/id')
def checker():
    query = request.args.get('q')
    #obj = EmailChecker()
    obj2 = Profile_existance()
    data = obj2.db_check(query)
    return jsonify({'data': {'availability': data['profileExists']}})


# @app.route('/api/v1/profile/friends/<string:fname>')
# @app.route('/api/v1/profile/friends/<string:fname>/<int:limit>')
# @app.route('/api/v1/profile/friends')
# def profile_friends():
#     query = request.args.get('q')
#     limit = request.args.get('limit')
#     h = Profileclass()
#     result3 = h.friendsprofile(query, limit)
#     return jsonify({'data': result3})


# @app.route('/api/v1/profile/tweets/<string:tweets>')
# @app.route('/api/v1/profile/tweets/<string:tweets>/<int:limit>')
@app.route('/api/v1/profile/tweets')
def profile_tweets():
    query = request.args.get('q')
    limit = request.args.get('limit')
    i = TwitterClass()
    result4 = i.profiletweets(query, limit)
    return jsonify({'data': result4})


# @app.route('/api/v1/tweets/hastag/<string:htag>')
# @app.route('/api/v1/tweets/hastag/<string:htag>/<int:limit>')
@app.route('/api/v1/tweets/hashtag')
def tweets_hashtag():
    query = request.args.get('q')
    limit = request.args.get('limit')
    j = TwitterClass()
    result5 = j.hashtags(query, limit)
    return jsonify({'data': result5})


# @app.route('/api/v1/tweets/handle/<string:handler>')
# @app.route('/api/v1/tweets/handle/<string:handler>/<int:limit>')
@app.route('/api/v1/tweets/handle')
def tweets_handle():
    query = request.args.get('q')
    limit = request.args.get('limit')
    k = TwitterClass()
    result6 = k.handlertweets(query, limit)
    return jsonify({'data': result6})


@app.route('/api/v1/trend')
def twitter_trend():
    query = request.args.get('q')
    obj = geoTrend()
    data = obj.geoStream(areaName=query)
    return jsonify(data)


if __name__ == '__main__':
    app.run(port=5002)
