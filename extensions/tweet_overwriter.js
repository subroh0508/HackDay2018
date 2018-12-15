var offset = 0;

//ツイートを全て「にゃーん」にする
function convert_nyan(){
	var tweets = document.getElementsByClassName('js-tweet-text');
	var index = offset;
    for (var i = offset; i < tweets.length; i++) {
		offset++;
		console.log(tweets[i])
		$.ajax({ 
			type: 'POST',
			url: 'http://localhost:3000/convert_tweets',
			data: { 'tweet': tweets[i].toString() },
		}).done(function(response) {
			console.log(tweets[index]);
			tweets[index].innerHTML = `<img src='${response.url}' width='100' height='100'/>`;
			index++;
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
