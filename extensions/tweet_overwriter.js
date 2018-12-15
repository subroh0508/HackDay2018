//いいねを消し去る
function convert_nyan(){
	//要素を取得
	var elements = document.getElementsByClassName('ProfileTweet-action--favorite');
	while(elements.length != 0){
		//いいねの要素を削除
		elements[0].parentNode.removeChild(elements[0]);
	}
	console.log("hide");
}

//ストリーム変更時にいいねを消し去る
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
