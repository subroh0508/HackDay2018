import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import responder
from wordprosesser.library import IrasutoyaLibrary
import urllib.parse


api = responder.API()
library = IrasutoyaLibrary("../res/irasutoya_vectors.pickle")


@api.route("/translate/{id}/{tweet}")
async def home(request, response, *, id, tweet):
    tweet_decoded = urllib.parse.unquote(tweet)
    print("Query is", tweet_decoded)
    urls_translated = library.translate_to_images(tweet_decoded)
    response.media = { 'id': id, 'urls': urls_translated }
    response.headers.update({ 'Access-Control-Allow-Origin': '*' })


if __name__ == '__main__':
    api.run(port=3000)
