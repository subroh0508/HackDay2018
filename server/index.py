import responder

api = responder.API()
@api.route("/convert_tweets")
async def home(request, response):
    body = await request.media()
    print(body['tweet'])

    response.media = { 'url': 'https://4.bp.blogspot.com/-DcD4rBwJpK4/WlGpoy3pIBI/AAAAAAABJo0/h_bt-BS3gM4DxnZO3Q6rOim1FPJE83NMACLcBGAs/s180-c/sweets_potatochips_chocolate.png' }

if __name__ == '__main__':
    api.run(port = 3000)
