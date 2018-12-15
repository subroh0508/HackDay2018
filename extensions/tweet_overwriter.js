var offset = 0;

//ツイートを全て「にゃーん」にする
function convert_nyan(){
	var tweets = document.getElementsByClassName('js-tweet-text');
	var index = offset;
    for (var i = offset; i < tweets.length; i++) {
		offset++;
		var textContent = tweets[i].textContent
			.replace(/pic\.twitter\.com\/.*$/g, '')
			.replace(/(http|https):\/\/.*$/g, '');

		$.ajax({ 
			type: 'GET',
			url: 'http://localhost:3000/translate/'+textContent,
		}).done(function(response) {
			tweets[index].innerHTML = `<img src='${response.urls[0]}' width='100' height='100'/>`;
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
