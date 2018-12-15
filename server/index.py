import responder

api = responder.API()
@api.route("/convert_tweets")
async def home(request, response):
    body = await request.media()

    response.media = { 'url': body['tweet'] }

if __name__ == '__main__':
    api.run()
