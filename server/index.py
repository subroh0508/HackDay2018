import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import responder
from wordprosesser.library import IrasutoyaLibrary
import urllib.parse


api = responder.API()
library = IrasutoyaLibrary("../res/irasutoya_vectors.pickle")


@api.route("/translate/{tweet}")
async def home(request, response, *, tweet):
    tweet_decoded = urllib.parse.unquote(tweet)
    print("Query is", tweet_decoded)
    urls_translated = library.translate_to_images(tweet_decoded)
    response.media = {'urls': urls_translated}


if __name__ == '__main__':
    api.run(port=3000)
