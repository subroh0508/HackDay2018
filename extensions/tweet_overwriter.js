function guid() {
	function s4() {
	  	return Math.floor((1 + Math.random()) * 0x10000)
			.toString(16)
			.substring(1);
	}
	return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
 }

function getRandomInt(max) {
	return Math.floor(Math.random() * Math.floor(max));
}

function getSecretImage() {
	var images = [
		'https://3.bp.blogspot.com/-AsnnYzSW6vg/V6wGR6ksWOI/AAAAAAAA9Dg/my9L5O967Wo_-GiMJnu7-PxtdSFCxttKACLcB/s800/naisyo_woman.png',
		'https://3.bp.blogspot.com/-4tQDFzywlyE/VdL1J-vvleI/AAAAAAAAw6g/AvHAtxkyE-Y/s800/maruhi_mark.png',
		'https://2.bp.blogspot.com/-wFDZA61ytB8/WIHkGLIVhbI/AAAAAAABBLk/f87uBLuluW4kGLAf7fXbcGI3Dd5LCUX2QCEw/s800/book_taboo.png',
	];
 
	return images[getRandomInt(3)];
}

function findTweet(tweets, id) {
	var t = null;

	for (var j = 0; j < tweets.length; j++) {
		if (tweets[j] === undefined) {
			continue;
		}
		
		if (id === tweets[j].id) {
			t = tweets[j].content;
			break;
		}
	}

	return t;
}

function genInnerHtml(urls) {
	var html = '';
	
	for (var j = 0, url; url = urls[j]; j++) {
		html += `<img src='${url}' width='100' height='100'/>`;
	}

	if (urls.length == 0) {
		html += `<img src='${getSecretImage()}' width='100' height='100'>`;
	}

	return html;
}

function genProgressInnerHtml(inner, progressCount) {
	var replaced = inner.replace(/\<span\>.*\<\/span\>$/g, '');
	
	if (progressCount === 0) {
		return replaced;
	}

	return replaced + `<span>${progressCount}件浄水中...</span>`;
}

var offset = 0;

function convertIrasutoya() {
	var globalNav = document.getElementById('global-actions');
	var rawTweets = document.getElementsByClassName('js-tweet-text');
	var tweets = [];
	var progressCount = 0;

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

		progressCount++;
		globalNav.innerHTML = genProgressInnerHtml(globalNav.innerHTML, progressCount);
		$.ajax({ 
			type: 'GET',
			url: `http://localhost:3000/translate/${tweets[i].id}/${textContent}`,
		}).done(function(response) {
			progressCount--;
			globalNav.innerHTML = genProgressInnerHtml(globalNav.innerHTML, progressCount);

			var tweet = findTweet(tweets, response.id);

			if (tweet === null) {
				return;
			}

			tweet.innerHTML = genInnerHtml(response.urls);
		});
    }
}

function ObserveStream(){
	//オブザーバーの作成
	var observer = new MutationObserver(convertIrasutoya);
	//監視の開始
	observer.observe(document.getElementsByClassName('stream-items')[0], {
	    attributes: true,
	    childList:  true
	});
	console.log("observe");
	convertIrasutoya();
} 
//body変更時にObserveStreamを設定する。
//オブザーバーの作成
var observer = new MutationObserver(ObserveStream);
//監視の開始
observer.observe(document.getElementsByTagName("body")[0], {
    attributes: true
});
