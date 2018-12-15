function guid() {
	function s4() {
	  return Math.floor((1 + Math.random()) * 0x10000)
		.toString(16)
		.substring(1);
	}
	return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
  }

var offset = 0;

//ツイートを全て「にゃーん」にする
function convert_nyan(){
	var rawTweets = document.getElementsByClassName('js-tweet-text');
	var tweets = [];
	for (var i = offset; i < rawTweets.length; i++) {
		tweets[i] = { id: guid(), content: rawTweets[i] };
	}

    for (var i = offset; i < tweets.length; i++) {
		offset++;
		var textContent = tweets[i].content
			.textContent
			.replace(/pic\.twitter\.com\/.*$/g, '')
			.replace(/(http|https):\/\/.*$/g, '');

		if (textContent.length == 0) {
			continue;
		}
		$.ajax({ 
			type: 'GET',
			url: `http://localhost:3000/translate/${tweets[i].id}/${textContent}`,
		}).done(function(response) {
			var tweet = null;
			for (var j = 0; j < tweets.length; j++) {
				if (response.id === tweets[j].id) {
					tweet = tweets[j].content;
					break;
				}
			}

			if (tweet === null) {
				return;
			}

			tweet.innerHTML = `<img src='${response.urls[0]}' width='100' height='100'/>`;
		});
    }
}

function ObserveStream(){
	//オブザーバーの作成
	var observer = new MutationObserver(convert_nyan);
	//監視の開始
	observer.observe(document.getElementsByClassName('stream-items')[0], {
	    attributes: true,
	    childList:  true
	});
	console.log("observe");
	convert_nyan();
} 
//body変更時にObserveStreamを設定する。
//オブザーバーの作成
var observer = new MutationObserver(ObserveStream);
//監視の開始
observer.observe(document.getElementsByTagName("body")[0], {
    attributes: true
});
